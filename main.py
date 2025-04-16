from scipy.integrate import solve_ivp
import numpy as np
from manim import *


def lorenz(t, state, sigma=10, rho=28, beta=8/3):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]


def ode_solution_points(function, state0, time, dt=0.01):
    solution = solve_ivp(
        function,
        t_span=(0, time),
        y0=state0,
        t_eval=np.arange(0, time, dt),
    )
    return solution.y.T


class LorenzAttractor(ThreeDScene):
    def construct(self):
        # Set up 3D axes
        axes = ThreeDAxes(
            x_range=[-50, 50, 5],
            y_range=[-50, 50, 5],
            z_range=[-0, 50, 5],
            x_length=16,
            y_length=16,
            z_length=8
        )
        axes.set_color(WHITE)
        axes.center()

        # Set camera orientation to get the classic "butterfly" view
        # Increasing theta rotates the view counterclockwise around the z-axis (y-axis moves left)
        self.set_camera_orientation(
            phi=90*DEGREES,      # Angle from positive z-axis (top-down view)
            theta=90*DEGREES,    # Increased from 43 to 90 to rotate y-axis more to the left
            gamma=0,             # No camera roll
            zoom=0.9             # Normal zoom level
        )

        self.add(axes)

        # Add signature text as a fixed-in-camera object with high visibility

        signature = Text("made by sam", font_size=36, color=WHITE)
        # Position at the top right corner of the screen
        signature.to_corner(UR, buff=0.5)
        # Make text fixed in frame (proper syntax for ManimCE)
        self.add_fixed_in_frame_mobjects(signature)

        EPSILON = 0.01
        evolution_time = 12
        # Initial conditions & solve ODE
        states = [
            [10, 10, 10 + n * EPSILON]
            for n in range(2)
        ]

        colors = color_gradient([BLUE, YELLOW], len(states))

        # Create curve
        curves = VGroup()
        for state, color in zip(states, colors):
            points = ode_solution_points(lorenz, state, evolution_time)
            curve = VMobject().set_points_as_corners(
                [axes.c2p(*point) for point in points])
            curve.set_stroke(color, 2)
            curves.add(curve)

        # Create glowing dots using a different approach
        dots = VGroup()
        for color in colors:
            # Create a dot with a slight glow using a small sphere
            dot = Sphere(radius=0.15, resolution=(15, 15))
            dot.set_fill(color, opacity=1)
            dot.set_stroke(color, width=0.5, opacity=0.5)
            # Add a small ambient light to create a glow effect
            dot.set_sheen(0.3, UL)
            dots.add(dot)

        def update_dots(dots):
            for dot, curve in zip(dots, curves):
                dot.move_to(curve.get_end())

        # Add the updater outside the function definition
        dots.add_updater(update_dots)

        self.add(dots)

        # Add camera rotation during the animation
        # Negative rate rotates to the right
        self.begin_ambient_camera_rotation(rate=-0.2)

        self.play(
            *[Create(curve) for curve in curves],
            run_time=evolution_time,
            rate_func=linear
        )

        # Optional: stop the rotation at the end
        self.stop_ambient_camera_rotation()

        # Hold the final frame for a moment
        self.wait(2)
