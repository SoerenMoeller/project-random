from manim import *
from animation_setup.coin_toss import create_coin_toss, add_toss_animation
from animation_setup.maze_creation import create_maze
from animation_setup.determinism_box import create_box, add_number_animation
from constants import *


TEMPLATE = TexTemplate()
TEMPLATE.add_to_preamble(r"\usepackage{ulem}")
COLD_OPENER = Tex("Computer können keinen Zufall")
COLD_OPENER_STRIKED = Tex("\sout{Computer können keinen Zufall}", tex_template=TEMPLATE)


class Intro(Scene):
    def construct(self):
        self.camera.background_color=BACKGROUND_COLOR

        sub_title = Tex("Wie kann das sein?")
        VGroup(COLD_OPENER, sub_title).arrange(DOWN)

        # write title
        self.wait(1)
        self.play(Write(COLD_OPENER))
        self.wait(2)
        self.play(Write(sub_title))
        self.wait(3)

        # keep title at top
        self.play(
            COLD_OPENER.animate.to_corner(UP + RIGHT),
            FadeOut(sub_title)
        )


class IntroduceRandomness(ThreeDScene):
    def construct(self):
        self.camera.background_color=BACKGROUND_COLOR

        COLD_OPENER.to_corner(UP + RIGHT)
        self.add(COLD_OPENER)

        randomness_text = Tex("Was ist Zufall?")
        answer_in_place = Tex("Ein Ereignis, dessen Ausgang nicht vorhersehbar ist.", font_size=LOWER_FONT_SIZE)
        self.play(Write(randomness_text)) 
        self.play(randomness_text.animate.to_corner(UP + LEFT))       
        VGroup(randomness_text, answer_in_place).to_corner(UP + LEFT).arrange(DOWN, center=False, aligned_edge=LEFT, buff=0.8)  

        self.wait(3)
        answer = Tex("Ein Ereignis, dessen Ausgang nicht vorhersehbar ist.")
        self.play(Write(answer))

        self.wait(1)
        self.play(Transform(answer, answer_in_place))

        # introduce coin toss
        animations = create_coin_toss(rotate=False)

        self.play(animations[CREATE_ANIM])
        self.play(animations[SHIFT_ANIM])

        add_toss_animation(animations, animations[OBJECT])
        self.play(animations[INIT_ROTATION])


def construct_randomness_scene(scene):
    scene.camera.background_color=BACKGROUND_COLOR
    COLD_OPENER.to_corner(UP + RIGHT)
    randomness_text = Tex("Was ist Zufall?")
    answer_in_place = Tex("Ein Ereignis, dessen Ausgang nicht vorhersehbar ist.", font_size=LOWER_FONT_SIZE)
    randomness_text.to_corner(UP + LEFT)
    VGroup(randomness_text, answer_in_place).to_corner(UP + LEFT).arrange(DOWN, center=False, aligned_edge=LEFT, buff=.8)  
    scene.add(COLD_OPENER, randomness_text, answer_in_place)

    return randomness_text, answer_in_place


class IntroduceRandomnessHeadHead(ThreeDScene):
    def construct(self):
        construct_randomness_scene(self)

        animations = create_coin_toss()
        self.play(animations[PLAY_ANIM])


class IntroduceRandomnessHeadTail(ThreeDScene):
    def construct(self):
        construct_randomness_scene(self)

        animations = create_coin_toss(half=True)
        self.play(animations[PLAY_ANIM])


class IntroduceRandomnessTailTail(ThreeDScene):
    def construct(self):
        construct_randomness_scene(self)

        animations = create_coin_toss(heads_up=False)
        self.play(animations[PLAY_ANIM])


class IntroduceRandomnessTailHead(ThreeDScene):
    def construct(self):
        construct_randomness_scene(self)

        animations = create_coin_toss(heads_up=False, half=True)
        self.play(animations[PLAY_ANIM])


class RemoveRandomness(ThreeDScene):
    def construct(self):
        randomness_text, answer = construct_randomness_scene(self)

        animations = create_coin_toss()
        self.play(FadeOut(animations[OBJECT]), Unwrite(randomness_text), Unwrite(answer))


class ShowExamplesInit(ThreeDScene):
    def construct(self):
        self.camera.background_color=BACKGROUND_COLOR
        COLD_OPENER.to_corner(UP + RIGHT)
        self.add(COLD_OPENER)

        example_text = Tex("Anwendungen")
        self.play(Write(example_text))

        self.wait(1)
        self.play(example_text.animate.to_corner(LEFT + UP))


