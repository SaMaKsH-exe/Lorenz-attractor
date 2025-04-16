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

        # Set camera orientation to better view all axes
        self.set_camera_orientation(phi=43*DEGREES, theta=76.1*DEGREES)

        self.add(axes)

        EPSILON = 0.01
        evloution_time = 30
        # Initial conditions & solve ODE
        states = [
            [10, 10, 10 + n*EPSILON]
            for n in range(2)
        ]

        # Create curve
        curves = VGroup()
        states = ode_solution_points(lorenz, [10, 10, 10], 10)
        for state in states:
            points = ode_solution_points(lorenz, state, 10)
            curve = VMobject().set_points_as_corners(axes.c2p(*points.T))
            curve.set_stroke(BLUE, 2)
            curves.add(curve)

        self.play(
            *[Create(curve) for curve in curves],
            run_time=10,
            rate_func=linear
        )
