from manim import *
from animation_setup.coin_toss import create_coin_toss, add_toss_animation
from animation_setup.maze_creation import create_maze, create_maze_base, create_finished_maze
from animation_setup.determinism_box import create_box, add_number_animation, add_number_animation_parallel
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
        self.play(Write(example_text), run_time=1.5)

        self.wait(1)
        self.play(example_text.animate.to_corner(LEFT + UP), run_time=1.5)


class ShowExamplesCoinInit(ThreeDScene):
    def construct(self):
        self.camera.background_color=BACKGROUND_COLOR
        COLD_OPENER.to_corner(UP + RIGHT)
        example_text = Tex("Anwendungen").to_corner(LEFT + UP)
        self.add(COLD_OPENER, example_text)

        animations = create_coin_toss(heads_up=False, half=True, rotate=False, big_coin=False)
        self.play(animations[CREATE_ANIM])
        self.wait(.8)
        self.play(animations[SHRINK_ANIM])
        self.wait(.8)
        self.play(animations[OBJECT].animate.move_to(SMALL_POSITION))

        self.wait(.8)
        add_toss_animation(animations, animations[OBJECT], half=True)
        self.play(animations[INIT_ROTATION])


def construct_examples_scene(scene):
    scene.camera.background_color=BACKGROUND_COLOR
    COLD_OPENER.to_corner(UP + RIGHT)
    example_text = Tex("Anwendungen").to_corner(LEFT + UP)
    scene.add(COLD_OPENER, example_text)

    return example_text


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
        add_toss_animation(animations, animations[OBJECT], half=True)
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
        add_toss_animation(animations, animations[OBJECT], half=True)
        self.play(animations[PLAY_ANIM])


def construct_coin_scene(scene):
    example_text = construct_examples_scene(scene)
    animations = create_coin_toss(big_coin=False)
    scene.add(animations[OBJECT])

    return animations[OBJECT], example_text


class ShowExamplesMaze(ThreeDScene):
    def construct(self):
        construct_coin_scene(self)

        create_maze_base(self)


class ShowExamplesMazeCreation(ThreeDScene):
    def construct(self):
        construct_coin_scene(self)

        create_maze(self)


class ShowExamplesMazeBullets(ThreeDScene):
    def construct(self):
        print(create_finished_maze(self) == create_maze(self))
        return
        coin, example_text = construct_coin_scene(self)
        borders, outer = create_finished_maze(self)
        self.play(FadeOut(borders[0][0][-1]), FadeOut(borders[-1][-1][1]))

        self.wait(2)

        # now show further bulletspoints
        bullet_points = [
            Tex(r"\textbullet \; Simulationen", font_size=BULLET_POINT_SIZE), Tex(r"\textbullet \; Spiele", font_size=BULLET_POINT_SIZE), 
            Tex(r"\textbullet \; Kryptographie", font_size=BULLET_POINT_SIZE), Tex(r"\textbullet  \; ...", font_size=BULLET_POINT_SIZE)
        ]

        VGroup(*bullet_points).arrange(DOWN, center=True, aligned_edge=LEFT).move_to([4, 0, 0])

        for point in bullet_points:
            self.play(Write(point))
            self.wait(2)

        self.play(FadeOut(coin))
        self.play(AnimationGroup(*[Uncreate(line) for border in borders for lines in border for line in lines]))
        self.play(Uncreate(outer))
        self.play(AnimationGroup(*[Unwrite(point) for point in bullet_points]))
        self.play(Unwrite(example_text))

            
class StrikeOpener(Scene):
    def construct(self):
        self.camera.background_color=BACKGROUND_COLOR
        COLD_OPENER.to_corner(UP + RIGHT)

        self.play(COLD_OPENER.animate.move_to([0, 0, 0]))
        self.wait(1)
        self.play(Transform(COLD_OPENER, COLD_OPENER_STRIKED, replace_mobject_with_target_in_scene=True))
        self.wait(1)
        self.play(COLD_OPENER_STRIKED.animate.to_corner(UP + RIGHT))


class DeterminismInit(Scene):
    def construct(self):
        self.camera.background_color=BACKGROUND_COLOR
        COLD_OPENER_STRIKED.to_corner(UP + RIGHT)
        self.add(COLD_OPENER_STRIKED)

        box, img = create_box()
        self.play(Create(box), FadeIn(img))
        self.wait(1)
        self.play(Wiggle(box), Wiggle(img))
        add_number_animation(box, img, self, 3, 4)


