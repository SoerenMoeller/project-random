from manim import *
from constants import *

BIG_SMALL_RATIO = 0.2

def create_box(side_length=2):
    animations = {}

    main_box = Square(side_length)
    small_box_left = Square(side_length * BIG_SMALL_RATIO, z_index=2)
    small_box_right = Square(side_length * BIG_SMALL_RATIO, z_index=2)
    box = VGroup(small_box_left, main_box, small_box_right).arrange(RIGHT, center=True, buff=0)  

    animations[CREATE_ANIM] = Create(box)
    animations[OBJECT] = box

    return animations


def add_number_animation(animations, number):
    number_text = Tex(number).next_to(animations[OBJECT][0], LEFT)
    fade_in = Write(number_text)
    move_into_box = number_text.animate.move_to(animations[OBJECT][0].get_center())
    # todo: animate box
    move_in_silent = number_text.animate.move_to(animations[OBJECT][0].get_center())
    move_out_of_box = number_text.animate.next_to(animations[OBJECT][-1], RIGHT)
    fade_out = Unwrite(number_text)
    animations[PLAY_ANIM] = fade_in
    #animations[PLAY_ANIM] = AnimationGroup(fade_in, move_into_box, move_in_silent, move_out_of_box, fade_out, lag_ratio=1)
        