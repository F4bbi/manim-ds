from typing import override, Any

from manim import *
from manim.typing import Point3D, Vector3D

from manim_ds.constants import *
from manim_ds.utils.utils import *
from manim_ds.m_collection.m_collection import *

class MArray(MCollection):
    def __init__(
        self,
        arr: list,
        direction: Vector3D = RIGHT,
        square_args: dict = DEFAULT_SQUARE_ARGS,
        value_args: dict = DEFAULT_VALUE_ARGS
    ):
        self.__index_enabled: bool = False
        super().__init__(arr, direction, square_args, value_args)
    

    def set_index_args(self, index_args: dict):
        self.index_args = index_args.copy()
    

    def append(
        self,
        value: Any
    ):
        new_elem = MIndexedElement(
            str(value),
            self.square_args,
            self.value_args
        )
                
        self.elements.append(new_elem)

        if len(self.elements) > 1:
            self.elements[-1].next_to(self.elements[-2].square, self._dir, self.margin)
        else:
            self.elements[-1].move_to(self.spawn_point)
        
        if self.__index_enabled:
            index = Text(str(len(self.elements) - 1), **self.index_args)
            index.font_size = index.font_size * self.elements[-1].square.width
            self.elements[-1].add_index(index, self.__index_dir, self.__index_buff)
        self += self.elements[-1]
        return self
    

    @override_animate(append)
    def _append_animation(
        self,
        value: Any,
        anim_args = None
    ):
        return super()._append_animation(value, anim_args)
    

    def pop(
        self,
        index: int = -1
    ):
        if not len(self.elements):
            return
        popped_element = self.elements[index].copy()
        super().pop(index) 

        if self.__index_enabled:
            self.__set_index_from(index, len(self.elements) - 1, popped_element.index)
    

    @override_animate(pop)
    def _pop_animation(
        self,
        index: int = -1,
        anim_args = None
    ):
        popped_element = self._logic_pop(index)

        elem_shift = VGroup(*self.elements[index:])

        anims = [
            FadeOut(popped_element),
            ApplyMethod(elem_shift.shift, -(self._dir * popped_element.square.width))
        ]

        if self.__index_enabled:
            anims.append(ApplyMethod(self.__set_index_from, index, len(self.elements) - 1, popped_element.index.copy()))

        return Succession(
            *anims,
            **anim_args,
            group=VGroup(self, popped_element)
        )
    

    def __set_index_from(self, start, end, popped_index):
        old_index = popped_index
        for i in range(start, end + 1):
            curr = self.elements[i]
            new_index = old_index.copy().move_to(curr.index)
            old_index = curr.index
            curr -= curr.index
            curr.index = new_index
            curr += curr.index
        return self
        

    def _get_index_buff(self):
        if self.elements:
            last_element = self.elements[-1]
            square_center = last_element.square.get_center()
            index_center = last_element.index.get_center()
            offset = last_element.square.width / 2

            if np.array_equal(self._dir, UP) or np.array_equal(self._dir, DOWN):
                offset += last_element.index.width / 2
                direction_offset = [offset, 0, 0]
            else:
                offset += last_element.index.height / 2
                direction_offset = [0, offset, 0]

            if np.array_equal(self.__index_dir, UP) or np.array_equal(self.__index_dir, RIGHT):
                return index_center - square_center - direction_offset
            else:
                return square_center - index_center - direction_offset
    

    def _visual_swap(self, i, j):
        elem_i = self.elements[i]
        elem_j = self.elements[j]
        elem_i_group = VGroup(elem_i.square, elem_i.value)
        temp = elem_i_group.copy()
        elem_j_group = VGroup(elem_j.square, elem_j.value)
        elem_i_group.move_to(elem_j_group, DOWN)
        elem_j_group.move_to(temp, DOWN)

    
    def _logic_swap(self, i, j):        
        # Element swap
        # We have to remove first them from the scene to work correctly
        self -= self.elements[i]
        self -= self.elements[j]
        
        self.elements[i], self.elements[j] = self.elements[j], self.elements[i]
        
        if self.__index_enabled:
            # Index swap
            # We have to remove first them from the scene to work correctly
            self.elements[i] -= self.elements[i].index
            self.elements[j] -= self.elements[j].index
            
            self.elements[i].index, self.elements[j].index = self.elements[j].index, self.elements[i].index

            # We can add the indexes again
            self.elements[i] += self.elements[i].index
            self.elements[j] += self.elements[j].index

        # We can add the elements again
        self += self.elements[i]
        self += self.elements[j]
    

    def add_indexes(
        self,
        direction: Vector3D = UP,
        buff: float = DEFAULT_MOBJECT_TO_MOBJECT_BUFFER,
        index_args: dict = DEFAULT_INDEX_ARGS
    ):
        if self.__index_enabled:
            return self
        if np.array_equal(np.abs(self._dir), np.abs(direction)):
            raise Exception("The direction given is parallel to array growth direction!")
        
        for i in range(len(self.elements)):
            self.elements[i].add_index(Text(str(i), **index_args), direction, buff)
        
        self.__index_enabled = True
        self.__index_dir = direction
        self.__index_buff = buff
        self.set_index_args(index_args)
        def update_attr(obj):
            if obj.elements:
                obj.__index_buff = obj._get_index_buff()
        self.add_updater(update_attr)

        return self