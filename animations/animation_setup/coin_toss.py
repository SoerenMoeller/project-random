from manim import *
import math
from constants import *


"""
Problem: Can not manage to alter the coin sides between the throws, so I have to split it into different animations
"""


CURRENT_DEGREE = 0
TOSS_PITCH = np.array([0, 5.5, 0])


def pow(i, j):
    return int(math.pow(i, j))


def create_coin_toss(heads_up=True, rotate=True, half=False, big_coin=True):
    global COIN_POSITION

    animations = {}
    coin = create_coin(heads_up, rotate)
    animations[OBJECT] = coin

    animations[CREATE_ANIM] = FadeIn(coin, lag_ratio=0)
    if big_coin:
        COIN_POSITION = coin.get_center() - COIN_BIG_SHIFT

        if not rotate:
            animations[SHIFT_ANIM] = coin.animate.shift(COIN_BIG_SHIFT)
            return animations

        coin.shift(COIN_BIG_SHIFT)
        add_toss_animation(animations, coin, half)
        return animations

    COIN_POSITION = SMALL_POSITION
    if not rotate:
        animations[SHRINK_ANIM] = ScaleInPlace(coin, SMALL_SHRINK)
        return animations

    coin.move_to(SMALL_POSITION)
    coin.scale(SMALL_SHRINK)
    add_toss_animation(animations, coin, half)
    
    return animations


def add_toss_animation(animations, coin, half=False):
    # has to be split up, since shift has to happen first
    animations[INIT_ROTATION] = Rotate(coin, angle=PI / 1.5, axis=RIGHT)
    animations[PLAY_ANIM] = create_toss_animation(half, coin)


def create_toss_animation(half, coin):
    global CURRENT_DEGREE
    
    CURRENT_DEGREE = 0
    return UpdateFromAlphaFunc(coin, update_toss_animation_half if half else update_toss_animation, run_time=TOSS_TIME)


def create_coin(heads_up=True, rotate=False):
    circle_1 = Circle(COIN_SIZE, color=BLACK, shade_in_3d=True)
    circle_0 = Circle(COIN_SIZE, color=BLACK, shade_in_3d=True)
    circle_0.move_to(add_offset(COIN_POSITION, COIN_THICKNESS / 2 + .01))
    circle_1.move_to(add_offset(COIN_POSITION, - COIN_THICKNESS / 2 - .01))
    cylinder = Cylinder(radius=COIN_SIZE, height=COIN_THICKNESS, fill_color=GOLD_COLOR, checkerboard_colors=[GOLD_COLOR]) 
    cylinder.move_to(COIN_POSITION)

    # create number
    num_width = COIN_SIZE / 4
    offset_number = np.array([0, 0, COIN_THICKNESS / 2 + 0.02]) if heads_up else np.array([0, 0, -COIN_THICKNESS / 2 - 0.02]) + COIN_POSITION
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
    offset_head = np.array([0, 0, -COIN_THICKNESS / 2 - 0.01]) if heads_up else np.array([0, 0, COIN_THICKNESS / 2 + 0.01]) + COIN_POSITION
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
    head = Polygon(*head_border, shade_in_3d=True, fill_color=DARKER_GOLD_COLOR, fill_opacity=1, color=BLACK)

    if heads_up:
        head.rotate(PI).rotate(PI, axis=UP)
    else:
        number.rotate(PI).rotate(PI, axis=UP)
    
    # create coin
    coin = VGroup(cylinder, circle_0, circle_1, head, number)

    if rotate:
        coin.rotate(PI / 1.5, axis=RIGHT)

    return coin


def update_toss_animation(coin, alpha):
    global CURRENT_DEGREE

    ROTATION = 2 * PI

    if alpha < .5:
        coin.move_to(COIN_POSITION + TOSS_PITCH * alpha * 2)
    else:
        coin.move_to(COIN_POSITION + TOSS_PITCH - TOSS_PITCH * (alpha - .5) * 2)

    to_rotate = ROTATION * alpha - CURRENT_DEGREE
    CURRENT_DEGREE += to_rotate
    coin.rotate(to_rotate, axis=RIGHT)


def update_toss_animation_half(coin, alpha):
    global CURRENT_DEGREE

    ROTATION = 3 * PI

    if alpha < .5:
        coin.move_to(COIN_POSITION + TOSS_PITCH * alpha * 2)
    else:
        coin.move_to(COIN_POSITION + TOSS_PITCH - TOSS_PITCH * (alpha - .5) * 2)

    to_rotate = ROTATION * alpha - CURRENT_DEGREE
    CURRENT_DEGREE += to_rotate
    coin.rotate(to_rotate, axis=RIGHT)


def add_offset(position, offset):
    return position + np.array([0, 0, offset])