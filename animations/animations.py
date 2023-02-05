from manim import *
from random import randrange, choice
import math
from itertools import chain


CURRENT_DEGREE = 0

CREATE_BORDER = "create_border"
FADE_IN_ANIM = "fade_in_animation"
CREATE_ANIM = "create_animation"
PLAY_ANIM = "play_animation"

def pow(i, j):
    return int(math.pow(i, j))


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


class MazeCreation3(Scene):
    def construct(self):
        animations = create_maze()
        self.play(animations[CREATE_BORDER])
        self.play(animations[FADE_IN_ANIM])
        self.play(animations[CREATE_ANIM])
        self.play(animations[PLAY_ANIM])

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
    

class MazeCreation2(Scene):
    def construct(self):
        TOTAL_SIZE = 6
        MAZE_SIZE = 4
        CELL_SIZE = TOTAL_SIZE / MAZE_SIZE
        
        # binary digits: upper, right, below, left, visited - where directions declare a wall being present
        maze = [[0b11110 for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]
        row = randrange(len(maze))
        col = randrange(len(maze))
        maze[row][col] += pow(2, 0) # marks as visited
        stack = [(row, col)]

        # init visualization
        border = Square(MAZE_SIZE * CELL_SIZE + 0.5, fill_color=BLACK)
        self.play(Create(border))
        maze_visual = [[Square(CELL_SIZE, fill_opacity=1, fill_color=BLACK, stroke_width=0) for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]
        VGroup(*list(chain.from_iterable(maze_visual))).arrange_in_grid(MAZE_SIZE, MAZE_SIZE, buff=0)
        maze_visual_borders = []
        for maze_row in maze_visual:
            maze_visual_borders.append([])
            for elem in maze_row:
                center = elem.get_center()
                corners = [
                    center + [-CELL_SIZE / 2, CELL_SIZE / 2, 0], 
                    center + [CELL_SIZE / 2, CELL_SIZE / 2, 0], 
                    center + [CELL_SIZE / 2, -CELL_SIZE / 2, 0], 
                    center + [-CELL_SIZE / 2, -CELL_SIZE / 2, 0]
                ]
                lines = (
                    Line(start=corners[0], end=corners[1], z_index=2),
                    Line(start=corners[1], end=corners[2], z_index=2),
                    Line(start=corners[2], end=corners[3], z_index=2),
                    Line(start=corners[3], end=corners[0], z_index=2)
                )
                maze_visual_borders[-1].append(lines)
        init_group = [Create(square) for square in list(chain.from_iterable(maze_visual))]
        self.play(AnimationGroup(*init_group, lag_ratio=.05))
        init_borders = [Create(border) for elems in list(chain.from_iterable(maze_visual_borders)) for border in elems]
        self.play(AnimationGroup(*init_borders, lag_ratio=.05))

        current_marked = Square(side_length=CELL_SIZE - 0.1, fill_opacity=1, fill_color=MAROON, stroke_width=0, z_index=3).move_to(maze_visual[row][col].get_center())
        animations = []
        animations.append(FadeIn(current_marked))
        
        COLOR_BACKWARDS = BLUE
        COLOR_MARKING = MAROON
        color_current = COLOR_MARKING
        
        TRACE_SIZE = 4
        trace = []
        while stack:
            # === logic ===
            row, col = stack.pop()

            trace_animation = None
            if len(trace) == TRACE_SIZE:
                trace_row, trace_col = trace.pop(0)
                trace_cell = maze_visual[trace_row][trace_col]
                trace_animation = trace_cell.animate.set_fill_color(GREY)

            current = Square(side_length=CELL_SIZE - 0.1, fill_opacity=1, fill_color=color_current, stroke_width=0, z_index=3).move_to(maze_visual[row][col].get_center())
            trace.append((row, col))
            mark_new_animations = [Transform(current_marked, current), maze_visual[row][col].animate.set_fill_color(color_current)]
            if trace_animation is not None:
                animations.append(AnimationGroup(trace_animation, AnimationGroup(*mark_new_animations, lag_ratio=1)))
            else:
                animations.append(AnimationGroup(*mark_new_animations, lag_ratio=1))

            # choose possible neigbors (coordinates and if they are not visited yet)
            possible_neighbours = [(row, col - 1), (row, col + 1), (row + 1, col), (row - 1, col)]
            possible_neighbours = [(new_row, new_col) for new_row, new_col in possible_neighbours if 0 <= new_row < MAZE_SIZE and 0 <= new_col < MAZE_SIZE and maze[new_row][new_col] % 2 == 0]
            if not possible_neighbours:
                color_current = COLOR_BACKWARDS
                continue
            color_current = COLOR_MARKING

            stack.append((row, col))
            new_row, new_col = choice(possible_neighbours)
            if row == new_row:
                if col < new_col:
                    # remove right of current one
                    maze[row][col] -= pow(2, 3)
                    maze[new_row][new_col] -= pow(2, 1)

                    animations.append(AnimationGroup(FadeOut(maze_visual_borders[row][col][1]), FadeOut(maze_visual_borders[new_row][new_col][3])))
                else:
                    # remove left of current one
                    maze[row][col] -= pow(2, 1)
                    maze[new_row][new_col] -= pow(2, 3)

                    animations.append(AnimationGroup(FadeOut(maze_visual_borders[row][col][3]), FadeOut(maze_visual_borders[new_row][new_col][1])))
            else:
                if row < new_row:
                    # remove bottom of current one
                    maze[row][col] -= pow(2, 2)
                    maze[new_row][new_col] -= pow(2, 4)    

                    animations.append(AnimationGroup(FadeOut(maze_visual_borders[row][col][2]), FadeOut(maze_visual_borders[new_row][new_col][0])))               
                else:
                    # remove upper of current one
                    maze[row][col] -= pow(2, 4)
                    maze[new_row][new_col] -= pow(2, 2)

                    animations.append(AnimationGroup(FadeOut(maze_visual_borders[row][col][0]), FadeOut(maze_visual_borders[new_row][new_col][2])))
            maze[new_row][new_col] += pow(2, 0)
            stack.append((new_row, new_col))

            # === visualization ===
            #current = maze_visual[new_row][new_col].copy().set_fill_color(MAROON).set_stroke_width(0)
            #self.play(Transform(current_marked, current))
            #threading.Thread(target=lambda _: self.play(Transform(current_marked, current_marked.copy().set_fill_color(BLACK)))).start()
            #current_marked = current
            #self.wait(.2)
        print("done")
        self.play(AnimationGroup(*animations, lag_ratio=1))

        
class MazeCreation(Scene):
    def construct(self):
        MAZE_SIZE = 10
        CELL_SIZE = 0.3
        
        # binary digits: upper, right, below, left, visited - where directions declare a wall being present
        maze = [[0b11110 for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]
        row = randrange(len(maze))
        col = randrange(len(maze))
        maze[row][col] += pow(2, 0) # marks as visited
        stack = [(row, col)]

        # init visualization
        border = Square(MAZE_SIZE * CELL_SIZE + 0.5, fill_color=BLACK)
        self.play(Create(border))
        maze_visual = [[Square(CELL_SIZE, fill_opacity=1, fill_color=BLACK, stroke_width=0) for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]
        VGroup(*list(chain.from_iterable(maze_visual))).arrange_in_grid(MAZE_SIZE, MAZE_SIZE, buff=0)
        maze_visual_borders = []
        for maze_row in maze_visual:
            maze_visual_borders.append([])
            for elem in maze_row:
                center = elem.get_center()
                corners = [
                    center + [-CELL_SIZE / 2, CELL_SIZE / 2, 0], 
                    center + [CELL_SIZE / 2, CELL_SIZE / 2, 0], 
                    center + [CELL_SIZE / 2, -CELL_SIZE / 2, 0], 
                    center + [-CELL_SIZE / 2, -CELL_SIZE / 2, 0]
                ]
                lines = (
                    Line(start=corners[0], end=corners[1], z_index=2),
                    Line(start=corners[1], end=corners[2], z_index=2),
                    Line(start=corners[2], end=corners[3], z_index=2),
                    Line(start=corners[3], end=corners[0], z_index=2)
                )
                maze_visual_borders[-1].append(lines)
        init_group = [Create(square) for square in list(chain.from_iterable(maze_visual))]
        self.play(AnimationGroup(*init_group, lag_ratio=.05))
        init_borders = [Create(border) for elems in list(chain.from_iterable(maze_visual_borders)) for border in elems]
        self.play(AnimationGroup(*init_borders, lag_ratio=.05))

        current_marked = Square(side_length=CELL_SIZE - 0.1, fill_opacity=1, fill_color=MAROON, stroke_width=0, z_index=3).move_to(maze_visual[row][col].get_center())
        self.play(FadeIn(current_marked))
        self.wait()
        
        COLOR_BACKWARDS = BLUE
        COLOR_MARKING = MAROON
        color_current = COLOR_MARKING
        
        TRACE_SIZE = 4
        trace = []
        while stack:
            # === logic ===
            row, col = stack.pop()

            trace_animation = None
            print(len(trace))
            if len(trace) == TRACE_SIZE:
                trace_row, trace_col = trace.pop(0)
                trace_cell = maze_visual[trace_row][trace_col]
                trace_animation = trace_cell.animate.set_fill_color(GREY)

            current = Square(side_length=CELL_SIZE - 0.1, fill_opacity=1, fill_color=color_current, stroke_width=0, z_index=3).move_to(maze_visual[row][col].get_center())
            trace.append((row, col))
            mark_new_animations = [Transform(current_marked, current), maze_visual[row][col].animate.set_fill_color(color_current)]
            if trace_animation is not None:
                self.play(AnimationGroup(trace_animation, AnimationGroup(*mark_new_animations, lag_ratio=1)))
            else:
                self.play(AnimationGroup(*mark_new_animations, lag_ratio=1))


            # choose possible neigbors (coordinates and if they are not visited yet)
            possible_neighbours = [(row, col - 1), (row, col + 1), (row + 1, col), (row - 1, col)]
            possible_neighbours = [(new_row, new_col) for new_row, new_col in possible_neighbours if 0 <= new_row < MAZE_SIZE and 0 <= new_col < MAZE_SIZE and maze[new_row][new_col] % 2 == 0]
            if not possible_neighbours:
                #current = maze_visual[row][col].copy().set_fill_color(BLUE).set_stroke_width(0)
                #self.play(Transform(current_marked, current))
                #current_marked = current
                #self.wait(.2)
                color_current = COLOR_BACKWARDS
                continue
            color_current = COLOR_MARKING

            stack.append((row, col))
            new_row, new_col = choice(possible_neighbours)
            if row == new_row:
                if col < new_col:
                    # remove right of current one
                    maze[row][col] -= pow(2, 3)
                    maze[new_row][new_col] -= pow(2, 1)

                    self.play(FadeOut(maze_visual_borders[row][col][1]), FadeOut(maze_visual_borders[new_row][new_col][3]))
                else:
                    # remove left of current one
                    maze[row][col] -= pow(2, 1)
                    maze[new_row][new_col] -= pow(2, 3)

                    self.play(FadeOut(maze_visual_borders[row][col][3]), FadeOut(maze_visual_borders[new_row][new_col][1]))
            else:
                if row < new_row:
                    # remove bottom of current one
                    maze[row][col] -= pow(2, 2)
                    maze[new_row][new_col] -= pow(2, 4)    

                    self.play(FadeOut(maze_visual_borders[row][col][2]), FadeOut(maze_visual_borders[new_row][new_col][0]))               
                else:
                    # remove upper of current one
                    maze[row][col] -= pow(2, 4)
                    maze[new_row][new_col] -= pow(2, 2)

                    self.play(FadeOut(maze_visual_borders[row][col][0]), FadeOut(maze_visual_borders[new_row][new_col][2]))
            maze[new_row][new_col] += pow(2, 0)
            stack.append((new_row, new_col))

            # === visualization ===
            #current = maze_visual[new_row][new_col].copy().set_fill_color(MAROON).set_stroke_width(0)
            #self.play(Transform(current_marked, current))
            #threading.Thread(target=lambda _: self.play(Transform(current_marked, current_marked.copy().set_fill_color(BLACK)))).start()
            #current_marked = current
            #self.wait(.2)
        print("done")

        
            

class CoinToss(ThreeDScene):
    def construct(self):
        global CURRENT_DEGREE

        # bug when using cashed data
        self.camera.background_color=WHITE

        COIN_POSITION = np.array([0, 0, 0])
        COIN_SIZE = 1
        COIN_THICKNESS = COIN_SIZE / 8
        GOLD_COLOR = "#FFD700"
        DARKER_GOLD_COLOR = "#B59902"

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
        container = VGroup(head, number, cylinder, circle_0, circle_1)
        self.play(Rotate(container, angle=PI / 1.5, axis=RIGHT))
        self.wait(3)

        # start anim
        toss_time = 2
        CURRENT_DEGREE = 0
        self.play(UpdateFromAlphaFunc(container, update_toss_animation, run_time=toss_time))
    
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


class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        square.flip(RIGHT)
        square.rotate(-3 * TAU / 8)
        circle.set_fill(PINK, opacity=0.5)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))

class OpeningManim(Scene):
    def construct(self):
        title = Tex(r"This is some \LaTeX")
        basel = MathTex(r"\sum_{n=1}^\infty \frac{1}{n^2} = \frac{\pi^2}{6}")
        VGroup(title, basel).arrange(DOWN)
        self.play(
            Write(title),
            FadeIn(basel, shift=DOWN),
        )
        self.wait()

        transform_title = Tex("That was a transform")
        transform_title.to_corner(UP + LEFT)
        self.play(
            Transform(title, transform_title),
            LaggedStart(*[FadeOut(obj, shift=DOWN) for obj in basel]),
        )
        self.wait()

        grid = NumberPlane()
        grid_title = Tex("This is a grid", font_size=72)
        grid_title.move_to(transform_title)

        self.add(grid, grid_title)  # Make sure title is on top of grid
        self.play(
            FadeOut(title),
            FadeIn(grid_title, shift=UP),
            Create(grid, run_time=3, lag_ratio=0.1),
        )
        self.wait()

        grid_transform_title = Tex(
            r"That was a non-linear function \\ applied to the grid"
        )
        grid_transform_title.move_to(grid_title, UL)
        grid.prepare_for_nonlinear_transform()
        self.play(
            grid.animate.apply_function(
                lambda p: p
                          + np.array(
                    [
                        np.sin(p[1]),
                        np.sin(p[0]),
                        0,
                    ]
                )
            ),
            run_time=3,
        )
        self.wait()
        self.play(Transform(grid_title, grid_transform_title))
        self.wait()
