# Differential equation of the double pendulum
# (2nd order ode transformed in a system of 1st order ode)
# Antonia Kaufmann
# inspired by https://www.youtube.com/watch?v=R3Az7Zd_nys

# how to debug manim code: https://p14jeffwest.blogspot.com/2020/04/how-to-debug-manim-code-with-pycham.html


from manimlib.imports import *
import numpy as np
import scipy.integrate as integrate


def parameters_double_pendulum():
    length = 1
    gravity = 9.81
    return np.array([length, gravity])


def polar_to_cartesian(l, solution):
    # solution_transp = np.transpose(solution)
    x1 = l * np.sin(solution[0])
    y1 = -l * np.cos(solution[0])
    x2 = x1 + l * np.sin(solution[2])
    y2 = y1 - l * np.cos(solution[2])
    return x1, y1, x2, y2


class DoublePendulum(Scene):
    def construct(self):
        axes = NumberPlane().set_opacity(0.2)
        self.add(axes)

        Text1 = TexMobject(rf"""
                \alpha_1 &= 90^o \\
                \dot{{\alpha}}_1 &=0^o/s
                """).to_edge(UP + LEFT)

        self.add(Text1)

        Text2 = TexMobject(rf"""
                \alpha_2 &= 0^o\\
                \dot{{\alpha}}_2 &=0^o/s
                """).to_edge(UP + RIGHT)

        self.add(Text2)

        def rhs(t,y):
            length, gravity = parameters_double_pendulum()
            z = np.zeros(4)
            z[0] = y[1]
            z[2] = y[3]
            M = np.array([[2, np.cos(y[2] - y[0])], [np.cos(y[2] - y[0]), 1]])
            v = np.array([-2 * gravity / length * np.sin(y[0]) + np.sin(y[2] - y[0]) * y[3] ** 2,
                          -gravity / length * np.sin(y[2]) - np.sin(y[2] - y[0]) * y[1] ** 2])
            z[1], z[3] = np.linalg.solve(M, v)
            return z

        # create a time array with dt steps
        length, gravity = parameters_double_pendulum()
        dt = 0.025
        t_span = [0, 5]
        initial_angle1 = 90.0
        initial_angular_velocity1 = 0.0
        initial_angle2 = 0
        initial_angular_velocity2 = 0.0

        # initial state
        state = np.radians([initial_angle1, initial_angular_velocity1, initial_angle2, initial_angular_velocity2])

        # integrate your ODE using scipy.integrate.
        solution = integrate.solve_ivp(fun=rhs, t_span=t_span, y0=state, dense_output=True)
        t_dense = np.arange(t_span[0], t_span[1], dt)
        dense_solution = solution.sol(t_dense)

        x1, y1, x2, y2 = polar_to_cartesian(length, dense_solution)

        # Motion of the Pendulum

        Center = Dot()
        Circle1 = Dot(radius=0.04).move_to(x1[0] * RIGHT + y1[0] * UP).set_color(BLUE)
        Circle2 = Dot(radius=0.04).move_to(x2[0] * RIGHT + y2[0] * UP).set_color(BLUE)

        Line1 = self.getline(Center, Circle1)
        Line1.add_updater(
            lambda mob: mob.become(
                self.getline(Center, Circle1)
            ))

        Line2 = self.getline(Circle1, Circle2)
        Line2.add_updater(
            lambda mob: mob.become(
                self.getline(Circle1, Circle2)
            ))

        self.add(Line1, Line2, Center, Circle1, Circle2)
        traj = VGroup()  # trajectory

        for i in range(len(x1) - 1):
            a = 30
            self.remove(traj)
            traj = VGroup()

            if i >= 30:
                for n in range(i, i - 30, -1):
                    line1 = Line(x1[n] * RIGHT + y1[n] * UP, x1[n - 1] * RIGHT + y1[n - 1] * UP).set_stroke(YELLOW,
                                                                                                            width=2).set_opacity(
                        0.03 * a)  # yellow trajectory for the first pendulum
                    line2 = Line(x2[n] * RIGHT + y2[n] * UP, x2[n - 1] * RIGHT + y2[n - 1] * UP).set_stroke(BLUE,
                                                                                                            width=2).set_opacity(
                        0.03 * a)  # blue trajectory for the second pendulum
                    traj.add(line1)
                    traj.add(line2)
                    a -= 1

            else:
                for n in range(i, 0, -1):
                    line1 = Line(x1[n] * RIGHT + y1[n] * UP, x1[n - 1] * RIGHT + y1[n - 1] * UP).set_stroke(YELLOW,
                                                                                                            width=2).set_opacity(
                        0.05 * a)
                    line2 = Line(x2[n] * RIGHT + y2[n] * UP, x2[n - 1] * RIGHT + y2[n - 1] * UP).set_stroke(BLUE,
                                                                                                            width=2).set_opacity(
                        0.05 * a)
                    traj.add(line1)
                    traj.add(line2)
                    a -= 1

            self.add(traj)
            self.remove(Circle1, Circle2)
            self.add(Circle1, Circle2)
            self.play(
                Circle1.move_to, x1[i + 1] * RIGHT + y1[i + 1] * UP,
                Circle2.move_to, x2[i + 1] * RIGHT + y2[i + 1] * UP,
                run_time=1/100, rate_func=linear)

    def getline(self, Point1, Point2):
        start_point = Point1.get_center()
        end_point = Point2.get_center()
        line = Line(start_point, end_point).set_stroke(width=2)
        return line
