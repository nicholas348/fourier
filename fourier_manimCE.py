from manim import *
import numpy as np
import scipy.integrate

from mobjects.fourier_circles import FourierCircles


class ComplexWave(Scene):
    def construct(self):
        phi = ValueTracker(0)

        funcs = [
            lambda x: np.cos(x * PI + phi.get_value()),
            lambda x: np.cos(2 * x * PI + PI / 6 + 2 * phi.get_value()),
            lambda x: np.cos(3 * x * PI + PI / 4 + 3 * phi.get_value()),
        ]
        funcs_static = [
            lambda x: np.cos(x * PI),
            lambda x: np.cos(2 * x * PI + PI / 6),
            lambda x: np.cos(3 * x * PI + PI / 4),
        ]

        func_complex = lambda x: sum(f(x) for f in funcs)
        func_complex_static = lambda x: sum(f(x) for f in funcs_static)

        base_axes_kwargs = dict(x_range=[-5, 5, 1], y_range=[-2, 2, 1])
        x_step = 0.005
        plot_kwargs = dict(x_range=[-5, 5, x_step], color=WHITE, use_smoothing=False)

        comp_shifts = [UP * 2 + LEFT, LEFT, DOWN * 2 + LEFT]
        axes_components = [
            Axes(**base_axes_kwargs).scale(1 / 3).to_edge(RIGHT).shift(shift)
            for shift in comp_shifts
        ]
        axes_mix = Axes(**base_axes_kwargs).scale(1 / 2).to_edge(LEFT).shift(0.75 * DOWN)

        graphs_static = [
            ax.plot(f, **plot_kwargs) for ax, f in zip(axes_components, funcs_static)
        ]
        graph4_static = axes_mix.plot(func_complex_static, **plot_kwargs)

        recs = [SurroundingRectangle(g, buff=0.2).set_color(WHITE) for g in graphs_static]
        rec4 = SurroundingRectangle(graph4_static, buff=0.2)

        dots = [Dot() for _ in range(3)]
        tails = [TracedPath(dot.get_center, stroke_color=WHITE) for dot in dots]
        self.add(*tails)

        captions = [
            MathTex(r"f_{1}(x) = \cos(\pi (x + \varphi))"),
            MathTex(r"f_{2}(x) = \cos(2\pi (x + \varphi )+ \frac{\pi}{6})"),
            MathTex(r"f_{3}(x) = \cos(3\pi (x + \varphi )+ \frac{\pi}{4})"),
        ]
        caption_buffs = [0.1, 0, 0]
        captions = [
            cap.next_to(rec, UP, buff=buff).scale(2 / 3)
            for cap, rec, buff in zip(captions, recs, caption_buffs)
        ]
        caption4 = MathTex(r"f(x) = f_{1}(x) + f_{2}(x) + f_{3}(x)").next_to(rec4, UP)
        tex_label = always_redraw(
            lambda: MathTex(r"\varphi = {:.2f}".format(phi.get_value())).next_to(rec4, DOWN)
        )

        arrow_shifts = [0.3 * UP, ORIGIN, 0.3 * DOWN]
        arrows = [
            Arrow(rec4.get_right(), rec.get_left(), buff=0.2).shift(shift)
            for rec, shift in zip(recs, arrow_shifts)
        ]

        self.play(FadeIn(graph4_static), Create(rec4))

        graph4 = always_redraw(lambda: axes_mix.plot(func_complex, **plot_kwargs))
        self.remove(graph4_static)
        self.add(graph4)

        self.wait(5)

        for i, (ax, arrow, graph_static, rec) in enumerate(
            zip(axes_components, arrows, graphs_static, recs)
        ):
            self.play(Create(arrow), Create(graph_static), Create(rec))
            graph = always_redraw(lambda ax=ax, i=i: ax.plot(funcs[i], **plot_kwargs))
            self.remove(graph_static)
            self.add(graph)
            self.remove(dots[i])
        self.wait(2)
        for cap in captions:
            self.play(Write(cap))
        self.play(Write(caption4))
        self.wait(5)
        self.play(FadeIn(tex_label))
        self.play(phi.animate.set_value(4 * PI), run_time=10)
        self.wait()


class FourierStandardFixed2(Scene):
    def construct(self):

        epicycles = FourierCircles(
            input_graph=MathTex(r"\pi"),
            vector_number=100,
            n_samples=2000,
            vector_type="arrow",
        )
        

        trace = TracedPath(epicycles.get_end)
        trace.set_stroke(YELLOW, 3)
        self.add(trace)
        self.play(Create(epicycles))
    
        self.play(epicycles.vector_clock.animate.set_value(2), run_time=30, rate_func=linear)
        self.wait(2)


class PiecewiseExample(Scene):
    def construct(self):
        def sign_func(x):
            if x < 0:
                return -1
            elif x > 0:
                return 1
            elif x == 0:
                return 0

        def component_func(n):
            return lambda x: 4 / PI * (1 / (2 * n + 1)) * np.sin((2 * n + 1) * PI * x / 4)

        axes = Axes(
            y_range=[-2, 2, 1],
            x_range=[-5, 5, 1],
            x_length=14,
            y_length=7.875,
        )
        axes2 = axes.copy()
        sign_graph = axes2.plot(sign_func, x_range=[-5, 5], discontinuities=[0], color=RED)
        sign_group = VGroup(axes2, sign_graph).scale(1 / 2).to_edge(LEFT)

        self.add(axes)

        component_number = 40

        def combined_func(n):
            return lambda x: sum(
                (1 / (2 * k + 1)) * np.sin((2 * k + 1) * PI * x / 4) for k in range(n)
            )

        group = VGroup(axes)

        for i in range(component_number):
            graph_init = axes.plot(component_func(i), x_range=[-5, 5, 0.1], color=BLUE)
            graph_added = axes.plot(combined_func(i + 1), x_range=[-5, 5, 0.1], color=WHITE)
            graph_added_behind = axes.plot(
                combined_func(i + 1), x_range=[-5, 5, 0.1], color=WHITE
            ).set_stroke(opacity=0.2)

            if i < 5:
                self.play(FadeIn(graph_init))
                self.wait(2)
                self.play(Transform(graph_init, graph_added))
                self.wait(2)
                self.play(Transform(graph_init, graph_added_behind))
            else:
                self.play(FadeIn(graph_init), run_time=2 / i)
                self.play(Transform(graph_init, graph_added), run_time=6 / i)
                self.play(Transform(graph_init, graph_added_behind), run_time=2 / i)

            group.add(graph_init)

        self.wait(2)
        self.play(group.animate.scale(1 / 2).to_edge(LEFT))
        self.wait(2)
        self.play(FadeIn(sign_group))
        self.wait(2)
        self.play(sign_group.animate.to_edge(RIGHT))
        self.wait(2)
        self.play(sign_group.animate.to_edge(UP), group.animate.to_edge(UP))
        self.wait(2)

        tex2 = MathTex(
            r"\operatorname{sgn}(x) = \frac{4}{\pi} \sum_{n=0}^{\infty} \frac{\sin\big((2n+1)x\big)}{2n+1}"
        ).next_to(axes, DOWN, buff=1)
        tex1 = MathTex(
            r"\operatorname{sgn}(x) =\begin{cases}-1, & x < 0 \\0, & x = 0 \\1, & x > 0\end{cases}"
        ).next_to(tex2, RIGHT, buff=1)
        self.play(FadeIn(tex1), FadeIn(tex2))
        self.wait(2)