class ShowExamplesCoinInit(ThreeDScene):
    def construct(self):
        self.camera.background_color=BACKGROUND_COLOR
        COLD_OPENER.to_corner(UP + RIGHT)
        example_text = Tex("Anwendungen").to_corner(LEFT + UP)
        self.add(COLD_OPENER, example_text)

        animations = create_coin_toss(heads_up=False, half=True, rotate=False, big_coin=False)
        self.play(animations[CREATE_ANIM])
        self.play(animations[SHRINK_ANIM])
        self.play(animations[OBJECT].animate.move_to(SMALL_POSITION))

        add_toss_animation(animations, animations[OBJECT], half=True)
        self.play(animations[INIT_ROTATION])
        self.play(animations[PLAY_ANIM])


def construct_examples_scene(scene):
    scene.camera.background_color=BACKGROUND_COLOR
    COLD_OPENER.to_corner(UP + RIGHT)
    example_text = Tex("Anwendungen").to_corner(LEFT + UP)
    scene.add(COLD_OPENER, example_text)


class ShowExamplesCoinHeadHead(ThreeDScene):
    def construct(self):
        construct_examples_scene(self)

        animations = create_coin_toss(big_coin=False)
        add_toss_animation(animations, animations[OBJECT])
        self.play(animations[PLAY_ANIM])


class ShowExamplesCoinHeadTail(ThreeDScene):
    def construct(self):
        construct_examples_scene(self)

        animations = create_coin_toss(half=True, big_coin=False)
        add_toss_animation(animations, animations[OBJECT])
        self.play(animations[PLAY_ANIM])


class ShowExamplesCoinTailTail(ThreeDScene):
    def construct(self):
        construct_examples_scene(self)

        animations = create_coin_toss(heads_up=False, big_coin=False)
        add_toss_animation(animations, animations[OBJECT])
        self.play(animations[PLAY_ANIM])


class ShowExamplesCoinTailHead(ThreeDScene):
    def construct(self):
        construct_examples_scene(self)

        animations = create_coin_toss(heads_up=False, half=True, big_coin=False)
        add_toss_animation(animations, animations[OBJECT])
        self.play(animations[PLAY_ANIM])


def construct_coin_scene(scene):
    construct_examples_scene(scene)
    animations = create_coin_toss(big_coin=False)
    scene.add(animations[OBJECT])

    return animations[OBJECT]


class ShowExamplesMaze(ThreeDScene):
    def construct(self):
        construct_coin_scene(self)

        animations = create_maze(self)
        self.play(animations[CREATE_BORDER])
        self.play(animations[FADE_IN_ANIM])
        self.play(animations[CREATE_ANIM])


class ShowExamplesMazeCreation(ThreeDScene):
    def construct(self):
        coin = construct_coin_scene(self)

        animations = create_maze(self)
        self.play(animations[PLAY_ANIM])

        self.wait(1)

        # now show further bulletspoints
        bullet_points = [
            Tex(r"\textbullet \; Simulationen", font_size=BULLET_POINT_SIZE), Tex(r"\textbullet \; Spiele", font_size=BULLET_POINT_SIZE), 
            Tex(r"\textbullet \; Kryptographie", font_size=BULLET_POINT_SIZE), Tex(r"\textbullet  \; ...", font_size=BULLET_POINT_SIZE)
        ]

        VGroup(*bullet_points).arrange(DOWN, center=True, aligned_edge=LEFT).move_to([4, 0, 0])

        for point in bullet_points:
            self.play(Write(point))

        self.wait(2)

        # destroy scene
        self.play(FadeOut(coin), *[Unwrite(point) for point in bullet_points])
        self.play(animations[UNCREATE_WALLS])
        self.play(animations[BUG_FIX_FILL])

            
class StrikeOpener(Scene):
    def construct(self):
        self.camera.background_color=BACKGROUND_COLOR
        COLD_OPENER.to_corner(UP + RIGHT)

        self.play(COLD_OPENER.animate.move_to([0, 0, 0]))
        self.wait(1)
        self.play(Transform(COLD_OPENER, COLD_OPENER_STRIKED))
        self.wait(1)
        self.play(COLD_OPENER_STRIKED.animate.to_corner(UP + RIGHT))


class DeterminismInit(Scene):
    def construct(self):
        self.camera.background_color=BACKGROUND_COLOR
        COLD_OPENER_STRIKED.to_corner(UP + RIGHT)

        animations = create_box()
        self.play(animations[CREATE_ANIM])

        add_number_animation(animations, 3)
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
