from manim import *
from math import cos, sin


class Intro(Scene):
    def construct(self):
        cold_opener = Tex("Computer können keinen Zufall")
        sub_title = Tex("Wie kann das sein?")
        VGroup(cold_opener, sub_title).arrange(DOWN)

        # write title
        self.wait(1)
        self.play(Write(cold_opener))
        self.wait(2)
        self.play(Write(sub_title))
        self.wait(3)

        # keep title at top
        self.play(
            cold_opener.animate.to_corner(UP + RIGHT),
            FadeOut(sub_title)
        )
        self.wait(1)

        # declare typical use cases


        self.wait(5)


class Test(ThreeDScene):
    def construct(self):
        # bug when using cashed data
        config.flush_cache = True
        self.camera.background_color=WHITE

        COIN_POSITION = np.array([0, 0, 0])
        COIN_SIZE = 0.5
        COIN_THICKNESS = COIN_SIZE / 8
        AMOUNT_OF_EDGES = 10
        GOLD_COLOR = "#FFD700"
        DARKER_GOLD_COLOR = "#B59902"

        # create top and bottom of the coin
        circle_1 = Circle(COIN_SIZE, color=BLACK, fill_color=GOLD_COLOR, fill_opacity= 1, shade_in_3d=True)
        circle_0 = Circle(COIN_SIZE, color=BLACK, fill_color=GOLD_COLOR, fill_opacity= 1, shade_in_3d=True)
        circle_0.move_to(add_offset(COIN_POSITION, COIN_THICKNESS / 2))
        circle_1.move_to(add_offset(COIN_POSITION, - COIN_THICKNESS / 2))

        # create number
        num_width = COIN_SIZE / 4
        offset_number = np.array([0, 0, COIN_THICKNESS / 2 + 0.01]) + COIN_POSITION
        num_border = [
            np.array([-num_width / 2, -COIN_SIZE * 3/8, 0]) + offset_number,
            np.array([num_width / 2, -COIN_SIZE * 3/8, 0]) + offset_number,
            np.array([num_width / 2, COIN_SIZE * 3/8, 0]) + offset_number,
            np.array([-num_width / 2, COIN_SIZE * 3/8, 0]) + offset_number,
            np.array([-num_width, COIN_SIZE * 3/8 - num_width / 2, 0]) + offset_number,
            np.array([-num_width / 2, COIN_SIZE * 3/8 - num_width, 0]) + offset_number
        ]
        number = Polygon(*num_border, shade_in_3d=True, fill_color=DARKER_GOLD_COLOR, fill_opacity=1, color=BLACK)

        # create head
        offset_head = np.array([0, 0, -COIN_THICKNESS / 2 - 0.01]) + COIN_POSITION
        head_border = [
            np.array([-1/5 * COIN_SIZE, -3/8 * COIN_SIZE, 0]) + offset_head,
            np.array([-1/5 * COIN_SIZE, -2/8 * COIN_SIZE, 0]) + offset_head,
            np.array([-2/5 * COIN_SIZE, -1/8 * COIN_SIZE, 0]) + offset_head,
            np.array([-2/5 * COIN_SIZE, 1/8 * COIN_SIZE, 0]) + offset_head,
            np.array([0, 3/8 * COIN_SIZE, 0]) + offset_head,
            np.array([3/10 * COIN_SIZE, 3/16 * COIN_SIZE, 0]) + offset_head,
            np.array([3/10 * COIN_SIZE, -1/8 * COIN_SIZE, 0]) + offset_head,
            np.array([1/5 * COIN_SIZE, -2/8 * COIN_SIZE, 0]) + offset_head,
            np.array([1/5 * COIN_SIZE, -3/8 * COIN_SIZE, 0]) + offset_head
        ]
        head = Polygon(*head_border, shade_in_3d=True, fill_color=DARKER_GOLD_COLOR, fill_opacity=1, color=BLACK).rotate(PI).rotate(PI, axis=UP)
        
        # create side pieces, determine points first, use angles for that 
        step = PI / AMOUNT_OF_EDGES
        degree = 0
        left = []
        right = []
        while degree < PI:
            # left side
            vector = [- sin(degree), - cos(degree), 0]
            vector_normalized = vector / np.linalg.norm(vector)
            position = vector_normalized * COIN_SIZE
            left.append(position)

            # right side
            vector = [sin(degree), cos(degree), 0]
            vector_normalized = vector / np.linalg.norm(vector)
            position = vector_normalized * COIN_SIZE
            right.append(position)

            degree += step
        positions = left + right

        # create squares between the positions
        borders = []
        for i in range(len(positions)):
            current = i
            next = i + 1 if i != len(positions) - 1 else 0

            square_pos = [
                add_offset(positions[current], COIN_THICKNESS / 2),
                add_offset(positions[current], -COIN_THICKNESS / 2),
                add_offset(positions[next], -COIN_THICKNESS / 2),
                add_offset(positions[next], COIN_THICKNESS / 2),
            ]

            borders.append(Polygon(*square_pos, color=BLACK, fill_color=GOLD_COLOR, fill_opacity=1, shade_in_3d=True))


        # init coin
        container = VGroup(head, number, circle_0, circle_1, *borders)

        # start anim
        height = 0.25
        rotation = PI / 4
        toss_time = 1
        toss_func = rate_functions.ease_in_out_sine
        self.play(
            UpdateFromAlphaFunc(
                container, 
                lambda coin, alpha: coin.shift(height * UP * alpha).rotate(rotation * alpha, axis=RIGHT),
                run_time=toss_time,
                rate_func=toss_func 
            )
        )
        self.play(
            UpdateFromAlphaFunc(
                container, 
                lambda coin, alpha: coin.shift(height * DOWN * alpha).rotate(rotation * alpha, axis=RIGHT),
                run_time=toss_time,
                rate_func=toss_func 
            )
        )
        



