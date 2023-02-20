from manim import *
from random import randrange, choice, seed
from itertools import chain
from constants import *


RIGHT_L = "right"
LEFT_L = "left"
UP_L = "up"
DOWN_L = "down"
LINE_WIDTH = .45
LINE_WIDTH_OUTER = .8
CELL_SIZE = MAZE_WIDTH / AMOUNT_OF_CELLS


def create_maze_base(scene):
    # init visualization
    outer = Square(AMOUNT_OF_CELLS * CELL_SIZE + 0.5, fill_color=BACKGROUND_COLOR, stroke_width=LINE_WIDTH_OUTER).move_to([MAZE_POSITION])
    scene.play(Create(outer))
    scene.wait(1)
    
    maze_visual = [[Square(CELL_SIZE, fill_opacity=1, fill_color=BACKGROUND_COLOR, stroke_width=0) for _ in range(AMOUNT_OF_CELLS)] for _ in range(AMOUNT_OF_CELLS)]
    maze_visual_group = VGroup(*list(chain.from_iterable(maze_visual))).arrange_in_grid(AMOUNT_OF_CELLS, AMOUNT_OF_CELLS, buff=0)
    maze_visual_group.move_to(MAZE_POSITION)

    #animations[UNCREATE_BORDER] = Uncreate(outer)
    #animations[OBJECT] = outer

    # create the lines
    borders = []
    for i in range(AMOUNT_OF_CELLS):
        for j in range(AMOUNT_OF_CELLS):
            center_front = maze_visual[i][0].get_center()
            center_back = maze_visual[i][-1].get_center()
            line = Line(center_front + [-CELL_SIZE / 2, CELL_SIZE / 2, 0], center_back + [CELL_SIZE / 2, CELL_SIZE / 2, 0], stroke_width=LINE_WIDTH)
            borders.append(line)
            if i == AMOUNT_OF_CELLS - 1:
                line = Line(center_front + [-CELL_SIZE / 2, -CELL_SIZE / 2, 0], center_back + [CELL_SIZE / 2, -CELL_SIZE / 2, 0], stroke_width=LINE_WIDTH)
                borders.append(line)
            
            center_left = maze_visual[0][i].get_center()
            center_right = maze_visual[-1][i].get_center()
            line = Line(center_left + [-CELL_SIZE / 2, CELL_SIZE / 2, 0], center_right + [-CELL_SIZE / 2, -CELL_SIZE / 2, 0], stroke_width=LINE_WIDTH)
            borders.append(line)
            if i == AMOUNT_OF_CELLS - 1:
                line = Line(center_left + [CELL_SIZE / 2, CELL_SIZE / 2, 0], center_right + [CELL_SIZE / 2, -CELL_SIZE / 2, 0], stroke_width=LINE_WIDTH)
                borders.append(line)

    maze_visual_borders = [Create(border) for elems in list(chain.from_iterable(borders)) for border in elems]

    scene.play(AnimationGroup(*maze_visual_borders, lag_ratio=.05))


def create_maze(scene):
    seed(MAZE_SEED)
    """
    Create a maze and returns animations
    """

    animations = {}
    _, init, steps = maze_no_visuals()
    
    # binary digits: upper, right, below, left, visited - where directions declare a wall being present
    maze = [[0b11110 for _ in range(AMOUNT_OF_CELLS)] for _ in range(AMOUNT_OF_CELLS)]
    row, col = init
    maze[row][col] += pow(2, 0) # marks as visited
    stack = [(row, col)]

    # init visualization
    outer = Square(AMOUNT_OF_CELLS * CELL_SIZE + 0.5, fill_color=BACKGROUND_COLOR, stroke_width=LINE_WIDTH_OUTER).move_to([MAZE_POSITION])
    animations[CREATE_BORDER] = Create(outer)
    maze_visual = [[Square(CELL_SIZE, fill_opacity=1, fill_color=BACKGROUND_COLOR, stroke_width=0, stroke_color=BACKGROUND_COLOR) for _ in range(AMOUNT_OF_CELLS)] for _ in range(AMOUNT_OF_CELLS)]
    maze_visual_group = VGroup(*list(chain.from_iterable(maze_visual))).arrange_in_grid(AMOUNT_OF_CELLS, AMOUNT_OF_CELLS, buff=0)
    maze_visual_group.move_to(MAZE_POSITION)

    scene.add(outer)

    # create the lines
    borders = []
    for i, maze_row in enumerate(maze_visual):
        borders.append([])
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
                lines.append(Line(start=corners[0], end=corners[1], stroke_width=LINE_WIDTH))
            if maze[i][j] & 0b01000:
                lines.append(Line(start=corners[1], end=corners[2], stroke_width=LINE_WIDTH))
            if maze[i][j] & 0b00100:
                lines.append(Line(start=corners[2], end=corners[3], stroke_width=LINE_WIDTH))
            if maze[i][j] & 0b00010:
                lines.append(Line(start=corners[3], end=corners[0], stroke_width=LINE_WIDTH))
            borders[-1].append(lines)

    scene.add(maze_visual_group, *[line for border in borders for lines in border for line in lines])
    
    trace = []
    length_satisfied = False
    while stack or trace:
        stack_present = bool(stack)
        if stack_present:
            row, col = stack.pop()
        
        # draw last active cells
        for old_row, old_col in trace:
            maze_visual[old_row][old_col].set_fill_color(MAROON)
        if len(trace) == TRACE_SIZE or length_satisfied:
            length_satisfied = True
            old_row, old_col = trace.pop(0)
            maze_visual[old_row][old_col].set_fill_color(BACKGROUND_COLOR)
        if stack_present:
            trace.append((row, col))
            maze_visual[row][col].set_fill_color(MAROON_E)
        
        for i, maze_row in enumerate(maze_visual):
            for j, elem in enumerate(maze_row):
                # remove lines
                if not maze[i][j] & 0b10000:
                    scene.remove(borders[i][j][0])
                if not maze[i][j] & 0b01000:
                    scene.remove(borders[i][j][1])
                if not maze[i][j] & 0b00100:
                    scene.remove(borders[i][j][2])
                if not maze[i][j] & 0b00010:
                    scene.remove(borders[i][j][3])
        scene.wait(TRANSITION_TIME)

        if not stack_present:
            continue

        # choose possible neigbors (coordinates and if they are not visited yet)
        possible_neighbours = [(row, col - 1), (row, col + 1), (row + 1, col), (row - 1, col)]
        possible_neighbours = [(new_row, new_col) for new_row, new_col in possible_neighbours if 0 <= new_row < AMOUNT_OF_CELLS and 0 <= new_col < AMOUNT_OF_CELLS and maze[new_row][new_col] % 2 == 0]
        if not possible_neighbours:
            continue

        # remove borders in logic
        stack.append((row, col))
        step = steps.pop(0)
        if step == RIGHT_L:
            # remove right of current one
            maze[row][col] -= pow(2, 3)
            new_row, new_col = row, col + 1
            maze[new_row][new_col] -= pow(2, 1)
        if step == LEFT_L:
            # remove left of current one
            maze[row][col] -= pow(2, 1)
            new_row, new_col = row, col - 1
            maze[new_row][new_col] -= pow(2, 3)
        if step == DOWN_L:
            # remove bottom of current one
            maze[row][col] -= pow(2, 2)
            new_row, new_col = row + 1, col
            maze[new_row][new_col] -= pow(2, 4)                 
        if step == UP_L:
            # remove upper of current one
            maze[row][col] -= pow(2, 4)
            new_row, new_col = row - 1, col
            maze[new_row][new_col] -= pow(2, 2)
        maze[new_row][new_col] += pow(2, 0)
        stack.append((new_row, new_col))

    #return animations
    return maze


