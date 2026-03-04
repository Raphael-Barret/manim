from manim import *
import numpy as np


from descentegradient3D import Descentegradient3D
from descentegradient import Descentegradient
from introduction import Introduction
from results import Results
from etudetheorique import Etudetheorique




class ModelTV(ThreeDScene):
    def title(self, str_title:str, str_title2:str=None):
        title = Tex(str_title).scale(1.5)
        
        self.play(Write(title))
        self.wait(1)
        if str_title2 != None:
            title2 = Tex(str_title2).scale(1.5)
            self.play(TransformMatchingTex(title,title2))
        else:
            title2 = title
        self.add_fixed_in_frame_mobjects(title2)
        self.play(
            title2.animate.scale(0.5).to_corner(UL),
            run_time=1.5,
        )




    def partie1(self):
        
        pb_global = MathTex(
            r"(\hat{u},\hat{v}) &= \arg\min_{u,v \in \mathbb{R}^{N}} \frac{1}{2}\lVert u+v-z \rVert_{2}^{2}",
            tex_environment="align*"
        )

        pb_primal1 = MathTex(
            r"\hat{u} &= \arg\min_{u \in \mathbb{R}^{N}} \frac{1}{2}\lVert u+v-z \rVert_{2}^{2}",
            tex_environment="align*"
        )

        pb_primal2 = MathTex(
            r"\hat{v} &= \arg\min_{v \in \mathbb{R}^{N}} \frac{1}{2}\lVert u+v-z \rVert_{2}^{2}",
            tex_environment="align*"
        )


        target = VGroup(pb_primal1,pb_primal2).arrange(LEFT,buff=2)
        target.next_to(pb_global,UP)



        self.play(Write(pb_global))
        self.play(
            #TransformMatchingTex(pb_global,target),
            Write(pb_primal1),
            Write(pb_primal2),
            FadeOut(pb_global)
        )

        
    def construct(self):

        self.title("Introduction")
        Introduction(self).play()
        self.play(FadeOut(*self.mobjects)) #Jules
        
        self.title("Méthode de {{Descente de gradient}}","{{Descente de gradient}}")
        Descentegradient(self).play()
        self.play(FadeOut(*self.mobjects)) #Raph

        self.title("{{Descente de gradient}}","{{Descente de gradient}} {{3D}}")
        Descentegradient3D(self).play()
        self.play(FadeOut(*self.mobjects)) #Jules

        self.set_camera_orientation(phi = 0*DEGREES, theta=-90*DEGREES)
        self.title("Etude {{Théori}}qu{{e}}","{{Théori}}{{e}}")
        Etudetheorique(self).play()
        self.play(FadeOut(*self.mobjects))

        self.title("Affichage et analyse des {{Résultats}}","{{Résultats}}")
        Results(self).play()
        self.play(FadeOut(*self.mobjects))


        self.title("Comparaison des méthodes")
        Results(self).play2()
        self.play(FadeOut(*self.mobjects))



        self.play(Write(MathTex(
            r"(\hat u,\hat v)=\arg\min_{\hat u,\hat v\in\mathbb{R}^N} {{\frac{1}{2}\|u+v-z\|_2^2}} + {{\frac{\lambda}{2}\|Su\|_2^2}} + {{\mu\|Dv\|_1}}",
        )))
        self.wait(2)
        self.play(FadeOut(*self.mobjects))
        group = Group(
            Tex("By"),
            Tex("Raphaël Barret"),
            Tex("and"),
            Tex("Jules Grivot Pélisson"),
        ).arrange(DOWN).move_to(ORIGIN)

        self.play(*[Write(m) for m in group])
        self.wait(2)

        self.play(FadeOut(*self.mobjects))
        self.play(Write(Tex("Merci de votre attention")))
        self.play(FadeOut(*self.mobjects))
        self.play(Write(Text("Passons aux questions ?")))



