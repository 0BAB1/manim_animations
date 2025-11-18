from manim import *
import pickle

ACCENT_P = ManimColor("#F7A5A5")
ACCENT_Y = ManimColor("#FFDBB6")
LIGHT = ManimColor("#FFF2EF")
FONT_NAME = "Menlo"

def create_logic_unit(size: float, position: list, color: ManimColor, inputs: list, outputs: list, clock: bool = False, title: str = "", inverted=False) -> VGroup:
    """creates a logical unit with I/Os"""
    
    if not inverted:
        w, h = 3*size, 5*size
    else:
        h, w = 2*size, 5*size

    box = RoundedRectangle(width=w, height=h, color=color,
                    fill_color=color, fill_opacity=0.2, stroke_width=1.5, corner_radius=w*0.1)

    vg = VGroup()
    vg.add(box)

    n_in, n_out = len(inputs), len(outputs)

    for i, input in enumerate(inputs):
        text = Text(input, font_size=8, color=ManimColor("#FFF2EF"))
        text.next_to(box, LEFT, buff=-(text.width+0.1))
        text.shift([0, (h/2)-((i+1)*(h/(n_in+1))), 0])
        vg.add(text)

    for i, output in enumerate(outputs):
        text = Text(output, font_size=8, color=ManimColor("#FFF2EF"))
        text.next_to(box, RIGHT, buff=-(text.width+0.1))
        text.shift([0, (h/2)-((i+1)*(h/(n_out+1))), 0])
        vg.add(text)

    if clock:
        text = Text("clock", font_size=8, color=ManimColor("#FFF2EF"))
        text.shift([-text.width/2, 0, 0])
        text.next_to(box, UP, buff=-(text.height+0.1))
        vg.add(text)

    if not title == "":
        text = Text(title, font_size=8, color=ManimColor("#FFF2EF"))
        text.next_to(box, DOWN)
        text.shift([0, 0.5, 0])
        vg.add(text)

    vg.move_to(position)

    return vg

def create_alu(size: float, position: list, color: ManimColor, title :str = "") -> VGroup:
    """creates a logical unit with I/Os"""

    # Define the points in the same order as your lines
    points = [
        [0, 0, 0],
        [0, -0.4 * size, 0],
        [0.1 * size, -0.5 * size, 0],
        [0, -0.6 * size, 0],
        [0, -1 * size, 0],
        [0.35 * size, -0.8 * size, 0],
        [0.35 * size, -0.2 * size, 0],
        [0, 0, 0],  # close the polygon
    ]

    alu = Polygon(*points, color=color, fill_opacity=0.2, fill_color=color, stroke_width=1.5)
    vg = VGroup(alu)

    title_text = Text(title, font_size=size*12)

    # Center the text inside the polygon
    title_text.move_to(alu.get_center()+[0.025*size,0,0])
    title_text.rotate(PI / 2)
    vg.add(title_text)

    vg.move_to(position)

    return vg

def create_mux(position: list, color: ManimColor, size: float = 1.0) -> VGroup:
    points = [
        [-0.25, 0.4, 0],
        [0.0, 0.25, 0],
        [0.0, -0.25, 0],
        [-0.25, -0.4, 0],
    ]
    scaled_points = [[x * size, y * size, z * size] for x, y, z in points]
    mux_shape = Polygon(
        *scaled_points,
        fill_color=color,
        fill_opacity=0.2,
        color=color,
        stroke_width=1.5
    ).shift(position)
    mux_label = Text("MUX", font_size=8 * size).rotate(PI / 2)
    mux_label.move_to(mux_shape.get_center())
    mux = VGroup(mux_shape, mux_label)
    return mux

from manim import *
import numpy as np

