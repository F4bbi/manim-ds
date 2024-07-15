from manim import *

from manim_ds.m_collection.m_stack import *

class Random(Scene):
    def construct(self):
        stack = MStack([1], square_args=PURPLE_SQUARE_ARGS, value_args=DEFAULT_VALUE_ARGS)
        self.play(Create(stack))
        self.play(stack.animate.shift(RIGHT))
        self.play(stack.animate.append('('))
        self.play(stack.animate.scale(0.75))
        self.play(stack.animate.append('a'))
        self.play(stack.animate.append('3'))
        self.wait()
        self.play(stack.container.animate.set_color(RED))
        self.play(stack.animate.shift(LEFT * 2))
        self.play(stack.container.animate.set_color(BLUE))
        self.play(stack.animate.append(8))
        self.play(stack.animate.pop())
        self.play(stack.animate.pop())
        self.play(stack.animate.pop())
        self.play(stack.animate.scale(5))
        self.wait()