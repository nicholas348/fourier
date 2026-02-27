"""Main Manim entry scenes for this project."""

from manim import *

from mobjects.fourier_circles import FourierCircles


class FourierIntroduction(Scene):
    """Intro scene demonstrating Fourier/epicycle animations."""
    def construct(self):
        image_set = [
            MathTex(r"\Pi").scale(2),
            MathTex(r"\Sigma").scale(2),
            ImageMobject("images/Gerald_G_Violin_2.svg").scale(2),
            ImageMobject("einstein.svg").scale(2),
        ]
        fourier_circles = [
            FourierCircles(
                input_graph=image,
                vector_number=100,
                n_samples=2000,
                vector_type="arrow"
            )
            for image in image_set
        ]
        self.add(fourier_circles[0])


        for i in range(len(fourier_circles) - 1):
            current = fourier_circles[i]
            next_circle = fourier_circles[i + 1]
            start_t = current.vector_clock.get_value()
            end_t = (i + 1) * PI / 4
            self.play(
                UpdateFromAlphaFunc(
                    current,
                    lambda m, a, s=start_t, e=end_t: m.set_value(interpolate(s, e, a)),
                ),
                run_time=3,
                rate_func=linear,
            )
            next_circle.set_value(end_t)
            self.remove(current)
            self.add(next_circle)

        # add introduced texts
        introduction_text = Text("傅里叶级数", font_size=24)
        self.play(Write(introduction_text))
        self.wait(2)
        self.play(FadeOut(introduction_text))

        #the analogy of fourier waves




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

        def merged_wave(x):
            return sum(f(x) for f in funcs)

        def static_merged_wave_func(x):
            return sum(f(x) for f in funcs_static)

        base_axes_kwargs = dict(x_range=[-5, 5, 1], y_range=[-2, 2, 1])
        x_step = 0.005
        plot_kwargs = dict(x_range=[-5, 5, x_step], color=WHITE, use_smoothing=False)

        comp_shifts = [UP * 2 + LEFT, LEFT, DOWN * 2 + LEFT]
        axes_components = [
            Axes(**base_axes_kwargs).scale(1 / 3).to_edge(RIGHT).shift(shift)
            for shift in comp_shifts
        ]

        axes_mix = Axes(**base_axes_kwargs).scale(1 / 2).to_edge(LEFT).shift(0.75 * DOWN)

        static_split_waves = [
            ax.plot(f, **plot_kwargs) for ax, f in zip(axes_components, funcs_static)
        ]
        static_merged_wave = axes_mix.plot(static_merged_wave_func, **plot_kwargs)

        recs_surrounding_split_waves = [SurroundingRectangle(
            g, buff=0.2).set_color(WHITE) for g in static_split_waves
            ]
        rec4_surrounding_split_waves = SurroundingRectangle(static_merged_wave, buff=0.2)

        caption4 = Tex(
            r'f(x) = f_{1}(x) + f_{2}(x) + f_{3}(x)'
            ).next_to(rec4_surrounding_split_waves, UP)
        tex_label = always_redraw(
            lambda: Tex(rf'\varphi = {phi.get_value():.2f}').next_to(
                rec4_surrounding_split_waves, DOWN
            )
        )

        dots = [Dot() for _ in range(3)]
        tails = [TracedPath(dot.get_center, stroke_color=WHITE) for dot in dots]
        self.add(*tails)

        arrow_shifts = [0.3 * UP, ORIGIN, 0.3 * DOWN]
        arrows = [
            Arrow(
                rec4_surrounding_split_waves.get_right(),
                 recs_surrounding_split_waves.get_left(),
                  buff=0.2
            ).shift(shift)
            for rec, shift in zip(recs_surrounding_split_waves, arrow_shifts)
        ]

        self.play(FadeIn(static_merged_wave), Create(rec4_surrounding_split_waves))

        graph4 = always_redraw(lambda: axes_mix.plot(merged_wave, **plot_kwargs))
        self.remove(static_merged_wave)
        self.add(graph4)

        self.wait(5)

        component_items = list(
            zip(axes_components, arrows, static_split_waves, recs_surrounding_split_waves)
        )
        self.play(
            AnimationGroup(
                *[
                    AnimationGroup(Create(arrow), Create(graph_static), Create(rec), lag_ratio=0)
                    for _, arrow, graph_static, rec in component_items
                ],
                lag_ratio=0,
            )
        )

        for i, (ax, _, graph_static, _) in enumerate(component_items):
            graph = always_redraw(lambda ax=ax, i=i: ax.plot(funcs[i], **plot_kwargs))
            self.remove(graph_static)
            self.add(graph)
            self.remove(dots[i])
        self.wait(2)
        self.play(Write(caption4))
        self.wait(5)
        self.play(FadeIn(tex_label))
        self.play(phi.animate.set_value(4 * PI), run_time=10)
        self.wait()



        #fit a square wave
        square_wave = Square().scale(2)

        square_ref = square_wave.copy()
        square_ref.set_stroke(GREY_B, width=2, opacity=0.35)
        self.add(square_ref)

        epicycles = FourierCircles(
            graph=square_wave,
            vector_number=10,
            n_samples=2000,
            vector_type="arrow",
        )
        epicycles.set_value(0)

        trace = TracedPath(epicycles.get_end)
        trace.set_stroke(YELLOW, 3)
        self.add(trace)

        self.play(Create(epicycles))

        speed = 0.25 / 3
        epicycles.start_orient(speed)
        for n_vectors in [25, 60, 120]:
            self.wait(3)
            epicycles.start_orient(0)
            new_epicycles = FourierCircles(
                graph=square_wave,
                vector_number=n_vectors,
                n_samples=2000,
                vector_type="arrow",
            )
            new_epicycles.set_value(epicycles.vector_clock.get_value())
            self.play(ReplacementTransform(epicycles, new_epicycles), run_time=2)
            epicycles = new_epicycles
            epicycles.start_orient(speed)

        self.wait(3)
        epicycles.start_orient(0)

        self.clear()







        #grid presenting the amount of waves

        random_signal = [
            [3, 0.1],
            [5, 0.3],
            [6, 0.2],
            [10, 0.4],
            [15, 0.2],
            [20, 0.1],
        ]

        n_rows = 7
        n_cols = 2
        cell_width = 3.2
        cell_height = 0.8

        cells = VGroup(
            *[
                Rectangle(width=cell_width, height=cell_height).set_stroke(WHITE, width=1)
                for _ in range(n_rows * n_cols)
            ]
        )
        cells.arrange_in_grid(rows=n_rows, cols=n_cols, buff=0.05)

        contents = VGroup()

        if len(random_signal) > 0:
            max_amp = max(a for _, a in random_signal)
        else:
            max_amp = 1.0
        y_lim = max(1e-3, 1.2 * float(max_amp))

        merged_y_lim = max(1e-3, 1.2 * float(sum(abs(a) for _, a in random_signal)))
        merged_phase = ValueTracker(0)
        merged_axes = Axes(
            x_range=[0, TAU, TAU / 2],
            y_range=[-merged_y_lim, merged_y_lim, merged_y_lim],
            x_length=6.0,
            y_length=3.0,
            tips=False,
            axis_config={"stroke_opacity": 0},
        )
        merged_axes.to_edge(LEFT, buff=0.7)
        merged_wave = always_redraw(
            lambda: merged_axes.plot(
                lambda x: sum(
                    a * np.sin(f * (x + merged_phase.get_value())) for f, a in random_signal
                ),
                x_range=[0, TAU, TAU / 200],
                color=WHITE,
                use_smoothing=False,
            ).set_stroke(width=2)
        )

        for row in range(n_rows):
            left_cell = cells[row * n_cols]
            right_cell = cells[row * n_cols + 1]

            if row < min(len(random_signal), n_rows - 1):
                freq, amp = random_signal[row]

                axes = Axes(
                    x_range=[0, TAU, TAU / 2],
                    y_range=[-y_lim, y_lim, y_lim],
                    x_length=cell_width * 0.85,
                    y_length=cell_height * 0.65,
                    tips=False,
                    axis_config={"stroke_opacity": 0},
                )
                axes.move_to(left_cell.get_center())
                wave = axes.plot(
                    lambda x, f=freq, a=amp: a * np.sin(f * x),
                    x_range=[0, TAU],
                    color=YELLOW,
                    use_smoothing=False,
                )
                wave.set_stroke(width=2)

                amp_label = DecimalNumber(amp, num_decimal_places=2).scale(0.6)
                amp_label.move_to(right_cell.get_center())

                contents.add(wave, amp_label)
            else:
                dots_left = VGroup(*[Dot(radius=0.04) for _ in range(3)]).arrange(
                    RIGHT, buff=0.12
                )
                dots_left.move_to(left_cell.get_center())
                dots_right = dots_left.copy().move_to(right_cell.get_center())
                contents.add(dots_left, dots_right)

        grid = VGroup(cells, contents)
        grid.to_edge(RIGHT, buff=0.5)

        split_arrow = Arrow(merged_axes.get_right(), grid.get_left(), buff=0.25)
        split_arrow.set_stroke(WHITE, width=2)

        self.play(FadeIn(merged_wave), Create(cells), FadeIn(contents), GrowArrow(split_arrow))
        self.play(merged_phase.animate.increment_value(TAU), run_time=8, rate_func=linear)
        self.wait(2)
