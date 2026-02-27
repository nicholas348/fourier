# Fourier (Manim)

This repo contains a few Manim Community scenes for Fourier/epicycle style animations, plus a reusable mobject `FourierCircles`.

## Project layout

- `fourier_manimCE.py`
  - `ComplexWave` (sum of cosines)
  - `FourierStandardFixed2` (epicycles)
  - `PiecewiseExample`
- `mobjects/fourier_circles.py`
  - `FourierCircles`: reusable epicycle/circle-chain mobject
- `media/`
  - Manim render outputs

## Setup

Create and activate a virtualenv, then install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Notes:
- Manim requires system dependencies (e.g. FFmpeg, LaTeX) depending on your scene.
- On macOS, you typically install FFmpeg via Homebrew:

```bash
brew install ffmpeg
```

## `FourierCircles` mobject

`FourierCircles` takes a shape (path/Text/MathTex/SVG), samples it, computes Fourier coefficients, and draws an animated chain of circles + vectors.

### Minimal usage

```python
from manim import *
from mobjects.fourier_circles import FourierCircles

class Demo(Scene):
    def construct(self):
        epicycles = FourierCircles(
            input_graph=MathTex(r"\pi"),
            vector_number=100,
            n_samples=2000,
            vector_type="arrow",
        )
        self.add(epicycles)
        start_t = epicycles.vector_clock.get_value()
        end_t = 2
        self.play(
            UpdateFromAlphaFunc(
                epicycles,
                lambda m, a, s=start_t, e=end_t: m.set_value(interpolate(s, e, a)),
            ),
            run_time=10,
            rate_func=linear,
        )
```

### Accepted input types

- VMobject/path with `point_from_proportion` (custom paths)
- `Text`, `Tex`, `MathTex` (a subpath is automatically selected)
- SVG file path or `SVGMobject`

Examples:

```python
FourierCircles(input_graph="high_clef.svg", vector_number=120)
FourierCircles(svg_file="high_clef.svg", vector_number=120)
FourierCircles(input_graph=SVGMobject("high_clef.svg"), vector_number=120)
```

### Vector style

- `vector_type="line"` or `vector_type="arrow"`

### Size / fitting controls

- **Scale epicycle size**: `scale_factor=...` (alias `size=...`) scales all coefficients.
- **Auto-fit** (mainly for Text/MathTex):
  - `auto_fit=True/False`
  - `fit_fraction=0.7` (default)
  - `fit_height=...`, `fit_width=...`
  - `force_fit=True` (force fit even for SVG/path inputs)

### Endpoint helper

Use `get_end()` to trace the final tip:

```python
trace = TracedPath(epicycles.get_end)
trace.set_stroke(YELLOW, 3)
self.add(trace)
```
