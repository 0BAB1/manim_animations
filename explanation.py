from manim import *


class Explanation(Scene):
    def construct(self):
        def create_logic_unit(scene: Scene, size: float, position: list, color: ManimColor, inputs: list, outputs: list, clock: bool) -> VGroup:
            box = Rectangle(width=2*size, height=5*size, color=color,
                            fill_color=color, fill_opacity=0.2)

            vg = VGroup()
            vg.add(box)

            w, h = 2*size, 5*size
            n_in, n_out = len(inputs), len(outputs)
            in_coords, out_coords = [], []

            for i, input in enumerate(inputs):
                text = Text(input, font_size=8, color=WHITE)
                text.next_to(box, LEFT, buff=-(text.width+0.1))
                text.shift([0, (h/2)-((i+1)*(h/(n_in+1))), 0])
                in_coords.append(text.get_y())
                vg.add(text)

            for i, output in enumerate(outputs):
                text = Text(output, font_size=8, color=WHITE)
                text.next_to(box, RIGHT, buff=-(text.width+0.1))
                text.shift([0, (h/2)-((i+1)*(h/(n_out+1))), 0])
                out_coords.append(text.get_y())
                vg.add(text)

            if clock:
                text = Text("clock", font_size=8, color=WHITE)
                text.shift([-text.width/2, 0, 0])
                text.next_to(box, UP, buff=-(text.height+0.1))
                vg.add(text)

            vg.move_to(position)

            for element in vg:
                scene.play(Create(element))

            return vg, in_coords, out_coords
        # Set dark background
        self.camera.background_color = "#2B2B2B"

        # ===================
        # INSTRUCTION MEMORY
        # ===================
        instr_box = Rectangle(width=2, height=5, color=RED,
                              fill_color=RED, fill_opacity=0.2)
        left_text = Text("Addr", font_size=10, color=WHITE).next_to(
            instr_box, LEFT, buff=-0.45)
        right_text = Text("RD", font_size=10, color=WHITE).next_to(
            instr_box, RIGHT, buff=-0.3)
        bottom_text = Text("Instruction memory", font_size=10, color=WHITE)
        bottom_text.next_to(instr_box, DOWN, buff=-0.5)
        instr_mem = VGroup(instr_box, left_text, right_text, bottom_text)
        self.play(Create(instr_box))
        self.play(Write(left_text), Write(right_text))
        self.play(Write(bottom_text))
        self.play(instr_mem.animate.shift(1.2*RIGHT))

        # ===================
        # PC
        # ===================
        pc, _, _ = create_logic_unit(
            self, 0.5, [-1.5, 0, 0], GRAY, ["pc_next"], ["pc"], True)

        self.wait(2)
