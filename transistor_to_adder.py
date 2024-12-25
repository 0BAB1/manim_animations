from manim import *


class TransistorToAdder(Scene):
    def construct(self):
        # Set dark background
        self.camera.background_color = "#2B2B2B"

        # Helper function to create a MOSFET transistor
        def create_transistor():
            transistor = VGroup()

            # Create the main channel
            channel = Rectangle(height=1.2, width=0.3,
                                fill_color="#4A90E2", fill_opacity=0.8)

            # Create source and drain terminals
            source = Line(channel.get_top(), channel.get_top() + UP * 0.4)
            drain = Line(channel.get_bottom(),
                         channel.get_bottom() + DOWN * 0.4)

            # Create gate terminal
            gate = Line(channel.get_left() + LEFT * 0.4, channel.get_left())

            # Add arrow for direction
            arrow = Arrow(
                start=channel.get_center() + UP * 0.2,
                end=channel.get_center() + DOWN * 0.2,
                buff=0,
                color=WHITE
            ).scale(0.5)

            transistor.add(channel, source, drain, gate, arrow)
            return transistor

        # Helper function to create clean logic gates
        def create_gate(gate_type):
            gate = VGroup()

            if gate_type == "XOR":
                # XOR Gate
                body = Rectangle(width=1.2, height=1.2,
                                 fill_color="#4CAF50", fill_opacity=0.8)
                arc1 = Arc(radius=0.15, angle=PI/2).move_to(body.get_left())
                arc2 = Arc(radius=0.25, angle=PI /
                           2).move_to(body.get_left() + LEFT * 0.1)
                gate.add(body, arc1, arc2)
                gate.set_stroke(color=WHITE)

            elif gate_type == "AND":
                # AND Gate
                body = Rectangle(width=1.2, height=1.2,
                                 fill_color="#FF6B6B", fill_opacity=0.8)
                gate.add(body)
                gate.set_stroke(color=WHITE)

            elif gate_type == "OR":
                # OR Gate
                body = Rectangle(width=1.2, height=1.2,
                                 fill_color="#FFA726", fill_opacity=0.8)
                arc = Arc(radius=0.15, angle=PI/2).move_to(body.get_left())
                gate.add(body, arc)
                gate.set_stroke(color=WHITE)

            return gate

        # 1. Start with title
        title = Text("From Transistors to Full Adder").scale(0.8).to_edge(UP)
        self.play(Write(title))

        # 2. Show single transistor
        transistor = create_transistor().scale(1.5)
        transistor_labels = VGroup(
            Text("Gate", font_size=24).next_to(transistor, LEFT),
            Text("Source", font_size=24).next_to(transistor, UP),
            Text("Drain", font_size=24).next_to(transistor, DOWN)
        )

        self.play(Create(transistor))
        self.play(Write(transistor_labels))
        self.wait(1)

        # Clear transistor
        self.play(
            FadeOut(transistor),
            FadeOut(transistor_labels)
        )

        # 3. Full Adder Circuit
        # Create gates with proper spacing and alignment
        xor1 = create_gate("XOR").move_to(LEFT * 3)
        xor2 = create_gate("XOR").move_to(RIGHT * 0.5 + UP * 1.5)
        and1 = create_gate("AND").move_to(RIGHT * 0.5 + DOWN * 1.5)
        and2 = create_gate("AND").move_to(LEFT * 3 + DOWN * 2)
        or_gate = create_gate("OR").move_to(RIGHT * 3 + DOWN * 0.5)

        # Create gate labels
        gate_labels = VGroup(
            Text("XOR", font_size=20).next_to(xor1, UP, buff=0.1),
            Text("XOR", font_size=20).next_to(xor2, UP, buff=0.1),
            Text("AND", font_size=20).next_to(and1, DOWN, buff=0.1),
            Text("AND", font_size=20).next_to(and2, DOWN, buff=0.1),
            Text("OR", font_size=20).next_to(or_gate, UP, buff=0.1)
        )

        # Input labels with proper positioning
        inputs = VGroup(
            Text("A", font_size=24).move_to(LEFT * 5 + UP * 1),
            Text("B", font_size=24).move_to(LEFT * 5 + DOWN * 1),
            Text("Cin", font_size=24).move_to(LEFT * 1 + UP * 3)
        )

        # Output labels
        outputs = VGroup(
            Text("Sum", font_size=24).move_to(RIGHT * 5 + UP * 1.5),
            Text("Cout", font_size=24).move_to(RIGHT * 5 + DOWN * 0.5)
        )

        # Create all gates first
        gates = VGroup(xor1, xor2, and1, and2, or_gate)
        self.play(Create(gates))
        self.play(Write(gate_labels))

        # Add inputs and outputs
        self.play(
            Write(inputs),
            Write(outputs)
        )

        # Create connections with proper routing
        connections = VGroup()

        # Input connections
        connections.add(Line(inputs[0].get_right(),
                        xor1.get_left() + UP * 0.3))
        connections.add(Line(inputs[1].get_right(),
                        xor1.get_left() + DOWN * 0.3))

        # XOR1 to XOR2
        connections.add(Line(xor1.get_right(), xor2.get_left() + UP * 0.3))

        # Cin to XOR2
        connections.add(Line(inputs[2].get_bottom(),
                        xor2.get_left() + DOWN * 0.3))

        # AND gate connections
        connections.add(Line(xor1.get_right() + RIGHT *
                        0.1, and1.get_left() + UP * 0.3))
        connections.add(Line(and1.get_right(), or_gate.get_left() + UP * 0.3))
        connections.add(
            Line(and2.get_right(), or_gate.get_left() + DOWN * 0.3))

        # Output connections
        connections.add(Line(xor2.get_right(), outputs[0].get_left()))
        connections.add(Line(or_gate.get_right(), outputs[1].get_left()))

        # Animate connections
        self.play(Create(connections))

        # Add equation at bottom
        equations = MathTex(
            r"Sum &= A \oplus B \oplus C_{in}\\",
            r"C_{out} &= (A \oplus B)C_{in} + AB"
        ).scale(0.8).to_edge(DOWN)

        self.play(Write(equations))
        self.wait(2)
