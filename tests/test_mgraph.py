from manim import *

from manim_ds.m_collection.m_stack import *
from manim_ds.m_graph.m_graph import *

class DfsIterative(Scene):
    def dfs(self, graph, mGraph, mStack, start):
        visited = {}
        stack = [start]
        prevList = [None]
        
        self.play(mStack.animate.append(start))
        
        for node in graph:
            visited[node] = False

        while stack:
            node = stack.pop()
            self.play(mStack.animate.pop())
            
            prev = prevList.pop()
            if prev and not visited[node]:
                    self.play(mGraph[(prev, node)].animate.highlight())

            if not visited[node]:
                self.play(mGraph[node].animate.highlight())
                visited[node] = True
            
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    stack.append(neighbor)
                    self.play(mStack.animate.append(neighbor))
                    prevList.append(node)

    
    def construct(self):
        graph = {
            '0': ['1', '2'],
            '1': ['0', '2', '3', '4'],
            '2': ['0', '1'],
            '3': ['1', '5'],
            '4': ['1'],
            '5': ['3', '6', '7', '8'],
            '6': ['5'],
            '7': ['5', '8'],
            '8': ['5', '7', '9'],
            '9': ['8']
        }

        nodes_and_positions = {
            '0': LEFT * 6,
            '1': LEFT * 4 + UP,
            '2': LEFT * 4 + DOWN,
            '3': LEFT * 2,
            '4': LEFT * 2 + UP * 2,
            '5': ORIGIN,
            '6': LEFT * 2 + DOWN * 2,
            '7': RIGHT * 2 + DOWN * 2,
            '8': RIGHT * 2 + UP * 2,
            '9': RIGHT * 4 + UP * 2,
        }
        start = '0'

        title = Text("Depth-First Search in un grafo", font="Cascadia Code").to_edge(UP)
        self.play(Create(title))
        mGraph = MGraph(graph, nodes_and_positions, PURPLE_CIRCLE_ARGS).scale(0.7).to_edge(LEFT).shift(DR)
        mStack = MStack(square_args=BLUE_SQUARE_ARGS).scale(0.7).to_edge(RIGHT).shift(DL)
        self.play(Create(mGraph))
        self.play(Create(mStack))
        self.dfs(graph, mGraph, mStack, start)
        self.wait()