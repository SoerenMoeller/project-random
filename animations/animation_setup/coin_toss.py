from manim import *
from random import randrange, choice
import math
from itertools import chain
from constants import CREATE_BORDER, FADE_IN_ANIM, CREATE_ANIM, PLAY_ANIM, INIT_ROTATION


CURRENT_DEGREE = 0


def pow(i, j):
    return int(math.pow(i, j))


def create_maze():
    """
    Create a maze and returns animations
    """
    TOTAL_SIZE = 6
    MAZE_SIZE = 4
    CELL_SIZE = TOTAL_SIZE / MAZE_SIZE
    TRACE_SIZE = 4
    TRANSITION_TIME = 0.2
    animations = {}
    
    # binary digits: upper, right, below, left, visited - where directions declare a wall being present
    maze = [[0b11110 for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]
    row = randrange(len(maze))
    col = randrange(len(maze))
    maze[row][col] += pow(2, 0) # marks as visited
    stack = [(row, col)]

    # init visualization
    border = Square(MAZE_SIZE * CELL_SIZE + 0.5, fill_color=BLACK)
    animations[CREATE_BORDER] = Create(border)
    maze_visual = [[Square(CELL_SIZE, fill_opacity=1, fill_color=BLACK, stroke_width=0) for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]
    maze_visual_group = VGroup(*list(chain.from_iterable(maze_visual))).arrange_in_grid(MAZE_SIZE, MAZE_SIZE, buff=0)

    # create the lines
    maze_visual_borders = []
    for i in range(MAZE_SIZE):
        for j in range(MAZE_SIZE):
            center_front = maze_visual[i][0].get_center()
            center_back = maze_visual[i][-1].get_center()
            line = Line(center_front + [-CELL_SIZE / 2, CELL_SIZE / 2, 0], center_back + [CELL_SIZE / 2, CELL_SIZE / 2, 0])
            maze_visual_borders.append(line)
            if i == MAZE_SIZE - 1:
                line = Line(center_front + [-CELL_SIZE / 2, -CELL_SIZE / 2, 0], center_back + [CELL_SIZE / 2, -CELL_SIZE / 2, 0])
                maze_visual_borders.append(line)
            
            center_left = maze_visual[0][i].get_center()
            center_right = maze_visual[-1][i].get_center()
            line = Line(center_left + [-CELL_SIZE / 2, CELL_SIZE / 2, 0], center_right + [-CELL_SIZE / 2, -CELL_SIZE / 2, 0])
            maze_visual_borders.append(line)
            if i == MAZE_SIZE - 1:
                line = Line(center_left + [CELL_SIZE / 2, CELL_SIZE / 2, 0], center_right + [CELL_SIZE / 2, -CELL_SIZE / 2, 0])
                maze_visual_borders.append(line)

    init_borders = [Create(border) for elems in list(chain.from_iterable(maze_visual_borders)) for border in elems]
    animations[FADE_IN_ANIM] = FadeIn(maze_visual_group)
    animations[CREATE_ANIM] = AnimationGroup(*init_borders, lag_ratio=.05)
    
    trace = []
    transition_animations = []
    while stack:
        row, col = stack.pop()
        maze_visual = [[Square(CELL_SIZE, fill_opacity=1, fill_color=BLACK, stroke_width=0) for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]
        
        # draw last active cells
        for old_row, old_col in trace:
            maze_visual[old_row][old_col].set_fill_color(MAROON)
        if len(trace) == TRACE_SIZE:
            trace.pop(0)
        trace.append((row, col))
        maze_visual[row][col].set_fill_color(MAROON_E)
        
        # draw new lines
        maze_group = VGroup(*list(chain.from_iterable(maze_visual))).arrange_in_grid(MAZE_SIZE, MAZE_SIZE, buff=0)
        maze_visual_borders = []
        for i, maze_row in enumerate(maze_visual):
            maze_visual_borders.append([])
            for j, elem in enumerate(maze_row):
                center = elem.get_center()
                corners = [
                    center + [-CELL_SIZE / 2, CELL_SIZE / 2, 0], 
                    center + [CELL_SIZE / 2, CELL_SIZE / 2, 0], 
                    center + [CELL_SIZE / 2, -CELL_SIZE / 2, 0], 
                    center + [-CELL_SIZE / 2, -CELL_SIZE / 2, 0]
                ]
                lines = []

                # only draw the visible lines
                if maze[i][j] & 0b10000:
                    lines.append(Line(start=corners[0], end=corners[1]))
                if maze[i][j] & 0b01000:
                    lines.append(Line(start=corners[1], end=corners[2]))
                if maze[i][j] & 0b00100:
                    lines.append(Line(start=corners[2], end=corners[3]))
                if maze[i][j] & 0b00010:
                    lines.append(Line(start=corners[3], end=corners[0]))
                maze_visual_borders[-1].append(lines)
        borders = VGroup(*[line for i in maze_visual_borders for j in i for line in j])
        transition_animations.append(AnimationGroup(FadeIn(maze_group), FadeIn(borders), run_time=TRANSITION_TIME))

        # choose possible neigbors (coordinates and if they are not visited yet)
        possible_neighbours = [(row, col - 1), (row, col + 1), (row + 1, col), (row - 1, col)]
        possible_neighbours = [(new_row, new_col) for new_row, new_col in possible_neighbours if 0 <= new_row < MAZE_SIZE and 0 <= new_col < MAZE_SIZE and maze[new_row][new_col] % 2 == 0]
        if not possible_neighbours:
            continue

        # remove borders in logic
        stack.append((row, col))
        new_row, new_col = choice(possible_neighbours)
        if row == new_row:
            if col < new_col:
                # remove right of current one
                maze[row][col] -= pow(2, 3)
                maze[new_row][new_col] -= pow(2, 1)
            else:
                # remove left of current one
                maze[row][col] -= pow(2, 1)
                maze[new_row][new_col] -= pow(2, 3)
        else:
            if row < new_row:
                # remove bottom of current one
                maze[row][col] -= pow(2, 2)
                maze[new_row][new_col] -= pow(2, 4)                 
            else:
                # remove upper of current one
                maze[row][col] -= pow(2, 4)
                maze[new_row][new_col] -= pow(2, 2)
        maze[new_row][new_col] += pow(2, 0)
        stack.append((new_row, new_col))

    animations[PLAY_ANIM] = AnimationGroup(*transition_animations, lag_ratio=1)
    return animations


def create_coin_toss():
    global CURRENT_DEGREE

    COIN_POSITION = np.array([0, 0, 0])
    COIN_SIZE = 1
    COIN_THICKNESS = COIN_SIZE / 8
    GOLD_COLOR = "#FFD700"
    DARKER_GOLD_COLOR = "#B59902"
    animations = {}

    # create top and bottom of the coin (needed for the black border)
    circle_1 = Circle(COIN_SIZE, color=BLACK, shade_in_3d=True)
    circle_0 = Circle(COIN_SIZE, color=BLACK, shade_in_3d=True)
    circle_0.move_to(add_offset(COIN_POSITION, COIN_THICKNESS / 2))
    circle_1.move_to(add_offset(COIN_POSITION, - COIN_THICKNESS / 2))
    cylinder = Cylinder(radius=COIN_SIZE, height=COIN_THICKNESS, fill_color=GOLD_COLOR, checkerboard_colors=[GOLD_COLOR]) 
    cylinder.move_to(COIN_POSITION)

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
    
    # init coin
    container = VGroup(cylinder, circle_0, circle_1, head, number)
    animations[CREATE_ANIM] = FadeIn(container)
    animations[INIT_ROTATION] = Rotate(container, angle=PI / 1.5, axis=RIGHT)

    # start anim
    toss_time = 2
    CURRENT_DEGREE = 0
    animations[PLAY_ANIM] = UpdateFromAlphaFunc(container, update_toss_animation, run_time=toss_time)

    return animations


def update_toss_animation(coin, alpha):
    global CURRENT_DEGREE

    ROTATION = 4 * PI
    coin_position = np.array([0, 0, 0])
    pitch_position = np.array([0, 2, 0]) + coin_position

    if alpha < .5:
        coin.move_to(coin_position + pitch_position * alpha * 2)
    else:
        coin.move_to(coin_position + pitch_position - pitch_position * (alpha - .5) * 2)

    to_rotate = ROTATION * alpha - CURRENT_DEGREE
    CURRENT_DEGREE += to_rotate
    coin.rotate(to_rotate, axis=RIGHT)


def add_offset(position, offset):
    return position + np.array([0, 0, offset])