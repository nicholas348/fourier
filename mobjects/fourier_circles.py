from manim import *
import numpy as np
import os



class FourierCircles(VGroup):
    """FourierCircles mobject.

    Features:
    - Accepts an input shape via `graph` / `input_graph`:
    - A VMobject/path with `point_from_proportion`, OR
    - Higher-level mobjects like `Text` / `MathTex` (a subpath is automatically selected).
    - Computes Fourier coefficients internally from the input shape (sampling over [0, 1)).
    - Provides animated epicycles (circles + vectors) driven by a built-in `ValueTracker`:
    - Animate via `epicycles.vector_clock.animate.set_value(...)`.
    - Vector rendering modes:
    - `vector_type="line"` or `vector_type="arrow"`.
    - Size controls:
    - `scale_factor` (alias `size`) scales all coefficients (and thus overall epicycle size).
    - Auto-fit controls for Text/MathTex (and optional forcing for other inputs):
        `auto_fit`, `force_fit`, `fit_fraction`, `fit_height`, `fit_width`.
    Epicycle (Fourier series) visualization as a reusable Manim mobject.
    """
    def __init__(
        self,
        graph=None,
        input_graph=None,
        svg_file=None,
        n_vectors=100,
        vector_number=None,
        n_samples=2000,
        freqs=None,
        coefficients=None,
        vector_clock=None,
        vector_type="arrow",
        auto_fit=True,
        force_fit=False,
        fit_fraction=0.7,
        fit_height=None,
        fit_width=None,
        scale_factor=1.0,
        size=None,
        circle_color=BLUE_C,
        circle_stroke_width=1,
        circle_opacity=0.2,
        vector_color=WHITE,
        vector_stroke_width=1,
        **kwargs,
    ):
        super().__init__(**kwargs)

        if graph is None:
            graph = input_graph
        if graph is None:
            graph = svg_file
        if isinstance(graph, (str, os.PathLike)):
            graph = SVGMobject(str(graph))
        if vector_number is not None:
            n_vectors = vector_number
        if size is not None:
            scale_factor = size

        def _pick_sampling_path(mob):
            if hasattr(mob, "point_from_proportion"):
                return mob

            if hasattr(mob, "family_members_with_points"):
                members = mob.family_members_with_points()
                if members:
                    def score(m):
                        try:
                            return len(m.get_all_points())
                        except Exception:
                            try:
                                return len(m.get_points())
                            except Exception:
                                return 0

                    return max(members, key=score)

            raise TypeError(
                "input_graph must be a VMobject/path (with point_from_proportion) or a Mobject "
                "that contains such submobjects (e.g. Text/MathTex)."
            )

        if graph is not None:
            graph = graph.copy()

            should_fit = auto_fit and (
                fit_height is not None
                or fit_width is not None
                or isinstance(graph, (Text, Tex, MathTex))
                or force_fit
            )

            if should_fit:
                if fit_height is None:
                    fit_height = config.frame_height * fit_fraction
                if fit_width is None:
                    fit_width = config.frame_width * fit_fraction

                try:
                    graph.scale_to_fit_height(fit_height)
                except Exception:
                    pass

                if graph.width > fit_width:
                    try:
                        graph.scale_to_fit_width(fit_width)
                    except Exception:
                        pass

                graph.center()

        self.graph = graph
        self.sampling_path = _pick_sampling_path(graph) if graph is not None else None
        self.n_vectors = n_vectors
        self.n_samples = n_samples

        if self.sampling_path is not None:
            t_range = np.linspace(0, 1, self.n_samples, endpoint=False)
            points = [self.sampling_path.point_from_proportion(t) for t in t_range]
            complex_points = np.array([p[0] + 1j * p[1] for p in points])

            freqs = list(range(-self.n_vectors // 2, self.n_vectors // 2 + 1))
            freqs.sort(key=abs)
            coefficients = [
                np.mean(complex_points * np.exp(-TAU * 1j * f * t_range)) for f in freqs
            ]

        if freqs is None or coefficients is None:
            raise ValueError("FourierCircles requires either graph=... or (freqs, coefficients).")

        self.freqs = list(freqs)
        self.coefficients = [scale_factor * c for c in coefficients]
        self.vector_clock = vector_clock if vector_clock is not None else ValueTracker(0)
        self.vector_type = vector_type

        self._orient_updater = None

        self.circles = VGroup()
        self.vectors = VGroup()

        for f, c in zip(self.freqs, self.coefficients):
            mag = np.abs(c)

            circle = Circle(radius=mag)
            circle.set_stroke(circle_color, width=circle_stroke_width, opacity=circle_opacity)
            self.circles.add(circle)

            if self.vector_type == "arrow":
                vec = Arrow(ORIGIN, mag * RIGHT, buff=0)
            else:
                vec = Line(ORIGIN, mag * RIGHT)
            vec.set_stroke(vector_color, width=vector_stroke_width)

            vec.freq = f
            vec.coeff = c
            self.vectors.add(vec)

        self.add(self.circles, self.vectors)
        self.add_updater(self._update_epicycles)
        self._update_epicycles(self, 0)

    def _update_epicycles(self, mob, dt=0):
        t = self.vector_clock.get_value()
        current_pos = ORIGIN

        for i, v in enumerate(self.vectors):
            z = v.coeff * np.exp(TAU * 1j * v.freq * t)
            offset = np.array([z.real, z.imag, 0])

            self.circles[i].move_to(current_pos)
            v.put_start_and_end_on(current_pos, current_pos + offset)
            current_pos = v.get_end()

    def get_end(self):
        return self.vectors[-1].get_end()

    def start_orient(self, speed=1.0):
        if self._orient_updater is not None:
            try:
                self.remove_updater(self._orient_updater)
            except Exception:
                pass

        def _updater(mob, dt):
            mob.vector_clock.set_value(mob.vector_clock.get_value() + speed * dt)

        self._orient_updater = _updater
        self.add_updater(self._orient_updater)
        return self

    def set_value(self, value):
        self.vector_clock.set_value(value)
        self._update_epicycles(self, 0)
        return self
