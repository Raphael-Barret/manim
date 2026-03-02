from manim import *
class Descentegradient3D:
    def __init__(self,scene:Scene):
         self.scene = scene

    def play(self):
            # --- Caméra 3D + axes ---
            axes = ThreeDAxes(
                x_range=[-3, 3, 1],
                y_range=[-3, 3, 1],
                z_range=[0, 10, 2],
                x_length=7,
                y_length=7,
                z_length=4,
            ).move_to(ORIGIN)

            # Paraboloïde : z = f(u,v) = u^2 + v^2
            def f(u, v):
                return u**2 + v**2

            # IMPORTANT: checkerboard_colors doit être une liste OU False (pas None)
            surface = Surface(
                lambda u, v: axes.c2p(u, v, f(u, v)),
                u_range=[-2.2, 2.2],
                v_range=[-2.2, 2.2],
                resolution=(32, 32),
                fill_opacity=0.6,
                checkerboard_colors=False,
            )

            surf_label = MathTex(r"f(u,v)=u^2+v^2").scale(0.8).to_corner(UR)

            self.scene.set_camera_orientation(phi=65 * DEGREES, theta=-45 * DEGREES, zoom=1.05)
            self.scene.begin_ambient_camera_rotation(rate=0.15)

            self.scene.play(Create(axes))
            self.scene.play(Create(surface))
            self.scene.add_fixed_in_frame_mobjects(surf_label)
            self.scene.play(Write(surf_label))

            # --- Point (u,v) sur la surface ---
            u = ValueTracker(1.8)
            v = ValueTracker(-1.2)

            dot = always_redraw(
                lambda: Dot3D(
                    axes.c2p(u.get_value(), v.get_value(), f(u.get_value(), v.get_value())),
                    radius=0.08,
                    color=ORANGE,
                )
            )

            dot_label = always_redraw(
                lambda: MathTex("(u,v)").scale(0.7).next_to(dot, OUT, buff=0.15)
            )

            vertical = always_redraw(
                lambda: Line3D(
                    axes.c2p(u.get_value(), v.get_value(), 0),
                    axes.c2p(u.get_value(), v.get_value(), f(u.get_value(), v.get_value())),
                )
            )

            self.scene.play(FadeIn(dot, scale=0.8), FadeIn(vertical), Write(dot_label))

            # --- Règle de descente de gradient affichée ---
            rule = MathTex(
                r"\begin{pmatrix}u\\v\end{pmatrix}\leftarrow"
                r"\begin{pmatrix}u\\v\end{pmatrix}-\lambda\,\nabla f(u,v)"
            ).to_corner(UL)

            lam = 0.25
            lam_text = MathTex(r"\lambda =", f"{lam}").scale(0.8).next_to(rule, DOWN, aligned_edge=LEFT)

            self.scene.add_fixed_in_frame_mobjects(rule, lam_text)
            self.scene.play(Write(rule), Write(lam_text))

            # ∇f(u,v) = (2u, 2v)
            calc = always_redraw(
                lambda: MathTex(
                    r"\nabla f(u,v)=",
                    r"\begin{pmatrix}2u\\2v\end{pmatrix}=",
                    rf"\begin{{pmatrix}}{(2*u.get_value()):.2f}\\{(2*v.get_value()):.2f}\end{{pmatrix}}",
                
                ).scale(0.65).next_to(lam_text, DOWN, aligned_edge=LEFT)
            )
            self.scene.add_fixed_in_frame_mobjects(calc)
            self.scene.play(FadeIn(calc, shift=DOWN * 0.2))

            # --- Itérations : (u,v) <- (u,v) - lam*(2u,2v) ---
            n_steps = 7
            for _ in range(n_steps):
                u0, v0 = u.get_value(), v.get_value()
                u1 = u0 - lam * (2 * u0)
                v1 = v0 - lam * (2 * v0)

                self.scene.play(
                    Indicate(rule, scale_factor=1.03),
                    u.animate.set_value(u1),
                    v.animate.set_value(v1),
                    run_time=0.9,
                )

            self.scene.wait(0.6)
            self.scene.stop_ambient_camera_rotation()