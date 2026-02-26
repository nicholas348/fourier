from manimlib import *
from matplotlib import axes
from matplotlib.pyplot import PolarAxes
from numpy import trace
import scipy.integrate



class ComplexWave(Scene):
	def construct(self):
		# ValueTracker that moves the wave
		phi = ValueTracker(0)

		# Define Functions
		func1 = lambda x: np.cos(x*PI + phi.get_value()) 
		func2 = lambda x: np.cos(2*x*PI + PI/6 + 2*phi.get_value())
		func3 = lambda x: np.cos(3*x*PI + PI/4 + 3*phi.get_value())

		funcComplex = lambda x: np.cos(x*PI + phi.get_value()) + np.cos(2*x*PI + PI/6 + 2*phi.get_value()) + np.cos(3*x*PI + PI/4 + 3*phi.get_value())

		# Plot them
		axes1 = Axes(x_range=[-5,5], y_range=[-2,2])
		axes2 = axes1.copy()
		axes3 = axes1.copy()
		axes = axes1.copy()

		# Static graph
		graph1_static = axes1.get_graph(lambda x: np.cos(x*PI), [-5,5,0.1]).scale(1/3).to_edge(RIGHT).shift(UP*2+LEFT)
		graph2_static = axes2.get_graph(lambda x: np.cos(2*x*PI + PI/6), [-5,5,0.1]).scale(1/3).to_edge(RIGHT).shift(LEFT)
		graph3_static = axes3.get_graph(lambda x: np.cos(3*x*PI + PI/4), [-5,5,0.1]).scale(1/3).to_edge(RIGHT).shift(DOWN*2+LEFT)
		graph4_static = axes.get_graph(
		    lambda x: np.cos(x*PI) + np.cos(2*x*PI + PI/6) + np.cos(3*x*PI + PI/4),
		    [-5,5,0.1]
		).scale(1/2).to_edge(LEFT).shift(0.75*DOWN)

		# Surrounding Rectangles
		rec1 = SurroundingRectangle(graph1_static,buff=0.2).set_color(WHITE)
		rec2 = SurroundingRectangle(graph2_static,buff=0.2).set_color(WHITE)
		rec3 = SurroundingRectangle(graph3_static,buff=0.2).set_color(WHITE)
		rec4 = SurroundingRectangle(graph4_static,buff=0.2)

		dot1 = Dot()
		dot2 = Dot()
		dot3 = Dot()
		tail1 = TracingTail(dot1,color = WHITE)
		tail2 = TracingTail(dot2,color = WHITE)
		tail3 = TracingTail(dot3,color = WHITE)
		self.add(tail1,tail2,tail3)

		# Captions
		caption1 = Tex(r'f_{1}(x) = \cos(\pi (x + \varphi))').next_to(rec1,UP,buff=0.1).scale(2/3)
		caption2 = Tex(r'f_{2}(x) = \cos(2\pi (x + \varphi )+ \frac{\pi}{6})').next_to(rec2,UP,buff=0).scale(2/3)
		caption3 = Tex(r'f_{3}(x) = \cos(3\pi (x + \varphi )+ \frac{\pi}{4})').next_to(rec3,UP,buff=0).scale(2/3)
		caption4 = Tex(r'f(x) = f_{1}(x) + f_{2}(x) + f_{3}(x)').next_to(rec4,UP)
		tex_label = always_redraw(lambda: Tex(r'\varphi = {:.2f}'.format(phi.get_value())).next_to(rec4,DOWN))


		# Arrows
		arrow1 = Arrow(rec4.get_right(), rec1.get_left(),buff=0.2).shift(0.3*UP)
		arrow2 = Arrow(rec4.get_right(), rec2.get_left(),buff=0.2)
		arrow3 = Arrow(rec4.get_right(), rec3.get_left(),buff=0.2).shift(0.3*DOWN)

		# Animations
		self.play(FadeIn(graph4_static),ShowCreation(rec4))
		graph4 = always_redraw(
		    lambda: axes.get_graph(funcComplex,[-5,5,0.1])
		    .scale(1/2).to_edge(LEFT).shift(0.75*DOWN)
		)

		self.remove(graph4_static)
		self.add(graph4)

		self.wait(5)
		self.play(ShowCreation(arrow1),ShowCreation(graph1_static),ShowCreation(rec1))

		graph1 = always_redraw(
		    lambda: axes.get_graph(func1,[-5,5,0.1])
		    .scale(1/3).to_edge(RIGHT).shift(UP*2+LEFT)
		)

		self.remove(graph1_static)
		self.add(graph1)

		self.remove(dot1)
		self.play(ShowCreation(arrow2),ShowCreation(graph2_static),ShowCreation(rec2))
		graph2 = always_redraw(
		    lambda: axes.get_graph(func2,[-5,5,0.1])
		    .scale(1/3).to_edge(RIGHT).shift(LEFT)
		)

		self.remove(graph2_static)
		self.add(graph2)

		self.remove(dot2)


		self.play(ShowCreation(arrow3),ShowCreation(graph3_static),ShowCreation(rec3))
		graph3 = always_redraw(
		    lambda: axes.get_graph(func3,[-5,5,0.1])
		    .scale(1/3).to_edge(RIGHT).shift(DOWN*2+LEFT)
		)

		self.remove(graph3_static)
		self.add(graph3)

		self.remove(dot3)
		self.wait(2)
		self.play(Write(caption1))
		self.play(Write(caption2))
		self.play(Write(caption3))
		self.play(Write(caption4))
		self.wait(5)
		self.play(FadeIn(tex_label))
		self.play(phi.animate.set_value(4*PI),run_time = 10)
		self.wait()

