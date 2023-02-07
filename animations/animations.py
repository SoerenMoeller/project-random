from manim import *
from animation_setup.coin_toss import create_coin_toss
from animation_setup.maze_creation import create_maze
from constants import CREATE_BORDER, FADE_IN_ANIM, CREATE_ANIM, PLAY_ANIM, INIT_ROTATION


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


class MazeCreation(Scene):
    def construct(self):
        animations = create_maze()
        self.play(animations[CREATE_BORDER])
        self.play(animations[FADE_IN_ANIM])
        self.play(animations[CREATE_ANIM])
        self.play(animations[PLAY_ANIM])
                

class CoinToss(ThreeDScene):
    def construct(self):
        self.camera.background_color=WHITE
        animations = create_coin_toss()

        self.play(animations[CREATE_ANIM])
        self.play(animations[INIT_ROTATION])
        self.wait(2)

        self.play(animations[PLAY_ANIM])
        self.wait(2)
        self.play(animations[PLAY_ANIM])



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
