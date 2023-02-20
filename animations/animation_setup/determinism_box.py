from manim import *
from constants import *

NUMBER_BUFFER = 1
BIG_SMALL_RATIO = 0.2

def create_box(side_length=2):
    main_box = Square(side_length, z_index=2, fill_opacity=1, fill_color=BACKGROUND_COLOR)
    img = ImageMobject("clipart64533.png", z_index=3).move_to(main_box.center()).scale(.2)
    small_box_left = Square(side_length * BIG_SMALL_RATIO, z_index=2, fill_opacity=1, fill_color=BACKGROUND_COLOR)
    small_box_right = Square(side_length * BIG_SMALL_RATIO, z_index=2, fill_opacity=1, fill_color=BACKGROUND_COLOR)
    box = VGroup(small_box_left, main_box, small_box_right).arrange(RIGHT, center=True, buff=0)  

    return box, img


def add_number_animation(box, img, scene, number_in, number_out):
    number_text_in = Tex(number_in).next_to(box, LEFT, buff=NUMBER_BUFFER)
    number_text_out = Tex(number_out).move_to(box[-1].get_center())
    scene.play(Write(number_text_in))
    scene.wait(.5)
    scene.play(number_text_in.animate.move_to(box[0].get_center()))
    scene.play(Rotate(img, axis=IN))
    scene.remove(number_text_in)
    scene.wait(.5)
    scene.play(number_text_out.animate.next_to(box, RIGHT, buff=NUMBER_BUFFER))
    scene.wait(.5)
    scene.play(Unwrite(number_text_out))

    
def add_number_animation_parallel(scene, box_determinism, box_non_determinism, img_a, img_b, input_number, output_number_a, output_number_b):
    number_a_text = Tex(input_number).next_to(box_determinism, LEFT, buff=NUMBER_BUFFER)
    number_b_text = Tex(input_number).next_to(box_non_determinism, LEFT, buff=NUMBER_BUFFER)
    scene.play(Write(number_a_text), Write(number_b_text))
    scene.wait(.5)
    scene.play(ScaleInPlace(number_a_text, .8), ScaleInPlace(number_b_text, .8))
    scene.wait(.5)
    scene.play(
        number_a_text.animate.move_to(box_determinism[0].get_center()),
        number_b_text.animate.move_to(box_non_determinism[0].get_center())
    )
    scene.play(Rotate(img_a, axis=IN), Rotate(img_b, axis=IN))
    scene.remove(number_a_text, number_b_text)
    number_a_text = Tex(output_number_a, font_size=MIDDLE_FONT_SIZE).move_to(box_determinism[-1].get_center())
    number_b_text = Tex(output_number_b, font_size=MIDDLE_FONT_SIZE).move_to(box_non_determinism[-1].get_center())
    scene.wait(.5)
    scene.play(
        number_a_text.animate.next_to(box_determinism, RIGHT, buff=NUMBER_BUFFER),
        number_b_text.animate.next_to(box_non_determinism, RIGHT, buff=NUMBER_BUFFER)
    )
    scene.play(ScaleInPlace(number_a_text, 1.3), ScaleInPlace(number_b_text, 1.3))
    scene.wait(.5)
    scene.play(Unwrite(number_a_text), Unwrite(number_b_text))