def update_toss_animation(coin, alpha):
    coin.restore()
    coin.become(
        coin.shift(interpolate)
    )


def add_offset(position, offset):
    return position + np.array([0, 0, offset])


class LavaLamp(Scene):
    def construct(self):
        title = Tex(r"Wie wird echter Zufall simuliert?")
        VGroup(title).arrange(DOWN)

        self.play(
            Write(title),
        )
        self.wait()

        transform_title = Tex("Lavalampen")
        transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(title, transform_title),
        )

        object_lamp = create_lamp()
        height_first_row = 2
        self.play(Create(object_lamp))
        self.wait(3)
        self.play(ScaleInPlace(object_lamp, 0.2))
        self.play(object_lamp.animate.move_to([-6, height_first_row, 0]))

        amount_of_lamps = 26
        row_offset = 1.25

        # -6, -4.5, -3, -1.5, 0, 1.5, 3, 4.5, 6

        lamps = [create_lamp(2).scale(0.2) for _ in range(amount_of_lamps)]
        self.add(*lamps)
        x = -4.5
        y = 2
        test = []
        for lamp in lamps:
            test.append(lamp.animate(run_time=2).move_to([x, y, 0]))
            x += 1.5
            if x > 6:
                x = -6
                y -= row_offset

        self.play(*test, lag_ratio=0.0)        
        self.wait()
    
def create_lamp(offset=0):
    lamp_part_one = [
                [3, 2, 0],
                [3.5, 4, 0],
                [2.75, 7, 0],
                [1.25, 7, 0],
                [0.5, 4, 0],
                [1, 2, 0],
            ]
    lamp_part_two = [
                [0, 0, 0],  # Untere Teil 2
                [4, 0, 0],
                [3, 2, 0],
                [1, 2, 0]
            ]
    lamp_part_three = [
                [1.25, 7, 0],
                [2.75, 7, 0],
                [2.5, 8, 0],
                [1.5, 8, 0]
    ]
    lamp_one = Polygon(*lamp_part_one, color=WHITE)
    lamp_two = Polygon(*lamp_part_two, color=WHITE, fill_color=GRAY_D)
    lamp_three = Polygon(*lamp_part_three, stroke_color=WHITE, fill_color=GRAY_D)
    lamp_one.scale(0.5).center().shift(DOWN * offset)
    lamp_two.scale(0.5).next_to(lamp_one, DOWN, buff=0)
    lamp_three.scale(0.5).next_to(lamp_one, UP, buff=0)
    
    return VGroup(lamp_one, lamp_two, lamp_three)


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
