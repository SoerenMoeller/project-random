from manim import *
from constants import *

NUMBER_BUFFER = 1
BIG_SMALL_RATIO = 0.2

def create_box(side_length=2):
    animations = {}

    main_box = Square(side_length, z_index=2, fill_opacity=1, fill_color=BACKGROUND_COLOR)
    small_box_left = Square(side_length * BIG_SMALL_RATIO, z_index=2, fill_opacity=1, fill_color=BACKGROUND_COLOR)
    small_box_right = Square(side_length * BIG_SMALL_RATIO, z_index=2, fill_opacity=1, fill_color=BACKGROUND_COLOR)
    box = VGroup(small_box_left, main_box, small_box_right).arrange(RIGHT, center=True, buff=0)  

    animations[CREATE_ANIM] = Create(box)
    animations[OBJECT] = box

    return animations


def add_number_animation(animations, scene, number):
    number_text = Tex(number).next_to(animations[OBJECT], LEFT, buff=NUMBER_BUFFER)
    scene.play(Write(number_text))
    scene.wait(.5)
    scene.play(number_text.animate.move_to(animations[OBJECT][0].get_center()))
    # todo: animate box
    scene.play(number_text.animate.move_to(animations[OBJECT][-1].get_center()))
    scene.wait(.5)
    scene.play(number_text.animate.next_to(animations[OBJECT], RIGHT, buff=NUMBER_BUFFER))
    scene.play(Unwrite(number_text))

    
        