def create_finished_maze(scene):
    maze, _, _ = maze_no_visuals()

    outer = Square(AMOUNT_OF_CELLS * CELL_SIZE + 0.5, fill_color=BACKGROUND_COLOR, stroke_width=LINE_WIDTH_OUTER).move_to([MAZE_POSITION])
    maze_visual = [[Square(CELL_SIZE, fill_opacity=1, fill_color=BACKGROUND_COLOR, stroke_width=0, stroke_color=BACKGROUND_COLOR) for _ in range(AMOUNT_OF_CELLS)] for _ in range(AMOUNT_OF_CELLS)]
    maze_visual_group = VGroup(*list(chain.from_iterable(maze_visual))).arrange_in_grid(AMOUNT_OF_CELLS, AMOUNT_OF_CELLS, buff=0)
    maze_visual_group.move_to(MAZE_POSITION)

    # create the lines
    borders = []
    for i, maze_row in enumerate(maze_visual):
        borders.append([])
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
                lines.append(Line(start=corners[0], end=corners[1], stroke_width=LINE_WIDTH))
            if maze[i][j] & 0b01000:
                lines.append(Line(start=corners[1], end=corners[2], stroke_width=LINE_WIDTH))
            if maze[i][j] & 0b00100:
                lines.append(Line(start=corners[2], end=corners[3], stroke_width=LINE_WIDTH))
            if maze[i][j] & 0b00010:
                lines.append(Line(start=corners[3], end=corners[0], stroke_width=LINE_WIDTH))
            borders[-1].append(lines)

    maze_complete = VGroup(maze_visual_group, *[line for border in borders for lines in border for line in lines], outer)
    scene.add(maze_complete)

    #return borders, outer
    return maze

def maze_no_visuals():
    seed(MAZE_SEED)
    maze = [[0b11110 for _ in range(AMOUNT_OF_CELLS)] for _ in range(AMOUNT_OF_CELLS)]
    row = randrange(AMOUNT_OF_CELLS)
    col = randrange(AMOUNT_OF_CELLS)
    maze[row][col] += pow(2, 0) # marks as visited
    steps = []
    init = (row, col)
    stack = [init]
    
    while stack:
        row, col = stack.pop()

        # choose possible neigbors (coordinates and if they are not visited yet)
        possible_neighbours = [(row, col - 1), (row, col + 1), (row + 1, col), (row - 1, col)]
        possible_neighbours = [(new_row, new_col) for new_row, new_col in possible_neighbours if 0 <= new_row < AMOUNT_OF_CELLS and 0 <= new_col < AMOUNT_OF_CELLS and maze[new_row][new_col] % 2 == 0]
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
                steps.append(RIGHT_L)
            else:
                # remove left of current one
                maze[row][col] -= pow(2, 1)
                maze[new_row][new_col] -= pow(2, 3)
                steps.append(LEFT_L)
        else:
            if row < new_row:
                # remove bottom of current one
                maze[row][col] -= pow(2, 2)
                maze[new_row][new_col] -= pow(2, 4)   
                steps.append(DOWN_L)              
            else:
                # remove upper of current one
                maze[row][col] -= pow(2, 4)
                maze[new_row][new_col] -= pow(2, 2)
                steps.append(UP_L)
        maze[new_row][new_col] += pow(2, 0)
        stack.append((new_row, new_col))
    return maze, init, steps