class DeterminismNumbers(Scene):
    def construct(self):
        self.camera.background_color=BACKGROUND_COLOR
        COLD_OPENER_STRIKED.to_corner(UP + RIGHT)
        self.add(COLD_OPENER_STRIKED)

        box, img = create_box()
        self.add(box, img, COLD_OPENER_STRIKED)
        add_number_animation(box, img, self, 4, 9)


class DeterminismExplain(Scene):
    def construct(self):
        self.camera.background_color=BACKGROUND_COLOR
        COLD_OPENER_STRIKED.to_corner(UP + RIGHT)

        box_a, img_a = create_box(BOX_SIZE)
        self.add(box_a, img_a, COLD_OPENER_STRIKED)

        box_b, img_b = create_box(BOX_SIZE * SMALLER_BOX_SHRINK)
        img_b.scale(0.85)
        
        determinism_text = Tex("Determinismus", font_size=MIDDLE_FONT_SIZE)
        determinism_explain = Tex("System, bei dem nur definierte und reproduzierbare Zustände auftreten.", font_size=LOWER_FONT_SIZE)
        VGroup(determinism_text, determinism_explain).arrange(DOWN).move_to([0, 2, 0])
        
        self.play(Write(determinism_text))
        self.wait(1)
        self.play(Write(determinism_explain))
        
        self.wait(1)
        self.play(Unwrite(determinism_text), Unwrite(determinism_explain))

        self.play(ScaleInPlace(box_a, SMALLER_BOX_SHRINK), ScaleInPlace(img_a, .85))
        self.play(box_a.animate.shift(UP * 0.5), img_a.animate.shift(UP * 0.5))

        box_b.shift(DOWN * 2)
        img_b.shift(DOWN * 2)
        self.play(Create(box_b), FadeIn(img_b)) 


class DeterminismComparison(Scene):
    def construct(self):
        self.camera.background_color=BACKGROUND_COLOR
        COLD_OPENER_STRIKED.to_corner(UP + RIGHT)

        box_a, img_a = create_box(BOX_SIZE * SMALLER_BOX_SHRINK)
        img_a.scale(.85)
        box_a.shift(UP * 0.5)
        img_a.shift(UP * 0.5)
        box_b, img_b = create_box(BOX_SIZE * SMALLER_BOX_SHRINK)
        box_b.shift(DOWN * 2)
        img_b.shift(DOWN * 2)
        img_b.scale(.85)
        self.add(box_a, img_a, box_b, img_b, COLD_OPENER_STRIKED)
        
        determinsm_text = Tex("Determinismus", font_size=MIDDLE_FONT_SIZE).next_to(box_a, LEFT, buff=3)
        non_determinism_text = Tex("Nichtdeterminismus", font_size=MIDDLE_FONT_SIZE).next_to(box_b, LEFT, buff=3)

        self.play(Write(determinsm_text), Write(non_determinism_text))

        self.play(Wiggle(box_a), Wiggle(img_a), Wiggle(box_b), Wiggle(img_b))


class DeterminismComparisonNumbers4(Scene):
    def construct(self):
        self.camera.background_color=BACKGROUND_COLOR
        COLD_OPENER_STRIKED.to_corner(UP + RIGHT)

        box_a, img_a = create_box(BOX_SIZE * SMALLER_BOX_SHRINK)
        img_a.scale(.85)
        box_a.shift(UP * 0.5)
        img_a.shift(UP * 0.5)
        box_b, img_b = create_box(BOX_SIZE * SMALLER_BOX_SHRINK)
        box_b.shift(DOWN * 2)
        img_b.shift(DOWN * 2)
        img_b.scale(.85)
        self.add(box_a, img_a, box_b, img_b, COLD_OPENER_STRIKED)
        
        determinsm_text = Tex("Determinismus", font_size=MIDDLE_FONT_SIZE).next_to(box_a, LEFT, buff=3)
        non_determinism_text = Tex("Nichtdeterminismus", font_size=MIDDLE_FONT_SIZE).next_to(box_b, LEFT, buff=3)

        self.add(determinsm_text, non_determinism_text)
        add_number_animation_parallel(self, box_a, box_b, img_a, img_b, 4, 9, 3)


