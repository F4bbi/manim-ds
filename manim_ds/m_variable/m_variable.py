from typing import override, Any

from manim import *
from manim.typing import Point3D, Vector3D

from manim_ds.constants import *
from manim_ds.utils.utils import *
from manim_ds.m_collection.m_collection import MElement

class MVariable(MElement, Labelable):
    def __init__(
        self,
        value: str,
        square_args: dict = DEFAULT_SQUARE_ARGS,
        value_args: dict = DEFAULT_VALUE_ARGS
    ):
        super().__init__(value, square_args, value_args)
    

    def add_label(
        self,
        text: Text,
        direction: Vector3D = UP,
        buff: float = 0.5,
        **kwargs
    ):
        super().add_label(text, direction, buff, **kwargs)
        self += self.label
        return self