def connect(
    scene,
    src: VGroup,
    dst: VGroup,
    color=LIGHT,
    offset_src=RIGHT,
    offset_dst=LEFT,
    pos_src=0.5,
    pos_dst=0.5,
    hgap=0.3,
    stroke_width=1.5,
    waypoints=None,
):
    """
    Draws a Manhattan-style wire (orthogonal only) between two logic units.
    Always goes vertically first (up/down) before horizontal.
    """

    def point_on_edge(vgroup, edge_dir, pos):
        rect = vgroup[0]  # assume first element is the main shape
        w, h = rect.width / 2, rect.height / 2
        cx, cy, cz = rect.get_center()
        if np.allclose(edge_dir, LEFT):
            return np.array([cx - w, cy + h * (0.5 - pos), cz])
        elif np.allclose(edge_dir, RIGHT):
            return np.array([cx + w, cy + h * (0.5 - pos), cz])
        elif np.allclose(edge_dir, UP):
            return np.array([cx - w * (0.5 - pos), cy + h, cz])
        elif np.allclose(edge_dir, DOWN):
            return np.array([cx - w * (0.5 - pos), cy - h, cz])
        else:
            return vgroup.get_center()

    start = point_on_edge(src, offset_src, pos_src)
    end = point_on_edge(dst, offset_dst, pos_dst)

    dir_src = normalize(offset_src)
    step1 = start + dir_src * hgap
    dir_dst = normalize(offset_dst)
    step_last = end + dir_dst * hgap

    # List of intermediate waypoints (optional)
    stops = [step1]
    if waypoints:
        for wp in waypoints:
            stops.append(np.array([wp[0], wp[1], 0]))
    stops.append(step_last)

    # Build vertical-first orthogonal segments
    points = [start]
    for i in range(len(stops)):
        prev = points[-1]
        curr = stops[i]
        # vertical first, then horizontal
        mid = np.array([prev[0], curr[1], 0])
        points.extend([mid, curr])
    # finally connect to end
    mid_to_end = np.array([points[-1][0], end[1], 0])
    points.extend([mid_to_end, end])

    # Create the VMobject wire
    wire = VMobject()
    wire.set_points_as_corners(points)
    wire.set_stroke(color=color, width=stroke_width)

    scene.add(wire)
    return wire

def pulse_wire(scene, wire: VMobject, color=ACCENT_Y, duration=0.15):
    """Return animations for a glowing pulse that fades out."""
    pulse = wire.copy()
    pulse.set_stroke(color=color, width=4, opacity=1.0)
    # DO NOT add pulse to scene manually

    anim_create = Create(pulse, rate_func=linear, run_time=duration)
    anim_fade = FadeOut(pulse, run_time=0.4)

    # Return as a sequential animation
    return Succession(anim_create, anim_fade)


