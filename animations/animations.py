from manim import *


class Intro(Scene):
    def construct(self):
        cold_opener = Tex("Computer haben einen eigenen Willen.")
        sub_title = Tex("Stimmt das?")
        VGroup(cold_opener, sub_title).arrange(DOWN)

        self.play(Write(cold_opener))
        self.wait(2)
        self.play(FadeIn(sub_title, shift=DOWN))


class Halton(Scene):
    def halton(self, b):
        """Generator function for Halton sequence."""
        n, d = 0, 1
        while True:
            x = d - n
            if x == 1:
                n = 1
                d *= b
            else:
                y = d // b
                while x <= y:
                    y //= b
                n = (b + 1) * y - x
            yield n / d
    
    def construct(self):
        AMOUNT_OF_DOTS = 150
        DELAY = 0.35
        DOT_SIZE = 0.05

        halton_2 = self.halton(2)
        halton_3 = self.halton(3)
        animations = [FadeIn(Dot([next(halton_2) * 10 - 5, next(halton_3) * 10 - 5, 0], radius=DOT_SIZE)) for _ in range(AMOUNT_OF_DOTS)]
        self.play(AnimationGroup(*animations, lag_ratio=DELAY))


class BlackBoxRandom(Scene):
    def construct(self):
        # setup constants
        BOX_SIDE_LENGTH = 4
        BOX_SHIFT_RIGHT = 2.5
        BOX_LEFT_BORDER = BOX_SHIFT_RIGHT - BOX_SIDE_LENGTH / 2
        LINE_LEFT = BOX_LEFT_BORDER - 1
        LINE_TOP = BOX_SIDE_LENGTH / 4
        LINE_BOTTOM = LINE_TOP - BOX_SIDE_LENGTH
        LINE_RIGHT = LINE_LEFT + 3/4 * BOX_SIDE_LENGTH
        TITLE_HEIGHT = 3

        # init view elements
        box = Square(color=BLACK, fill_opacity=1, side_length=BOX_SIDE_LENGTH, stroke_color=WHITE).set_z_index(2)
        line_0 = Line(start=[BOX_LEFT_BORDER, LINE_TOP, 0], end=[LINE_LEFT, LINE_TOP, 0], color=WHITE)
        line_1 = Line(start=[LINE_LEFT, LINE_TOP, 0], end=[LINE_LEFT, LINE_BOTTOM, 0], color=WHITE)
        line_2 = Line(start=[LINE_LEFT, LINE_BOTTOM, 0], end=[LINE_RIGHT, LINE_BOTTOM, 0], color=WHITE)
        line_3 = Arrow(start=[LINE_RIGHT, LINE_BOTTOM, 0], end=[LINE_RIGHT, LINE_BOTTOM + 1, 0], color=WHITE, buff=0)
        dot_0 = Dot([BOX_LEFT_BORDER, LINE_TOP, 0])
        dot_1 = Dot([LINE_LEFT, LINE_TOP, 0])
        dot_1_copy = dot_1.copy()
        dot_2 = Dot([LINE_LEFT, LINE_BOTTOM, 0])
        dot_3 = Dot([LINE_RIGHT, LINE_BOTTOM, 0])
        dot_4 = Dot([LINE_RIGHT, LINE_BOTTOM + 1, 0])
        loop_lines = VGroup(line_0, line_1, line_2, line_3)
        box.add(Text("Black Box").set_z_index(3))

        # show title
        title_element = Tex("Beispiel eines Zufallsgenerators")
        title_element.move_to([0, TITLE_HEIGHT, 0])
        self.play(Write(title_element))
        self.wait(3)

        # shift box and fade in the lines
        self.play(Create(box))
        self.play(box.animate.shift(RIGHT * BOX_SHIFT_RIGHT))
        self.play(Create(loop_lines))
        self.wait(3)

        # shift in the initial seed
        seed = Tex("78")
        seed.move_to([LINE_LEFT, 10, 0])  
        text_y = 1.5
        self.play(seed.animate(run_time=2).shift(DOWN * (10 - text_y)), Create(dot_1))
        self.wait(2)
        seed_text = Tex("Seed:").next_to(seed, LEFT, buff=0.5)
        self.play(Write(seed_text))
        self.wait(3)
        self.play(FadeOut(seed_text))
        self.wait(1)
        
        # setup loop animation
        old_text_elem = seed
        most_right = seed
        NUMBERS_PER_ROW = 5
        numbers = ["12", "9", "47", "15", "78", "12", "9", "47", "15"]
        #numbers = ["12", "9", "47"]

        # first loop
        self.play(seed.animate.shift(LEFT * 6), Transform(dot_1, dot_2))
        self.play(Transform(dot_1, dot_3))
        self.play(Transform(dot_1, dot_4))
        self.play(Transform(dot_1, dot_0), run_time=3)

        # loop animation
        for i in range(len(numbers)):
            text_elem = Tex(numbers[i]).move_to([BOX_LEFT_BORDER, text_y, 0])
            self.play(text_elem.animate.next_to(dot_1_copy, UP), Transform(dot_1, dot_1_copy))

            # check if new row is needed
            if i % NUMBERS_PER_ROW == 0 and i != 0:
                self.play(text_elem.animate.next_to(most_right, DOWN), Transform(dot_1, dot_2))
                most_right = text_elem
            else:
                self.play(text_elem.animate.next_to(old_text_elem, RIGHT, buff=0.5), Transform(dot_1, dot_2))
            old_text_elem = text_elem

            self.play(Transform(dot_1, dot_3))
            self.play(Transform(dot_1, dot_4))
            self.play(Transform(dot_1, dot_0), run_time=3)


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)
        circle.set_fill(PINK, opacity=0.5)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))

class OpeningManim(Scene):
    def construct(self):
        title = Tex(r"This is some \LaTeX")
        basel = MathTex(r"\sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}")
        VGroup(title, basel).arrange(DOWN)
        self.play(
            Write(title),
            FadeIn(basel, shift=DOWN),
        )
        self.wait()

        transform_title = Tex("That was a transform")
        transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(title, transform_title),
            LaggedStart(*[FadeOut(obj, shift=DOWN) for obj in basel]),
        )
        self.wait()

        grid = NumberPlane()
        grid_title = Tex("This is a grid", font_size=72)
        grid_title.move_to(transform_title)

        self.add(grid, grid_title)  # Make sure title is on top of grid
        self.play(
            FadeOut(title),
            FadeIn(grid_title, shift=UP),
            Create(grid, run_time=3, lag_ratio=0.1),
        )
        self.wait()

        grid_transform_title = Tex(
            r"That was a non-linear function \\ applied to the grid"
        )
        grid_transform_title.move_to(grid_title, UL)
        grid.prepare_for_nonlinear_transform()
        self.play(
            grid.animate.apply_function(
                lambda p: p
                          + np.array(
                    [
                        np.sin(p[1]),
                        np.sin(p[0]),
                        0,
                    ]
                )
            ),
            run_time=3,
        )
        self.wait()
        self.play(Transform(grid_title, grid_transform_title))
        self.wait()
