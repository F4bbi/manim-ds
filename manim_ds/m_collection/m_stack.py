from typing import override, Any

from manim import *
from manim.typing import Point3D, Vector3D

from manim_ds.constants import *
from manim_ds.utils.utils import *
from manim_ds.m_collection.m_collection import *

class MStack(MCollection):
    def __init__(
        self,
        arr: list = [],
        buff: float = 0.1,
        square_args: dict = DEFAULT_SQUARE_ARGS,
        value_args: dict = DEFAULT_VALUE_ARGS
    ):
        self.margin: float = buff
        super().__init__(arr, UP, square_args, value_args)

        elem = self.elements[0].square if self.elements else self.spawn_point
        container_height = (len(arr) + 3) * elem.height if arr else self.spawn_point.height * 7

        self.bottom_line: Line = (
            Line(ORIGIN, [elem.width + 2 * buff, 0, 0])
            .next_to(elem, DOWN, buff)
        )
        self.left_line: Line = (
            Line([0, container_height, 0], ORIGIN)
            .next_to(self.bottom_line, UL, 0)
        )
        self.right_line: Line = self.left_line.copy().next_to(self.bottom_line, UR, 0)
        
        self.container: VGroup = VGroup(self.left_line, self.bottom_line, self.right_line)
        self += self.container
        self.move_to(ORIGIN)
        self.stack_spawnpoint: Point3D = None

        # When the stack is scaled or moved,
        # the spawn_point of the objects must be changed as well
        def update_stack_attr(obj):
            obj.stack_spawnpoint = obj.get_spawn_point()
            obj.margin = buff * self.spawn_point.width
        
        self.add_updater(update_stack_attr)
    
    
    def get_spawn_point(self):
        return self.bottom_line.get_center() + (UP * self.right_line.height) + UP * self.spawn_point.width
    
    def append(
        self,
        value: Any
    ):
        return super().append(value)

    @override_animate(append)
    def _append_animation(self, value: str, anim_args=None):
        self.append(value)
        new_pos = self.elements[-1].get_center()
        self.elements[-1].move_to(self.stack_spawnpoint)
        
        return Succession(
            Create(self.elements[-1], **anim_args),
            ApplyMethod(self.elements[-1].move_to, new_pos),
            group=self
        )
    
    @override
    def pop(self):
        super().pop(len(self.elements) - 1)

    @override_animate(pop)
    def _pop_animation(self, anim_args=None):
        popped_element = self.elements[-1].copy()
        self.pop()
        return Succession(
            ApplyMethod(popped_element.move_to, self.stack_spawnpoint),
            FadeOut(popped_element),
            group=VGroup(self, popped_element)
        )
    

    def add_label(
        self,
        text: Text,
        direction: Vector3D = UP,
        buff: float = 0.5,
        **kwargs
    ):
        super().add_label(text, direction, buff, **kwargs)
        self.label.move_to(self.get_spawn_point())
        return self