class DeterminismFadeOut(Scene):
    def construct(self):
        self.camera.background_color=BACKGROUND_COLOR
        COLD_OPENER_STRIKED.to_corner(UP + RIGHT)

        box_a, img_a = create_box(BOX_SIZE * SMALLER_BOX_SHRINK)
        img_a.scale(.85)
        box_a.shift(UP * 0.5)
        img_a.shift(UP * 0.5)
        box_b, img_b = create_box(BOX_SIZE * SMALLER_BOX_SHRINK)
        img_b.scale(.85)
        box_b.shift(DOWN * 2)
        img_b.shift(DOWN * 2)
        
        determinsm_text = Tex("Determinismus", font_size=MIDDLE_FONT_SIZE).next_to(box_a, LEFT, buff=3)
        non_determinism_text = Tex("Nichtdeterminismus", font_size=MIDDLE_FONT_SIZE).next_to(box_b, LEFT, buff=3)
        self.add(box_a, img_a, box_b, img_b, determinsm_text, non_determinism_text, COLD_OPENER_STRIKED)

        self.play(Unwrite(determinsm_text), Unwrite(non_determinism_text))
        self.play(Uncreate(box_a), Uncreate(box_b), FadeOut(img_a), FadeOut(img_b))

        self.wait(.5)

        computer_text = Tex("Computer sind deterministisch.").shift(UP * .5)
        self.play(Write(computer_text))
        self.play(COLD_OPENER_STRIKED.animate.next_to(computer_text, DOWN))
        COLD_OPENER.move_to(COLD_OPENER_STRIKED.get_center())

        self.play(Transform(COLD_OPENER_STRIKED, COLD_OPENER, replace_mobject_with_target_in_scene=True))
        self.wait(.5)
        self.play(
            Unwrite(computer_text),
            COLD_OPENER.animate.to_corner(UP + RIGHT)
        )


class BlackBoxRandom(Scene):
    def construct(self):
        self.camera.background_color=BACKGROUND_COLOR
        COLD_OPENER.to_corner(UP + RIGHT)
        self.add(COLD_OPENER)

        # setup constants
        BOX_SIDE_LENGTH = 4
        BOX_SHIFT_RIGHT = 2.5
        BOX_LEFT_BORDER = BOX_SHIFT_RIGHT - BOX_SIDE_LENGTH / 2
        LINE_LEFT = BOX_LEFT_BORDER - 1
        LINE_TOP = BOX_SIDE_LENGTH / 4
        LINE_BOTTOM = LINE_TOP - BOX_SIDE_LENGTH
        LINE_RIGHT = LINE_LEFT + 3/4 * BOX_SIDE_LENGTH

        # init view elements
        box = Square(color=BACKGROUND_COLOR, fill_opacity=1, side_length=BOX_SIDE_LENGTH, stroke_color=WHITE).set_z_index(2)
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

        # show title
        title_element = Tex("Beispiel eines Zufallsgenerators", font_size=MIDDLE_FONT_SIZE)
        title_element.to_corner(UP + LEFT)
        self.play(Write(title_element))
        self.wait(3)

        # shift box and fade in the lines
        img = ImageMobject("clipart64533.png", z_index=3).move_to(box.get_center()).scale(.5)
        self.play(Create(box), FadeIn(img))
        self.play(box.animate.shift(RIGHT * BOX_SHIFT_RIGHT), img.animate.shift(RIGHT * BOX_SHIFT_RIGHT))
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
        numbers = ["12", "9", "47", "12", "15", "67", "16", "7", "45", "11"]
        #numbers = ["12", "9", "47"]

        # first loop
        self.play(seed.animate.shift(LEFT * 6), Transform(dot_1, dot_2))
        self.play(Transform(dot_1, dot_3))
        self.play(Transform(dot_1, dot_4))
        self.play(Transform(dot_1, dot_0), Rotate(img, axis=IN), run_time=3)

        # loop animation
        texts = []
        for i in range(len(numbers)):
            text_elem = Tex(numbers[i]).move_to([BOX_LEFT_BORDER, text_y, 0])
            texts.append(text_elem)
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
            self.play(Transform(dot_1, dot_0), Rotate(img, axis=IN), run_time=3)
        
        self.play(Uncreate(loop_lines), FadeOut(dot_1))
        self.play(Uncreate(box), *[Unwrite(text) for text in texts], Unwrite(title_element), FadeOut(img), Unwrite(seed))


