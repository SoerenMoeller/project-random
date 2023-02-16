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