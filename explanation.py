from manim import *
# This is a very simplyfied single cycle core scheme
# animated using manim.
# This one does not invole an LLM as I wanted it to fit my explaination part.
# This will be 100% used in the final edit as the core of the "nerdy part"


class Explanation(Scene):
    def construct(self):
        def create_mux(scene: Scene, position: list) -> VGroup:
            # mux shape
            mux_shape = Polygon(
                [-0.25, 0.4, 0],
                [0.15, 0.2, 0],
                [0.15, -0.2, 0],
                [-0.25, -0.4, 0],
                fill_color=GRAY, fill_opacity=0.2, color=GRAY
            ).shift(position)
            mux_label = Text("MUX", font_size=8).rotate(
                PI/2).next_to([mux_shape.get_x(), mux_shape.get_y(), mux_shape.get_z()]).shift([-0.25, 0, 0])
            mux = VGroup(mux_shape, mux_label)
            return mux

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

            self.wait(1)

        self.play(Uncreate(pc_text))
        self.play(Uncreate(i_text))

        part1 = VGroup(pc, i_mem, l)
        self.play(part1.animate.scale(0.65))
        self.play(part1.animate.shift([-3.5, 0, 0]))

        fetch_stage = VGroup(pc, i_mem, l)

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

        for i in range(1, 4):   # regfile wires
            p = regfile[i].get_edge_center(LEFT) - [0.1, 0, 0]
            l = Line([-0.7, p[1], 0], p)
            lines.add(l)

        p = signext.get_edge_center(LEFT)  # sign extender wire
        l = Line([-0.7, p[1], 0], p)
        lines.add(l)

        decode_stage.add(lines, l1, demux)

        self.play(Create(lines))

        self.play(fetch_stage.animate.shift([-1.5, 0, 0]),
                  decode_stage.animate.shift([-1.5, 0, 0]))

        # ======================
        # ALU
        # ======================

        alu_shape = Polygon(
            [-0.5, 1, 0],
            [0.5, 0.5, 0],
            [0.5, -0.5, 0],
            [-0.5, -1, 0],
            [-0.5, -0.25, 0],
            [-0.25, 0, 0],
            [-0.5, 0.25, 0],
            fill_color=BLUE, fill_opacity=0.2
        ).shift([2.5, -0.5, 0]).scale(1.15)

        alu_label = Text("ALU", font_size=16, color=WHITE)
        alu_label.next_to(alu_shape, RIGHT).rotate(PI/2).shift([-1, 0, 0])

        alu = VGroup(alu_shape, alu_label)

        self.play(Create(alu))

        # add mux and wires
        mux = create_mux(self, [1.25, -1.25, 0])

        lines = VGroup()

        p1 = regfile[5].get_edge_center(RIGHT) + [0.1, 0, 0]  # rs1 wire
        p2 = alu.get_edge_center(LEFT)
        l = Line(p1, [p2[0], p1[1], 0])
        lines.add(l)

        p1 = regfile[6].get_edge_center(RIGHT) + [0.1, 0, 0]  # rs2 wire
        p2 = mux.get_edge_center(LEFT)
        l = Line(p1, [p2[0], p1[1], 0])
        lines.add(l)

        p1 = mux.get_edge_center(RIGHT)  # mux wire
        p2 = alu.get_edge_center(LEFT)
        l = Line(p1, [p2[0], p1[1], 0])
        lines.add(l)

        p1 = signext.get_edge_center(RIGHT)  # imm wires
        p2 = p1 + [0.25, 0, 0]
        p4 = mux.get_edge_center(LEFT) - [0, 0.25, 0]
        p3 = [p2[0], p4[1], 0]
        l1 = Line(p1, p2)
        l2 = Line(p2, p3)
        l3 = Line(p3, p4)
        lines.add(l1)
        lines.add(l2)
        lines.add(l3)

        self.play(Create(mux))
        self.play(Create(lines))

        # ======================
        # DATA MEMORY
        # ======================

        d_mem = create_logic_unit(
            self, 0.65, [4.5, -0.25, 0], RED, ["addr", "data_in", "write_enable"], ["data_out"], True, "Data memory")

        # use result as an address ... 3 lines wire ...
        p1 = alu.get_edge_center(RIGHT)
        p2 = p1 + [0.25, 0, 0]
        p4 = d_mem[1].get_edge_center(LEFT) - [0.1, 0, 0]
        p3 = [p2[0], p4[1], 0]
        l1 = Line(p1, p2)
        l2 = Line(p2, p3)
        l3 = Line(p3, p4)

        addr_wire = VGroup(l1, l2, l3)
        self.play(Create(addr_wire))

        # data coming from register : store

        p1 = regfile[6].get_edge_center(RIGHT) + [0.75, 0, 0]
        p2 = p1 - [0, 1, 0]
        p3 = p2 + [2.7, 0, 0]
        p5 = d_mem[2].get_edge_center(LEFT) - [0.1, 0, 0]
        p4 = [p3[0], p5[1], 0]
        l1 = Line(p1, p2)
        l2 = Line(p2, p3)
        l3 = Line(p3, p4)
        l4 = Line(p4, p5)
        connection_circle = Circle(
            0.05, WHITE, fill_color=WHITE, fill_opacity=1).move_to(p1)

        d_in_wire = VGroup(connection_circle, l1, l2, l3, l4)
        self.play(Create(d_in_wire))

        # or read !

        p1 = d_mem[4].get_edge_center(RIGHT) + [0.1, 0, 0]
        p2 = p1 + [0.4, 0, 0]
        p3 = p2 - [0, 3.4, 0]
        p6 = regfile[4].get_edge_center(LEFT) - [0.1, 0, 0]
        p5 = p6 - [0.6, 0, 0]
        p4 = [p5[0], p3[1], 0]
        l1 = Line(p1, p2)
        l2 = Line(p2, p3)
        l3 = Line(p3, p4)
        l4 = Line(p4, p5)
        l5 = Line(p5, p6)

        wb_wire = VGroup(l1, l2, l3, l4, l5)
        self.play(Create(wb_wire))

        # or write back !
        self.play(Uncreate(wb_wire[0]), Uncreate(wb_wire[1]))

        mux = create_mux(self, [6, 0, 0])
        self.play(Create(mux))

        p1 = addr_wire[1].get_end()  # alu to mux wires
        p2 = p1 + [0, 1.5, 0]
        p3 = p2 + [2.15, 0, 0]
        p5 = mux.get_edge_center(LEFT) + [0, 0.3, 0]
        p4 = [p3[0], p5[1], 0]
        l1 = Line(p1, p2)
        l2 = Line(p2, p3)
        l3 = Line(p3, p4)
        l4 = Line(p4, p5)
        connection_circle = Circle(
            0.05, WHITE, fill_color=WHITE, fill_opacity=1).move_to(p1)
        alu_mux_wire = VGroup(connection_circle, l1, l2, l3, l4)
        self.play(Create(alu_mux_wire))

        p1 = d_mem[4].get_edge_center(RIGHT) + [0.1, 0, 0]  # dmem to mux wires
        p2 = [mux.get_edge_center(LEFT)[0], p1[1], 0]
        dmem_mux_wire = Line(p1, p2)
        self.play(Create(dmem_mux_wire))

        p1 = mux.get_edge_center(RIGHT)  # mux to wb wires
        p2 = p1 + [0.3, 0, 0]
        # p4 connects back to previous wb wires end...
        p4 = wb_wire[2].get_start()
        p3 = [p2[0], p4[1], 0]
        l1 = Line(p1, p2)
        l2 = Line(p2, p3)
        l3 = Line(p3, p4)
        mux_wb_wires = VGroup(l1, l2, l3)
        self.play(Create(mux_wb_wires))

        self.wait(2)