class AdditionalInformation(Scene):
    def construct(self):
        self.camera.background_color=BACKGROUND_COLOR
        COLD_OPENER.to_corner(UP + RIGHT)
        self.add(COLD_OPENER)

        challenges = Tex("Anforderungen und Verfahren", font_size=BULLET_POINT_SIZE).to_corner(UP + LEFT).shift(DOWN * 1.5)
        challenge_1 = Tex(r"\textbullet \; Keine Wiederholungen", font_size=MIDDLE_FONT_SIZE)
        challenge_2 = Tex(r"\textbullet \; Keine Vorraussagen möglich", font_size=MIDDLE_FONT_SIZE)
        challenge_3 = Tex(r"\textbullet \; Lineare Kongruenzmethode", font_size=MIDDLE_FONT_SIZE)
        challenge_4 = Tex(r"\textbullet \; Linear rückgekoppeltes Schieberegister", font_size=MIDDLE_FONT_SIZE)
        VGroup(challenges, challenge_1, challenge_2, challenge_3, challenge_4).arrange(DOWN, center=False, aligned_edge=LEFT, buff=.7)  

        self.play(Write(challenges))
        self.wait(1)
        self.play(Write(challenge_1))
        self.wait(3)
        self.play(Write(challenge_2))
        self.wait(3)
        self.play(Write(challenge_3))
        self.wait(3)
        self.play(Write(challenge_4))
        self.wait(3)

        seed = Tex("Seed", font_size=BULLET_POINT_SIZE).to_corner(UP + RIGHT).shift(DOWN * 1.5 + LEFT * 4.5)
        seed_1 = Tex(r"\textbullet \; Eingangswert des Zufallsgenerators", font_size=MIDDLE_FONT_SIZE)
        seed_2 = Tex(r"\textbullet \; Erzeugt Reproduzierbarkeit", font_size=MIDDLE_FONT_SIZE)
        seed_3 = Tex(r"\textbullet \; Mausposition", font_size=MIDDLE_FONT_SIZE)
        seed_4 = Tex(r"\textbullet \; Uhrzeit", font_size=MIDDLE_FONT_SIZE)
        VGroup(seed, seed_1, seed_2, seed_3, seed_4).arrange(DOWN, center=False, aligned_edge=LEFT, buff=.7)  

        self.play(Write(seed))
        self.wait(1)
        self.play(Write(seed_1))
        self.wait(3)
        self.play(Write(seed_2))
        self.wait(3)
        self.play(Write(seed_3))
        cursor = get_cursor().scale(.1).next_to(seed_3)
        self.play(Create(cursor))
        self.play(cursor.animate.shift(RIGHT + DOWN))
        self.wait(3)
        self.play(Write(seed_4))
        self.wait(3)

        self.play(
            Unwrite(seed), Unwrite(seed_1), Unwrite(seed_2), Unwrite(seed_3), Unwrite(seed_4),
            Unwrite(challenges), Unwrite(challenge_1), Unwrite(challenge_2), Unwrite(challenge_3), Unwrite(challenge_4), Uncreate(cursor)
        )

        final_question = Tex("Reicht dieser Zufall?", font_size=BULLET_POINT_SIZE).to_corner(UP).shift(DOWN * 1.5, LEFT)
        answer_1 = Tex(r"\textbullet \; Reproduzierbarkeit von Abläufen", font_size=MIDDLE_FONT_SIZE)
        answer_2 = Tex(r"\textbullet \; Analyse von Spezialfällen", font_size=MIDDLE_FONT_SIZE)
        answer_3 = Tex(r"\textbullet \; Sicherheitsrisiko", font_size=MIDDLE_FONT_SIZE)
        answer_4 = Tex(r"\textbullet \; Echter Zufall braucht zusätzliche Hardware", font_size=MIDDLE_FONT_SIZE)
        VGroup(final_question, answer_1, answer_2, answer_3, answer_4).arrange(DOWN, center=False, aligned_edge=LEFT, buff=.7)

        self.play(Write(final_question))
        self.wait(1)
        self.play(Write(answer_1))
        self.wait(3)
        self.play(Write(answer_2))
        self.wait(3)
        self.play(Write(answer_3))
        self.wait(3)
        self.play(Write(answer_4))
        self.wait(3)  

        self.play(Unwrite(final_question), Unwrite(answer_1), Unwrite(answer_2), Unwrite(answer_3), Unwrite(answer_4))
        self.wait(1)

        self.play(COLD_OPENER.animate.move_to([0, 0, 0]))
        pseudo = Tex("Computer können Pseudo-Zufall")
        self.play(Transform(COLD_OPENER, pseudo))

        self.wait(2)
        self.play(Unwrite(COLD_OPENER))


class Test(Scene):
    def construct(self):
        cursor_points = [
            [0, 0, 0],
            [0, -3, 0],
            [.8, -2.2, 0],
            [1.2, -3, 0],
            [1.6, -2.8, 0],
            [1.3, -2, 0],
            [2.2, -1.9, 0]
        ]

        cursor = Polygon(*cursor_points, stroke_color=WHITE, color=WHITE)
        self.add(cursor)

def get_cursor():
        cursor_points = [
            [0, 0, 0],
            [0, -3, 0],
            [.8, -2.2, 0],
            [1.2, -3, 0],
            [1.6, -2.8, 0],
            [1.3, -2, 0],
            [2.2, -1.9, 0]
        ]

        return Polygon(*cursor_points, stroke_color=WHITE, color=WHITE)
