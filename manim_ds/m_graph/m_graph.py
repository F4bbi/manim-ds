from typing import override, Any

from manim import *
from manim.typing import Point3D, Vector3D
import networkx as nx
from math import *
from abc import ABC, abstractmethod

from manim_ds.constants import *
from manim_ds.utils.utils import *
from manim_ds.m_collection.m_collection import *

class MGraph(VDict, Labelable):
    def __init__(
            self,
            graph: list[list[str]] | dict[str, dict[str, str]],
            nodes_position: dict,
            node_args: dict = DEFAULT_CIRCLE_ARGS,
            value_args: dict = DEFAULT_VALUE_ARGS,
            edge_args: dict = DEFAULT_EDGE_ARGS
        ):
        super().__init__()
        self.nodes = {}
        self.edges = {}

        self.set_node_args(node_args)
        self.set_value_args(value_args)
        self.set_edge_args(edge_args)
        self.set_weight_args(DEFAULT_WEIGHT_ARGS)

        for node in graph.keys():
            pos = nodes_position[node] if node in nodes_position else ORIGIN
            self.add_node(node, pos)
        
        if isinstance(graph, list) or isinstance(graph, dict):
            # The graph can be list of list or dict of list
            for src, destinations in graph.items() if isinstance(graph, dict) else enumerate(graph):
                for dest in destinations:
                    # If the graph is not weighted
                    # Example: {'0': ['1', '2']}
                    if isinstance(dest, str):
                        self.add_edge(str(src), dest)
                    # If the graph is weighted
                    # Example: {'0': [('1', 2), ('2', 4)]}
                    elif isinstance(dest, tuple) and len(dest) == 2 and isinstance(dest[0], str) and isinstance(dest[1], int):
                        dest, weight = dest
                        self.add_edge(str(src), dest, weight)

    class Node(VGroup, Highlightable):
        def __init__(
            self,
            name: str,
            position: Point3D = ORIGIN,
            circle_args: dict = DEFAULT_CIRCLE_ARGS,
            value_args: dict = DEFAULT_VALUE_ARGS
        ):
            super().__init__()
            self.name = name

            self.label = (
                Text(str(name), **value_args)
                .move_to(position)
                .set_z_index(3)
            )
            
            self.circle = (
                Circle(**circle_args)
                .move_to(position)
                .set_z_index(2)
            )
            
            self._add_highlight(self.circle)
            
            self += self.circle
            self += self.label


    class Edge(VGroup, Highlightable, ABC):
        def __init__(
            self,
            line: Line | ArcBetweenPoints,
            arrow: bool = True
        ):
            super().__init__()
            self.line = line.set_z_index(0)
            
            if arrow:
                self.line.add_tip()
                self.line.get_tip().set_stroke(width=1)
            
            self._add_highlight(self.line)
            self.set_highlight()
            
            self += self.line
        

        def weighted(
            self,
            weight: float = 0,
            weight_args: dict = DEFAULT_WEIGHT_ARGS
        ):
            self.label = Text(str(weight), **weight_args)
            self += self.label
            return self
        
        
        def set_highlight(self, stroke_color: ManimColor = RED, stroke_width: float = 8):
            super().set_highlight(stroke_color, stroke_width)
            if hasattr(self.line, 'tip'):
                arrow_width = self.line.get_tip().get_width()
                self.highlighting.get_tip().set_stroke(width=arrow_width).set_color(stroke_color).set_opacity(1)


        @abstractmethod
        def get_line_start_end(
            self,
            node1_center: Point3D,
            node2_center: Point3D,
            node1_radius: float,
            node2_radius: float
        ):
            pass
        
        @abstractmethod
        def get_label_position(
            self,
            label_distance: float
        ):
            pass
    
    
    class StraightEdge(Edge):
        def __init__(
            self,
            node1_center: Point3D,
            node2_center: Point3D,
            node1_radius: float,
            node2_radius: float,
            arrow: bool = True,
            line_args: dict = DEFAULT_EDGE_ARGS
        ):
            start, end = self.get_line_start_end(node1_center, node2_center, node1_radius, node2_radius)
            super().__init__(Line(start, end, **line_args), arrow)
        

        def weighted(
            self,
            weight: float = 0,
            label_distance: float = 0.3,
            weight_args: dict = DEFAULT_WEIGHT_ARGS
        ):
            super().weighted(weight, weight_args)
            self.label_distance: float = label_distance
            label_position = self.get_label_position(label_distance)
            self.label.move_to(label_position)
            return self


        def get_line_start_end(
            self,
            node1_center: Point3D,
            node2_center: Point3D,
            node1_radius: float,
            node2_radius: float
        ):
            direction = Line(node1_center, node2_center).get_unit_vector()
            start = node1_center + direction * node1_radius
            end = node2_center - direction * node2_radius
            return start, end
        

        def get_label_position(
            self,
            label_distance: float
        ):
            direction = self.line.get_unit_vector()
            mean = self.line.get_start() + direction * self.line.get_length() / 2
            orthogonal_dir = np.array([direction[1], -direction[0], 0])
            position = mean + orthogonal_dir * label_distance
            return position
    

    class CurvedEdge(Edge):
        def __init__(
            self,
            node1_center: Point3D,
            node2_center: Point3D,
            node1_radius: float,
            node2_radius: float,
            arrow: bool = True,
            node_angle: float = PI/3,
            arc_angle: float = PI/3,
            edge_args: dict = DEFAULT_EDGE_ARGS
        ):
            self.node_angle = node_angle
            self.arc_angle = arc_angle
            start, end = self.get_line_start_end(node1_center, node2_center, node1_radius, node2_radius, node_angle)
            super().__init__(ArcBetweenPoints(start, end, arc_angle, **edge_args), arrow)
        
        
        def weighted(
            self,
            weight: float = 0,
            label_distance: float = 0.3,
            weight_args: dict = DEFAULT_WEIGHT_ARGS
        ):
            super().weighted(weight, weight_args)            
            self.label_distance: float = label_distance
            label_position = self.get_label_position(label_distance)
            self.label.move_to(label_position)
            return self
        

        def get_line_start_end(
            self,
            node1_center: Point3D,
            node2_center: Point3D,
            node1_radius: float,
            node2_radius: float,
            start_angle: float = PI/3
        ):
            edge_direction = Line(node1_center, node2_center).get_unit_vector()
            edge_angle = acos(edge_direction[0])
            if(edge_direction[1] < 0):
                edge_angle = -edge_angle

            vector_start = np.array(
                [cos(edge_angle-start_angle), sin(edge_angle-start_angle), 0]
            )
                    
            vector_end = np.array(
                [cos(edge_angle-(PI-start_angle)), sin(edge_angle-(PI-start_angle)), 0]
            )

            direction_start = normalize(vector_start)
            direction_end = normalize(vector_end)        

            start = node1_center + direction_start * node1_radius
            end = node2_center + direction_end * node2_radius

            return start, end
        

        def get_label_position(
            self,
            label_distance: float
        ):
            arc = ArcBetweenPoints(self.line.get_start(), self.line.get_end(), self.arc_angle)
            line = Line(self.line.get_start(), self.line.get_end())
            direction = line.get_unit_vector()
            orthogonal_dir = np.array([direction[1], -direction[0], 0])
            position = arc.get_boundary_point(orthogonal_dir) + orthogonal_dir*len(line)*label_distance
            return position


    def add_node(
        self,
        name: str,
        position: Point3D = ORIGIN
    ):
        new_node = self.Node(name, position, self.node_args, self.value_args)
        self.nodes[name] = new_node
        self.add([(name, new_node)])
        return self


    @override_animate(add_node)
    def _add_node_animation(
        self,
        name: str,
        position: Point3D = ORIGIN,
        anim_args=None
    ):
        if anim_args is None:
            anim_args = {}
        
        self.add_node(name, position)
        return Create(self.nodes[name], **anim_args)
    

    def add_edge(
        self,
        node1_name: str,
        node2_name: str,
        weight: float = None,
        label_distance: float = 0.3
    ):
        edge_name = (node1_name, node2_name)
        edge_name_rev = (node2_name, node1_name)
        arrow = True
        
        node1 = self.nodes[node1_name].circle
        node2 = self.nodes[node2_name].circle

        if(edge_name_rev in self.edges):
            arrow = False
            node1, node2 = node2, node1

        new_edge = self.StraightEdge(
            node1.get_center(),
            node2.get_center(),
            node1.width / 2,
            node2.width / 2,
            arrow,
            self.edge_args
        )
        if weight:
            new_edge.weighted(
                weight,
                label_distance,
                self.weight_args
            )
        
        self.edges[edge_name] = new_edge
        
        if(edge_name_rev in self.edges):
            self.edges[edge_name_rev] = self[edge_name_rev] = new_edge
        
        self.add([(edge_name, new_edge)])
        return self


    @override_animate(add_edge)
    def _add_edge_animation(
        self,
        node1_name: str,
        node2_name: str,
        weight: float = None,
        label_distance: float = 0.3,
        anim_args=None
    ):
        if anim_args is None:
            anim_args = {}
        
        self.add_edge(
            node1_name,
            node2_name,
            weight,
            label_distance
        )

        return Create(self.edges[(node1_name, node2_name)], **anim_args)    
    

    def add_curved_edge(
        self,
        node1_name: str,
        node2_name: str,
        weight: float = None,
        label_distance: float = 0.3,
        node_angle: float = PI/3,
        arc_angle: float = PI/3
    ):
        edge_name = (node1_name, node2_name)
        edge_name_rev = (node2_name, node1_name)
        arrow = True
        
        node1 = self.nodes[node1_name].circle
        node2 = self.nodes[node2_name].circle

        if(edge_name_rev in self.edges):
            arrow = False
            node1, node2 = node2, node1

        new_edge = self.CurvedEdge(
            node1.get_center(),
            node2.get_center(),
            node1.width / 2,
            node2.width / 2,
            arrow,
            node_angle,
            arc_angle,
            self.edge_args
        )
        if weight:
            new_edge.weighted(
                weight,
                label_distance,
                self.weight_args
            )
        
        self.edges[edge_name] = new_edge
        
        if(edge_name_rev in self.edges):
            self.edges[edge_name_rev] = self[edge_name_rev] = new_edge
        
        self.add([(edge_name, new_edge)])
        return self


    @override_animate(add_curved_edge)
    def _add_curved_edge_animation(
        self,
        node1_name: str,
        node2_name: str,
        weight: float = None,
        label_distance: float = 0.3,
        node_angle: float = PI/3,
        arc_angle: float = PI/3,
        anim_args=None
    ):
        if anim_args is None:
            anim_args = {}
        
        self.add_curved_edge(
            node1_name,
            node2_name,
            weight,
            label_distance,
            node_angle,
            arc_angle,
        )

        return Create(self.edges[(node1_name, node2_name)], **anim_args)
    

    def show_backward_edge(
        self,
        node1_name: str,
        node2_name: str,
        forward_weight: float,
        backward_weight: float,
        label_distance: float = 0.3,
        node_angle: float = PI/6,
        arc_angle: float = PI/6
    ):
        edge_name = (node1_name, node2_name)
        edge_name_rev = (node2_name, node1_name)
        
        node1 = self.nodes[node1_name].circle
        node2 = self.nodes[node2_name].circle

        new_edge_1 = self.CurvedEdge(
            node1.get_center(),
            node2.get_center(),
            node1.width / 2,
            node2.width / 2,
            True,
            node_angle,
            arc_angle,
            self.edge_args
        )
        new_edge_1.weighted(
            forward_weight,
            label_distance,
            self.weight_args
        )

        new_edge_2 = self.CurvedEdge(
            node2.get_center(),
            node1.get_center(),
            node2.width / 2,
            node1.width / 2,
            True,
            node_angle,
            arc_angle,
            self.edge_args
        )
        new_edge_2.weighted(
            backward_weight,
            label_distance,
            self.weight_args
        )
        
        self.edges[edge_name] = self[edge_name] = new_edge_1
        self.edges[edge_name_rev] = new_edge_2
        self.add([(edge_name_rev, new_edge_2)])
        return self


    @override_animate(show_backward_edge)
    def _show_backward_edge_animation(
        self,
        node1_name: str,
        node2_name: str,
        forward_weight: float,
        backward_weight: float,
        label_distance: float = 0.3,
        node_angle: float = PI/6,
        arc_angle: float = PI/6,
        anim_args=None
    ):
        edge_name = (node1_name, node2_name)
        edge_name_rev = (node2_name, node1_name)
        old_edge = self.edges[edge_name]
        
        self.show_backward_edge(
            node1_name,
            node2_name,
            forward_weight,
            backward_weight,
            label_distance,
            node_angle,
            arc_angle
        )
        
        return Succession(
            FadeOut(self.edges[edge_name], run_time=0.0001),
            FadeOut(self.edges[edge_name_rev], run_time=0.00001),
            ReplacementTransform(old_edge, VGroup(self.edges[edge_name], self.edges[edge_name_rev]), **anim_args),
            group=VGroup(self, old_edge)
        )
    

    def node_layout(
        self,
        layout: str = 'kamada_kawai_layout'
    ):
        G = nx.DiGraph()
        G.add_edges_from(self.edges.keys())

        try:
            layout_function = eval(f'nx.{layout}')
            pos = layout_function(G)
        
        except:
            print('Layout not available')
            pos = nx.kamada_kawai_layout(G)

            
        labels = list(pos.keys())

        x = [x for x, y in pos.values()]
        y = [y for x, y in pos.values()]

        coeff_x = config.frame_x_radius/(abs(max(x)-min(x)))
        coeff_y = config.frame_y_radius/(abs(max(y)-min(y)))

        positions = []

        for label in labels:
            positions.append(np.array([pos.get(label)[0]*coeff_x, pos.get(label)[1]*coeff_y, 0]))

        nodes_and_positions = dict(zip(labels, positions))
        for node in nodes_and_positions:
            self.nodes[node].move_to(nodes_and_positions[node])
        for edge in self.edges:
            node1 = self.nodes[edge[0]].circle
            node2 = self.nodes[edge[1]].circle
            start, end = self.edges[edge].get_line_start_end(
                node1.get_center(),
                node2.get_center(),
                node1.width / 2,
                node2.width / 2
            )
            mEdge = self.edges[edge]
            mEdge.line.put_start_and_end_on(start, end)
            mEdge.highlighting.put_start_and_end_on(start, end)
            if(hasattr(mEdge, 'label')):
                label_position = mEdge.get_label_position(mEdge.label_distance)
                mEdge.label.move_to(label_position)
        
        return self
    

    def set_node_highlight(
        self,
        color: ManimColor = RED,
        width: float = 8,
    ):
        for node in self.nodes:
            self.nodes[node].set_highlight(color, width)
        return self

    def set_edge_highlight(
        self,
        color: ManimColor = RED,
        width: float = 8,
    ):
        for edge in self.edges:
            self.edges[edge].set_highlight(color, width)
        return self


    def set_node_args(self, node_args: dict):
        self.node_args = node_args.copy()
    

    def set_value_args(self, value_args: dict):
        self.value_args = value_args.copy()
    

    def set_edge_args(self, edge_args: dict):
        self.edge_args = edge_args.copy()
    

    def set_weight_args(self, weight_args: dict):
        self.weight_args = weight_args.copy()
    

    def add_label(
        self,
        text: Text,
        direction: Vector3D = UP,
        buff: float = 0.5,
        **kwargs
    ):
        super().add_label(text, direction, buff, **kwargs)
        self["label"] = self.label
        return self