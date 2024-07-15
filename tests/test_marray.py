from manim import *

from manim_ds.m_collection.m_array import *

class RandomOperations(Scene):
    def construct(self):
        arr = [1, 2, 3]
        mArray = (
            MArray(arr, RIGHT, PURPLE_SQUARE_ARGS)
            .add_indexes(DOWN, index_args=PURPLE_INDEX_ARGS)
            .add_label(Text("Arr", **DEFAULT_LABEL_ARGS), DOWN)
        )
        mArray.shift(UP * 1.5 + LEFT * 4)
        self.play(Create(mArray))
        self.play(mArray.animate.append(4))
        self.play(mArray.animate.append(5))
        self.play(mArray.animate.scale(0.5))
        self.play(mArray.animate.append(6))
        self.play(mArray.animate.append(7))
        self.play(mArray.animate.pop(0))
        self.play(mArray.animate.shift(RIGHT))
        self.play(mArray.animate.pop(2))
        self.play(mArray[0].value.animate.set_fill(RED))
        self.play(mArray[0].index.animate.set_fill(RED))
        self.play(mArray.animate.swap(0, 3, path_arc=PI/2))
        self.play(mArray[0].value.animate.set_fill(RED))
        self.play(mArray[0].index.animate.set_fill(RED))
        self.wait(1)