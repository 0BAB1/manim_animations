from manim import *


class Explanation(Scene):
    def construct(self):
        def create_logic_unit(scene: Scene, size: float, position: list, color: ManimColor, inputs: list, outputs: list, clock: bool = False, title: str = "", inverted=False) -> VGroup:
            if not inverted:
                w, h = 2*size, 5*size
            else:
                h, w = 2*size, 5*size

            box = Rectangle(width=w, height=h, color=color,
                            fill_color=color, fill_opacity=0.2)

            vg = VGroup()
            vg.add(box)

            n_in, n_out = len(inputs), len(outputs)

            for i, input in enumerate(inputs):
                text = Text(input, font_size=8, color=WHITE)
                text.next_to(box, LEFT, buff=-(text.width+0.1))
                text.shift([0, (h/2)-((i+1)*(h/(n_in+1))), 0])
                vg.add(text)

            for i, output in enumerate(outputs):
                text = Text(output, font_size=8, color=WHITE)
                text.next_to(box, RIGHT, buff=-(text.width+0.1))
                text.shift([0, (h/2)-((i+1)*(h/(n_out+1))), 0])
                vg.add(text)

            if clock:
                text = Text("clock", font_size=8, color=WHITE)
                text.shift([-text.width/2, 0, 0])
                text.next_to(box, UP, buff=-(text.height+0.1))
                vg.add(text)

            if not title == "":
                text = Text(title, font_size=8, color=WHITE)
                text.next_to(box, DOWN)
                text.shift([0, 0.5, 0])
                vg.add(text)

            vg.move_to(position)

            for element in vg:
                scene.play(Create(element))

            return vg
        # Set dark background
        self.camera.background_color = "#2B2B2B"

        # ===================
        # INSTRUCTION MEMORY
        # ===================
        i_mem = create_logic_unit(
            self, 1, [0, 0, 0], RED, ["addr"], [
                "instr"], True, "instruction mem"
        )

        self.play(i_mem.animate.shift([1.5, 0, 0]))

        # ===================
        # PC
        # ===================
        pc = create_logic_unit(
            self, 0.5, [-1.5, 0, 0], GRAY, ["pc_next"], ["pc"], True)

        l = Line(pc[2].get_edge_center(RIGHT) + [0.1, 0, 0],
                 i_mem[1].get_edge_center(LEFT) - [0.1, 0, 0])

        self.play(Create(l))

        # ======================
        # Clocking illustration
        # ======================

        program = [
            "lui x3 0x1",
            "lw x18 0x8(x3)",
            "sw x18 0xC(x3)",
            "lw x19 0x10(x3)",
            "add x20 x18 x19",
            "and x21 x18 x20",
            "lw x5 0x14(x3)",
            "lw x6 0x18(x3)",
            "or x7 x5 x6",
            "beq x6 x7 0xC"
        ]

        pc_text, i_text = Mobject(), Mobject()
        for i in range(5):
            self.remove(pc_text, i_text)
            # Chage PC
            pc_text = Text(hex(i*4), font_size=8, color=WHITE)
            pc_text.next_to(l, LEFT),
            pc_text.shift([1, pc_text.height * 1.5, 0])
            self.add(pc_text)

            # Change instruction
            i_text = Text(program[i], font_size=8, color=WHITE)
            i_text.next_to(i_mem[0], RIGHT),
            i_text.shift([0, 0, 0])
            self.add(i_text)

            self.wait(1.5)

        self.play(Uncreate(pc_text))
        self.play(Uncreate(i_text))

        part1 = VGroup(pc, i_mem, l)
        self.play(part1.animate.scale(0.65))
        self.play(part1.animate.shift([-3, 0, 0]))

        # ======================
        # CONTROL
        # ======================

        control_out = ["alu_ctrl", "imm_src", "reg_write", "mem_write", "..."]

        control = create_logic_unit(self, 0.7, [0.5, 0, 0], GREEN, [
                                    "instr"], control_out, False, "control unit")

        lines = VGroup()

        l_i = Line(i_mem.get_edge_center(RIGHT), control.get_edge_center(LEFT))
        self.play(Create(l_i))

        for i, out in enumerate(control[2:-1]):
            p1 = out.get_edge_center(RIGHT) + [0.1, 0, 0]
            p2 = p1 + [0.5, 0, 0]
            l = DashedLine(p1, p2)
            lines.add(l)

        self.play(Create(lines))

        self.wait(2)

        self.play(Uncreate(lines))
        self.play(Uncreate(l_i))

        self.play(control.animate.scale(0.5))
        self.play(control.animate.shift([0, 2.7, 0]))

        # ======================
        # REG FILE + SIGN EXT
        # ======================

        regfile = create_logic_unit(self, 0.7, [0.5, -0.5, 0], ORANGE,
                                    ["addr1", "addr2", "addr3", "data3"],
                                    ["data1", "data2"],
                                    True, "Registers")

        signext = create_logic_unit(self, 0.35, [0.5, -3, 0], YELLOW,
                                    ["immediate_in"],
                                    ["imm_out"],
                                    False, "sign_ext", True)

        # move our new group a bit to the right (temporary to leave space for connection illustrations)
        decode_stage = VGroup(control, regfile, signext)

        self.play(decode_stage.animate.shift([0.5, 0, 0]))

        # Create a big line for "DEMUX" in the middle

        demux = Line([-0.7, 3, 0], [-0.7, -3.2, 0])

        p = i_mem.get_edge_center(RIGHT)
        l1 = Line(p, [-0.7, p[1], 0])

        self.play(Create(demux))
        self.play(Create(l1))

        lines = VGroup()
        p = control.get_edge_center(LEFT)  # control wire
        l = Line([-0.7, p[1], 0], p)
        lines.add(l)

        for i in range(1, 5):   # regfile wires
            p = regfile[i].get_edge_center(LEFT) - [0.1, 0, 0]
            l = Line([-0.7, p[1], 0], p)
            lines.add(l)

        p = signext.get_edge_center(LEFT)  # sign extender wire
        l = Line([-0.7, p[1], 0], p)
        lines.add(l)

        self.play(Create(lines))

        self.wait(2)

        self.play(Uncreate(lines), Uncreate(l1))

        self.wait(2)
