from manim import *

class Descentegradient:
    def __init__(self,scene:Scene):
        self.scene = scene

    def play(self):
        # --- Axes centrés + courbe f(x)=x^2 ---
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-1, 10, 1],
            x_length=8,
            y_length=4.5,
            axis_config={"include_tip": True},
        ).move_to(ORIGIN)

        labels = axes.get_axis_labels(MathTex("x"), MathTex("y"))

        parabola = axes.plot(lambda x: x**2, x_range=[-3.2, 3.2], use_smoothing=True,color=BLUE)
        parabola_label = MathTex("f(x)=x^2").scale(0.8).next_to(parabola, UR)

        self.scene.play(Create(axes), Write(labels))
        self.scene.play(Create(parabola), Write(parabola_label))

        # --- Point sur la courbe, labellé "x" ---
        x0 = ValueTracker(3.0)

        dot = always_redraw(
            lambda: Dot(axes.c2p(x0.get_value(), x0.get_value() ** 2), radius=0.07,color=ORANGE)
        )
        dot_label = always_redraw(
            lambda: MathTex("x").scale(0.8).next_to(dot, UP, buff=0.15)
        )

        # --- Règle de descente de gradient affichée ---
        rule = MathTex(r"x \leftarrow x - \lambda \,\nabla f(x)").to_edge(LEFT)
        self.scene.play(FadeIn(dot, scale=0.8), Write(dot_label), Write(rule))

        # --- Paramètre lambda (step size) ---
        lam = 0.25
        lam_text = MathTex(r"\lambda =", f"{lam}").scale(0.8).next_to(rule, DOWN, aligned_edge=LEFT)
        self.scene.play(Write(lam_text))

        # --- Descente de gradient sur f(x)=x^2 : grad = 2x, donc x <- x - lam*(2x) ---
        def grad(x):
            return 2 * x

        # Affiche le calcul "x = x - λ grad(x)" avec les valeurs au fur et à mesure
        calc = always_redraw(
            lambda: MathTex(
                r"x =",
                f"{x0.get_value():.2f}",
                r"-",
                r"\lambda",
                r"\cdot",
                r"\nabla f(x)",
                r"=",
                f"{x0.get_value():.2f}",
                r"-",
                f"{lam:.2f}",
                r"\cdot",
                f"{grad(x0.get_value()):.2f}",
            ).scale(0.7).next_to(lam_text, DOWN, aligned_edge=LEFT)
        )
        self.scene.play(FadeIn(calc, shift=DOWN * 0.2))

        # --- Itérations (animation du point qui se déplace) ---
        n_steps = 6
        for _ in range(n_steps):
            x_prev = x0.get_value()
            x_next = x_prev - lam * grad(x_prev)

            # petite mise en évidence pendant l'update
            self.scene.play(
                Indicate(rule, scale_factor=1.05),
                x0.animate.set_value(x_next),
                run_time=0.9,
            )

        # --- Petit arrêt visuel ---
        self.scene.wait(0.5)