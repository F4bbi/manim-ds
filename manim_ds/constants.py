from manim import *
from manim.typing import Point3D, Vector3D

#-----------Square configs-----------
DEFAULT_SQUARE_ARGS: dict = {
    "color": WHITE,
    "stroke_width": 6,
    "width": 1,
    "height": 1,
}

PURPLE_SQUARE_ARGS: dict = {
    "color": ManimColor("#eb97fc"),
    "fill_color": ManimColor("#8c46d6"),
    "fill_opacity": 1,
    "stroke_width": 6,
    "width": 1,
    "height": 1,
}

BLUE_SQUARE_ARGS: dict = {
    "color": BLUE_B,
    "fill_color": BLUE_D,
    "stroke_width": 6,
    "fill_opacity": 1,
    "width": 1,
    "height": 1,
}

#-----------Value configs-----------
DEFAULT_VALUE_ARGS: dict = {
    "color": WHITE,
    "font": "Cascadia Code",
    "font_size": 48,
    "weight": BOLD
}

#-----------Index configs-----------
DEFAULT_INDEX_ARGS: dict = {
    "color": WHITE,
    "font": "Cascadia Code",
    "font_size": 32
}

BLUE_INDEX_ARGS: dict = {
    "color": BLUE_D,
    "font": "Cascadia Code",
    "font_size": 32
}

PURPLE_INDEX_ARGS: dict = {
    "color": ManimColor("#fabcff"),
    "font": "Cascadia Code",
    "font_size": 32
}

#-----------Circle configs-----------
DEFAULT_CIRCLE_ARGS: dict = {
    "color": WHITE,
    "stroke_width": 6,
    "radius": 0.5
}

PURPLE_CIRCLE_ARGS: dict = {
    "color": ManimColor("#eb97fc"),
    "fill_color": ManimColor("#8c46d6"),
    "fill_opacity": 0.5,
    "stroke_width": 6,
    "radius": 0.5,
}

BLUE_CIRCLE_ARGS: dict = {
    "color": BLUE_B,
    "fill_color": BLUE_D,
    "stroke_width": 6,
    "fill_opacity": 0.75,
    "radius": 0.5,
}

#-----------Edge configs-----------
DEFAULT_EDGE_ARGS: dict = {
    "color": GRAY,
    "stroke_width": 7,
}

#-----------Weight configs-----------
DEFAULT_WEIGHT_ARGS: dict = {
    "color": WHITE,
    "font_size": 34,
    "font": "Javiera"
}

#-----------Label configs-----------
DEFAULT_LABEL_ARGS: dict = {
    "color": BLUE_A,
    "font": "Cascadia Code",
    "font_size": 38
}