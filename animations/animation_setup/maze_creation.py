from manim import *
from random import randrange, choice
from itertools import chain
from constants import CREATE_BORDER, FADE_IN_ANIM, CREATE_ANIM, PLAY_ANIM


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