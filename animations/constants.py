from manim import *


OBJECT = "object"
BUG_FIX_FILL = "bug_fix_fill"
BACKGROUND_COLOR = "#292929"

LOWER_FONT_SIZE = 25
BULLET_POINT_SIZE = 31


# constants to access animations
CREATE_BORDER = "create_border"
UNCREATE_BORDER = "uncreate_border"
UNCREATE_WALLS = "uncreate_walls"
FADE_OUT_ANIM = "fade_out_animation"
FADE_IN_ANIM = "fade_in_animation"
CREATE_ANIM = "create_animation"
PLAY_ANIM = "play_animation"
INIT_ROTATION = "initial_rotation"
SHIFT_ANIM = "shift_animation"
SHRINK_ANIM = "shrink_animation"
COIN_HEAD_HEAD_ANIM = "coin_head_head_animation"
COIN_HEAD_TAIL_ANIM = "coin_head_tail_animation"
COIN_TAIL_TAIL_ANIM = "coin_tail_tail_animation"
COIN_TAIL_HEAD_ANIM = "coin_tail_head_animation"


### settings for timing etc
# maze 
MAZE_WIDTH = 3
AMOUNT_OF_CELLS = 2
TRACE_SIZE = 4
TRANSITION_TIME = 0.2
MAZE_POSITION = np.array([-0.5, -0.5, 0])

# coin
COIN_POSITION = np.array([0, 0, 0])
COIN_BIG_SHIFT = DOWN * 2.5
SMALL_SHRINK = .7
SMALL_POSITION = np.array([-5, -1.25, 0])
COIN_SIZE = 0.8
COIN_THICKNESS = COIN_SIZE / 8
GOLD_COLOR = "#FFD700"
DARKER_GOLD_COLOR = "#B59902"
TOSS_TIME = 3