class FourierStandardFixed2(Scene):
    def construct(self):
		# SVG settings
        path_mob = SVGMobject(r"C:\Users\F1339\Desktop\ManimLecture\manim\high_clef.svg") 
        path = path_mob.family_members_with_points()[0]

        # path_mob = Tex("\\pi")
        # path = path_mob.family_members_with_points()[0]
        # path.set_height(4)
        
        path.set_height(5) 
        path.center()
        path.set_stroke(WHITE, 1)
        path.set_fill(opacity=0)

        # Fourier Calculations
        n_vectors = 100 
        n_samples = 2000
        
        t_range = np.linspace(0, 1, n_samples, endpoint=False)
        points = [path.point_from_proportion(t) for t in t_range]
        complex_points = np.array([p[0] + 1j * p[1] for p in points])
        
        # Frequencies
        freqs = list(range(-n_vectors // 2, n_vectors // 2 + 1))
        freqs.sort(key=abs) 
        
        coefficients = [
            np.mean(complex_points * np.exp(-TAU * 1j * f * t_range))
            for f in freqs
        ]

        # Vectors
        vectors = VGroup()
        circles = VGroup()
        
        for f, c in zip(freqs, coefficients):
            mag = np.abs(c)
            circle = Circle(radius=mag)
            circle.set_stroke(BLUE_C, width=1, opacity=0.2)
            circles.add(circle)
            
            # Use Line instead of Vectors
            vec = Line(ORIGIN, mag * RIGHT)
            vec.set_stroke(WHITE, width=1)
            
            vec.freq = f
            vec.coeff = c 
            vectors.add(vec)

        # Updaters and Valuetracker: utilize the frequencies
        self.vector_clock = ValueTracker(0)

        def update_vectors(v_group):
            t = self.vector_clock.get_value()
            current_pos = ORIGIN 
            
            for i, v in enumerate(v_group):
                z = v.coeff * np.exp(TAU * 1j * v.freq * t)
                offset = np.array([z.real, z.imag, 0])
                
                circles[i].move_to(current_pos)
                v.put_start_and_end_on(current_pos, current_pos + offset)
                current_pos = v.get_end()

        self.add(circles, vectors)
        vectors.add_updater(update_vectors)

        # Path
        trace = TracedPath(vectors[-1].get_end)
        trace.set_stroke(YELLOW, 3) 
        self.add(trace)

        # Title
        title = Text("Why revolution creates everything?", font = "Times New Roman", font_size = 45).to_edge(UP)

        self.play(
        	ApplyMethod(self.vector_clock.animate.set_value,2,run_time=30,rate_func=linear),
        	Write(title,run_time=2)
        )
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


		def componentFunc(n):
			return lambda x: 4/PI * (1/(2*n+1)) * np.sin((2*n+1)*PI*x/4)

		axes = Axes(y_range=[-2,2],x_range=[-5,5],width=14,height=7.875)
		axes2 = axes.copy()
		sign_graph = axes2.get_graph(sign_func, discontinuities=[0]).set_color(RED)
		sign_group = VGroup(axes2,sign_graph).scale(1/2).to_edge(LEFT)


		self.add(axes)

		componentNumber = 40
		def combinedFunc(n):
			return lambda x: sum((1/(2*k+1)) * np.sin((2*k+1)*PI*x/4) for k in range(n))

		group = VGroup(axes)

		for i in range(componentNumber):
			graph_init = axes.get_graph(componentFunc(i),x_range=[-5,5,0.1]).set_color(BLUE)
			graph_added = axes.get_graph(combinedFunc(i + 1),x_range=[-5,5,0.1])
			graph_added_behind = axes.get_graph(combinedFunc(i + 1),x_range=[-5,5,0.1],stroke_opacity = 0.2)

			if i < 5:
				self.play(FadeIn(graph_init))
				self.wait(2)
				self.play(Transform(graph_init,graph_added))
				self.wait(2)
				self.play(Transform(graph_init,graph_added_behind))
			else:
				self.play(FadeIn(graph_init),run_time = 2/i)
				self.play(Transform(graph_init,graph_added),run_time = 6/i)
				self.play(Transform(graph_init,graph_added_behind),run_time = 2/i)

			group.add(graph_init)

		self.wait(2)
		self.play(group.animate.scale(1/2).to_edge(LEFT))
		self.wait(2)
		self.play(FadeIn(sign_group))
		self.wait(2)
		self.play(sign_group.animate.to_edge(RIGHT))
		self.wait(2)
		self.play(sign_group.animate.to_edge(UP),group.animate.to_edge(UP))
		self.wait(2)

		Tex2 = Tex(r'\operatorname{sgn}(x) = \frac{4}{\pi} \sum_{n=0}^{\infty} \frac{\sin\big((2n+1)x\big)}{2n+1}').next_to(axes,DOWN,buff=1)
		Tex1 = Tex(r'\operatorname{sgn}(x) =\begin{cases}-1, & x < 0 \\0, & x = 0 \\1, & x > 0\end{cases}').next_to(Tex2,RIGHT,buff=1)
		self.play(FadeIn(Tex1),FadeIn(Tex2))
		self.wait(2)





