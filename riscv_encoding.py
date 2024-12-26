from manim import *
# this has been llm generated, thus it is more or less bad.
# The result is nontheless pretty good even though some stuff is to correct
# TODO : align comas, better arrows


class RISCVEncoding(Scene):
    def construct(self):
        # Set dark grey background
        self.camera.background_color = "#2B2B2B"

        # Center everything on screen
        self.camera.frame_center = ORIGIN

        # Create the assembly instruction with highlighted parts
        asm_parts = {
            "op": Text("add", font_size=36),
            "rd": Text("x1", font_size=36),
            "rs1": Text("x2", font_size=36),
            "rs2": Text("x3", font_size=36)
        }

        # Arrange assembly parts with commas and spaces
        asm_group = VGroup(
            asm_parts["op"],
            Text(", ", font_size=36),
            asm_parts["rd"],
            Text(", ", font_size=36),
            asm_parts["rs1"],
            Text(", ", font_size=36),
            asm_parts["rs2"]
        ).arrange(RIGHT, buff=0.2)

        asm_group.to_edge(UP, buff=1)

        # Create binary representation
        binary = "00000000001100010000000010110011"

        # Create colored boxes for different instruction fields
        boxes = VGroup()
        field_colors = {
            "funct7": "#FF6B6B",  # Red
            "rs2": "#4ECDC4",     # Turquoise
            "rs1": "#45B7D1",     # Light blue
            "funct3": "#96CEB4",  # Green
            "rd": "#FFEEAD",      # Yellow
            "opcode": "#D4A5A5"   # Pink
        }

        # Field positions and widths
        fields = [
            ("funct7", 0, 7, None),
            ("rs2", 7, 12, "rs2"),
            ("rs1", 12, 17, "rs1"),
            ("funct3", 17, 20, "op"),  # Link funct3 to "add"
            ("rd", 20, 25, "rd"),
            ("opcode", 25, 32, "op")   # Link opcode to "add"
        ]

        # Calculate total width to center everything
        total_width = len(binary) * 0.25
        start_x = -total_width/2

        # Play the assembly instruction animation
        self.play(Write(asm_group))
        self.wait(1)

        # Create and animate each field
        all_elements = VGroup()
        arrows = VGroup()
        field_boxes = {}  # Store boxes for arrow references

        for field_name, start, end, asm_link in fields:
            # Create field box
            field_width = (end - start) * 0.25
            field_box = Rectangle(
                width=field_width,
                height=0.5,
                fill_color=field_colors[field_name],
                fill_opacity=0.7,
                stroke_color=WHITE
            )

            # Position box
            field_box.move_to(
                np.array([start_x + (start + (end-start)/2) * 0.25, 0, 0])
            )

            # Store box reference
            field_boxes[field_name] = field_box

            # Create field label
            label = Text(field_name, font_size=20)
            label.next_to(field_box, DOWN, buff=0.2)

            # Create binary text for this field
            field_binary = binary[start:end]
            binary_field = Text(field_binary, font_size=20)
            binary_field.move_to(field_box)

            # Create straight arrow if this field links to assembly
            if asm_link:
                start_point = field_box.get_top()
                end_point = asm_parts[asm_link].get_bottom()

                # Create straight arrow with small offset for separation
                arrow = Arrow(
                    start_point + UP * 0.1,
                    end_point - UP * 0.1,
                    buff=0.1,
                    stroke_width=2,
                    max_tip_length_to_length_ratio=0.15,
                    color=WHITE
                )
                arrows.add(arrow)

            # Animate appearance
            self.play(
                Create(field_box),
                Write(label),
                Write(binary_field),
                run_time=0.5
            )

            if asm_link:
                self.play(Create(arrow), run_time=0.5)

            all_elements.add(field_box, label, binary_field)

        # Show complete binary at the bottom
        final_binary = Text(binary, font_size=36, color=WHITE)
        final_binary.next_to(all_elements, DOWN, buff=1)

        self.play(Write(final_binary))

        # Add explanation text
        explanation = Text(
            "(add instruction example : 32bits RISC-V)",
            font_size=24,
            color=WHITE
        )
        explanation.next_to(final_binary, DOWN, buff=0.3)
        self.play(Write(explanation))

        # Final positioning adjustments
        entire_scene = VGroup(asm_group, all_elements,
                              arrows, final_binary, explanation)
        entire_scene.move_to(ORIGIN)

        self.wait(2)