class Animation(Scene):
    def construct(self):
        self.camera.background_color = "#1A2A4F"  # dark background for contrast
        DEFAULT_SIZE = 0.3

        # watermark = Text(
        #     "HOLY CORE ♰", 
        #     font_size=24, 
        #     color=ManimColor("#FFFFFF"), 
        #     stroke_width=0
        # ).move_to([0,0,0]).set_opacity(0.2)  # semi-transparent

        # self.add(watermark)

        # approximate placement
        units = {
            "pc_mux": create_mux([-5.5, 0, 0], ACCENT_Y, size=1.3),
            "pc": create_logic_unit(0.15, [-4.5, 0, 0], ACCENT_Y, [], [], title="PC"),

            "I$": create_logic_unit(DEFAULT_SIZE, [-3, 0.2, 0], ACCENT_Y, [], [], title="I$"),
            "pc_adder": create_alu(1, [-3, -1.5, 0], ACCENT_Y, title="+"),
            "4": create_logic_unit(0.1, [-3.8, -1.75, 0], ACCENT_Y,[], [],  title="0x4", inverted=False),

            "control": create_logic_unit(DEFAULT_SIZE, [-1, 2, 0], ACCENT_Y, [], [], title="Control"),
            "regfile": create_logic_unit(DEFAULT_SIZE, [-1, 0, 0], ACCENT_Y, [], [], title="RegFile"),
            "imm": create_logic_unit(0.2, [-1, -2, 0], ACCENT_Y, [], [], title="Imm", inverted=True),
            
            "alu_mux": create_mux([0.5,0.1,0], ACCENT_Y, size=1),
            "adder_mux": create_mux([0.5,-1.1,0], ACCENT_Y, size=1),

            "alu": create_alu(2, [1.7, 0.85, 0], ACCENT_Y, title="ALU"),
            "adder": create_alu(1.5, [1.7, -1.5, 0], ACCENT_Y, title="+"),

            "D$": create_logic_unit(DEFAULT_SIZE, [3.5, 0, 0], ACCENT_Y, [], [], title="D$"),
            "wb": create_mux([5.5,0,0], ACCENT_Y, size=2)
        }

        for unit in units.values():
            self.add(unit)

        # Example interconnections (customize as needed)
        w1 = connect(self, units["adder"], units["pc_mux"], color=ACCENT_P, waypoints=[(-6.5,-2.7)], pos_dst=.45)
        w2 = connect(self, units["pc_adder"], units["pc_mux"], color=ACCENT_P, waypoints=[(-6.3,-2.5)], pos_dst=0.9)
        w25 = connect(self, units["wb"], units["pc_mux"], color=ACCENT_P, waypoints=[(-6.7,-3)], pos_dst=0.)
        w3 = connect(self, units["pc_mux"], units["pc"], color=ACCENT_P)

        w4 = connect(self, units["pc"], units["I$"], color=ACCENT_P)
        w5 = connect(self, units["pc"], units["pc_adder"], color=ACCENT_P, pos_dst=0)
        w6 = connect(self, units["4"], units["pc_adder"], color=ACCENT_P, pos_dst=1)

        w7 = connect(self, units["I$"], units["control"], color=ACCENT_P)
        w8 = connect(self, units["I$"], units["regfile"], color=ACCENT_P, pos_dst=0)
        w9 = connect(self, units["I$"], units["imm"], color=ACCENT_P)

        w10 = connect(self, units["imm"], units["alu_mux"], color=ACCENT_P, pos_dst=1, waypoints=[(-0.05,-2)])

        w11 = connect(self, units["regfile"], units["alu_mux"], color=ACCENT_P, pos_dst=0, waypoints=[])
    
        w12 = connect(self, units["pc"], units["adder_mux"], color=ACCENT_P, pos_dst=1, waypoints=[(-2,-0.8)])
        w13 = connect(self, units["regfile"], units["adder_mux"], color=ACCENT_P, pos_dst=0, waypoints=[])
        w14 = connect(self, units["regfile"], units["adder_mux"], color=ACCENT_P, pos_dst=0, waypoints=[])
        
        w15 = connect(self, units["regfile"], units["alu"], color=ACCENT_P, pos_dst=0, pos_src=-0.2)
        w16 = connect(self, units["alu_mux"], units["alu"], color=ACCENT_P, pos_dst=1.1)

        w17 = connect(self, units["imm"], units["adder"], color=ACCENT_P, pos_dst=1.1,waypoints=[(-0.05,-2)])
        w18 = connect(self, units["adder_mux"], units["adder"], color=ACCENT_P, pos_dst=0)

        w19 = connect(self, units["alu"], units["D$"], color=ACCENT_P, pos_dst=0)
        w24 = connect(self, units["regfile"], units["D$"], color=ACCENT_P, pos_dst=1)

        w20 = connect(self, units["alu"], units["wb"], color=ACCENT_P, waypoints=[(4.5,1)], pos_dst=0)
        w21 = connect(self, units["D$"], units["wb"], color=ACCENT_P)
        w22 = connect(self, units["adder"], units["wb"], color=ACCENT_P, pos_dst=1, waypoints=[(4.5,-1.5)])

        w23 = connect(self, units["wb"], units["regfile"], color=ACCENT_P, pos_dst=1, waypoints=[(5.5,-3),(-1.75,-3)])

        # Load the trace
        with open("trace_data.pkl", "rb") as f:
            data = pickle.load(f)

        FONT_SIZE = 8
        fmt = lambda x: f"0x{x & 0xFFFFFFFF:08X}"

        # Create the initial text labels at their locations
        pc_text = Text(fmt(data["pc"][0]), font_size=FONT_SIZE, color=ManimColor("#FFF2EF"), font=FONT_NAME).move_to(units["pc"].get_right() + [0.4, 0.3,0])
        instr_text = Text(fmt(data["instr"][0]), font_size=FONT_SIZE, color=ManimColor("#FFF2EF"), font=FONT_NAME).move_to(units["I$"].get_right() + [0.65,0.1,0], UP)
        r1_text = Text(fmt(data['R1'][0]), font_size=FONT_SIZE, color=ManimColor("#FFF2EF"), font=FONT_NAME).move_to(units["regfile"].get_right() + [0.7,1.45,0])
        r2_text = Text(fmt(data['R2'][0]), font_size=FONT_SIZE, color=ManimColor("#FFF2EF"), font=FONT_NAME).move_to(units["regfile"].get_right() + [0.2, -0.3,0]).rotate(PI/2)
        imm_text = Text(fmt(data["imm"][0]), font_size=FONT_SIZE, color=ManimColor("#FFF2EF"), font=FONT_NAME).move_to(units["imm"].get_right() + [0.3,-0.1,0])
        mem_text = Text(fmt(data["mem"][0]), font_size=FONT_SIZE, color=ManimColor("#FFF2EF"), font=FONT_NAME).move_to(units["D$"].get_right()+ [0.3, 0.1,0])
        wb_text = Text(fmt(data["wb"][0]), font_size=FONT_SIZE, color=ManimColor("#FFF2EF"), font=FONT_NAME).move_to(units["wb"].get_right() + [0.2, -0.3,0]).rotate(PI/2)

        self.add(pc_text, instr_text, r1_text, r2_text, imm_text, mem_text, wb_text)

        # Update the values every second
        for i in range(1, min(300, len(data["pc"]))):
            new_pc = Text(fmt(data["pc"][i]), font_size=FONT_SIZE, color=ManimColor("#FFF2EF"), font=FONT_NAME).move_to(pc_text.get_center())
            new_instr = Text(fmt(data["instr"][i]), font_size=FONT_SIZE, color=ManimColor("#FFF2EF"), font=FONT_NAME).move_to(instr_text.get_center())
            new_r1 = Text(fmt(data['R1'][i]), font_size=FONT_SIZE, color=ManimColor("#FFF2EF"), font=FONT_NAME).move_to(r1_text.get_center())
            new_r2 = Text(fmt(data['R2'][i]), font_size=FONT_SIZE, color=ManimColor("#FFF2EF"), font=FONT_NAME).move_to(r2_text.get_center()).rotate(PI/2)
            new_imm = Text(fmt(data["imm"][i]), font_size=FONT_SIZE, color=ManimColor("#FFF2EF"), font=FONT_NAME).move_to(imm_text.get_center())
            new_mem = Text(fmt(data["mem"][i]), font_size=FONT_SIZE, color=ManimColor("#FFF2EF"), font=FONT_NAME).move_to(mem_text.get_center())
            new_wb = Text(fmt(data["wb"][i]), font_size=FONT_SIZE, color=ManimColor("#FFF2EF"), font=FONT_NAME).move_to(wb_text.get_center()).rotate(PI/2)

            OP_CODE = int(data["instr"][i]) & 0x7F

            # --- RISC-V 32I Opcode Map ---
            # (Base subset only, for clarity)
            # 0x33 -> R-type (ALU register)
            # 0x13 -> I-type (ALU immediate)
            # 0x03 -> Load
            # 0x23 -> Store
            # 0x63 -> Branch
            # 0x37 -> LUI
            # 0x17 -> AUIPC
            # 0x6F -> JAL
            # 0x67 -> JALR

            # We'll pulse the wires that roughly correspond to the datapath usage
            # You can fine-tune which wires get pulsed based on your visual layout.

            # --- Update OPCODE pulse block ---
            if OP_CODE == 0x33:  # R-type
                anims = [pulse_wire(self, w) for w in [w8, w4, w15, w7, w6, w2,w5, w3, w11, w16, w20, w23]]

            elif OP_CODE == 0x13:  # I-type
                anims = [pulse_wire(self, w) for w in [w8,w4, w15, w7, w6, w2,w5, w3, w10, w16, w20, w23]]

            elif OP_CODE == 0x03:  # LOAD
                anims = [pulse_wire(self, w) for w in [w8,w4, w15, w7, w6, w2,w5, w3 ,w9, w19, w21, w23, w24]]

            elif OP_CODE == 0x23:  # STORE
                anims = [pulse_wire(self, w) for w in [w8, w4, w15, w7, w6, w2,w5, w3, w10, w16, w19]]

            elif OP_CODE == 0x63:  # BRANCH
                anims = [pulse_wire(self, w) for w in [w8, w4, w7, w12, w17,w9, w18, w1, w3]]

            elif OP_CODE == 0x6F:  # JAL
                anims = [pulse_wire(self, w) for w in [w4, w7, w17, w9, w18,w1, w22, w23]]

            elif OP_CODE == 0x67:  # JALR
                anims = [pulse_wire(self, w) for w in [w8, w4, w7, w10, w1, w3, w25]]

            elif OP_CODE == 0x37:  # LUI
                anims = [pulse_wire(self, w) for w in [w4, w7, w6, w2,w5, w3, w10, w20, w23]]

            elif OP_CODE == 0x17:  # AUIPC
                anims = [pulse_wire(self, w) for w in [w4, w7, w6, w2,w5, w3, w12, w17,w9, w22, w23]]

            else:  # unknown opcode
                anims = [pulse_wire(self, w4)]

            self.play(
                Transform(pc_text, new_pc),
                Transform(instr_text, new_instr),
                Transform(r1_text, new_r1),
                Transform(r2_text, new_r2),
                Transform(imm_text, new_imm),
                Transform(mem_text, new_mem),
                Transform(wb_text, new_wb),
                AnimationGroup(*anims),
                run_time=0.2,  # match pulse duration
                rate_func=linear
            )

            # short delay before next instruction
            self.wait(0.05)