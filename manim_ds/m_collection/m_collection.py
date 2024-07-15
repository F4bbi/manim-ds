from typing import override, Any

from manim import *
from manim.typing import Point3D, Vector3D

from manim_ds.constants import *
from manim_ds.utils.utils import *

class MElement(VGroup, Highlightable):
    def __init__(
        self,
        value: str,
        square_args: dict = DEFAULT_SQUARE_ARGS,
        value_args: dict = DEFAULT_VALUE_ARGS
    ):
        super().__init__()
        self.square = Rectangle(**square_args)
        self.value = Text(value, **value_args)
        self.value.font_size = self.value.font_size * self.square.width
        self.value.move_to(self.square)
        self._add_highlight(self.square)

        self += self.square
        self += self.value
    

    def set_value(self, new_value):
        self -= self.value
        self.value = set_text(self.value, str(new_value))
        self += self.value
        return self
    

    @override_animate(set_value)
    def _set_value_animation(self, new_value, anim_args=None):
        self.set_value(new_value)
        return Indicate(self.value, **anim_args)


class MIndexedElement(MElement):
    def __init__(
        self,
        value: str,
        square_args: dict = DEFAULT_SQUARE_ARGS,
        value_args: dict = DEFAULT_VALUE_ARGS
    ):
        super().__init__(value, square_args, value_args)


    def set_index(self, new_index):
        self -= self.index
        self.index = utils.set_text(self.index, str(new_index))
        self += self.index
    

    def add_index(
        self,
        index: Text,
        direction: Point3D = UP,
        buff: float = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER,
    ):
        self.index = index.next_to(self.square, direction, buff)
        self += self.index


class MCollection(VGroup, Labelable):
    def __init__(
        self,
        arr: list,
        direction: Vector3D = RIGHT,
        square_args: dict = DEFAULT_SQUARE_ARGS,
        value_args: dict = DEFAULT_VALUE_ARGS
    ):
        super().__init__()
        self.elements = []
        
        self.set_square_args(square_args)
        self.set_value_args(value_args)
        
        self.spawn_point = Rectangle(**self.square_args).set_opacity(0)
        self += self.spawn_point

        self._dir = direction
        self._dir_map = {
            UP.data.tobytes(): RIGHT,
            DOWN.data.tobytes(): RIGHT,
            RIGHT.data.tobytes(): UP,
            LEFT.data.tobytes(): UP,
        }

        def update_args(obj):
            square_width = self._get_square_else_spawnpoint(0).width
            if "width" and "height" in obj.square_args:
                obj.square_args["width"] = obj.square_args["height"] = square_width
        self.add_updater(update_args)

        if not hasattr(self, "margin"):
            self.margin = 0

        for v in arr:
            self.append(v)
        self.move_to(ORIGIN)


    def set_square_args(self, square_args: dict):
        self.square_args = square_args.copy()
    

    def set_value_args(self, value_args: dict):
        self.value_args = value_args.copy()


    def append(
        self,
        value: int | float | str
    ):
        new_elem = MElement(
            str(value),
            self.square_args,
            self.value_args
        )
                
        self.elements.append(new_elem)

        if len(self.elements) > 1:
            self.elements[-1].next_to(self.elements[-2].square, self._dir, self.margin)
        else:
            self.elements[-1].move_to(self.spawn_point)

        self += self.elements[-1]
        return self
    

    @override_animate(append)
    def _append_animation(
        self,
        value: int | float | str,
        anim_args = None
    ):
        self.append(value)
        return Write(self.elements[-1], **anim_args)


    def _logic_pop(self, index):
        popped_element = self.elements[index]
        self -= popped_element
        self.elements.pop(index)
        return popped_element


    def pop(
        self,
        index: Any
    ):
        if not len(self.elements):
            return
        popped_element = self._logic_pop(index)

        VGroup(*self.elements[index:]) \
        .shift(-(self._dir * popped_element.square.width))
    

    @override_animate(pop)
    def _pop_animation(
        self,
        index: Any,
        anim_args = None
    ):
        popped_element = self._logic_pop(index)

        elem_shift = VGroup(*self.elements[index:])

        anims = [
            FadeOut(popped_element),
            ApplyMethod(elem_shift.shift, -(self._dir * popped_element.square.width))
        ]

        return Succession(
            *anims,
            **anim_args,
            group=VGroup(self, popped_element)
        )


    def _visual_swap(self, i, j):
        elem_i = self.elements[i]
        elem_j = self.elements[j]
        temp = elem_i.copy()
        elem_i.move_to(elem_j, DOWN)
        elem_j.move_to(temp, DOWN)
    

    def _logic_swap(self, i, j):        
        # Element swap
        # We have to remove first them from the scene to work correctly
        self -= self.elements[i]
        self -= self.elements[j]
        
        self.elements[i], self.elements[j] = self.elements[j], self.elements[i]
        
        # We can add the elements again
        self += self.elements[i]
        self += self.elements[j]


    def swap(self, i, j):
        self._visual_swap(i, j)
        self._logic_swap(i, j)
    

    @override_animate(swap)
    def _swap_animation(self, i, j, path_arc=PI/2, anim_args=None):
        anim = ApplyMethod(self._visual_swap, i, j, path_arc=path_arc, **anim_args)
        self._logic_swap(i, j)
        return anim
    

    def _get_square_else_spawnpoint(self, index):
        return self.elements[index].square if self.elements else self.spawn_point


    def __getitem__(self, key):
        if(key >= len(self.elements)):
            raise Exception("Index out of bounds!")
        return self.elements[key]
    
    @override
    def add_label(
        self,
        text: Text,
        direction: Vector3D = UP,
        buff: float = 0.5,
        **kwargs
    ):
        super().add_label(text, direction, buff, **kwargs)

        # If label position is parallel to array growth direction
        # the label have to be centered
        if np.array_equal(self._dir, direction):
            reference_element = self._get_square_else_spawnpoint(-1)
        elif np.array_equal(self._dir, -direction):
            reference_element = self._get_square_else_spawnpoint(0)
        else:
            reference_element = None

        if reference_element:
            self.label.next_to(reference_element, direction, buff)
        
        self += self.label
        return self