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
        self.play(FadeOut(*self.mobjects))



        # Descentegradient(self).play()
        # self.play(FadeOut(*self.mobjects))

        # Descentegradient3D(self).play()
        # self.play(FadeOut(*self.mobjects))

        # self.title("Etude {{Théori}}qu{{e}}","{{Théori}}{{e}}")
        # Etudetheorique(self).play()
        

        # self.title("Affichage et analyse des {{Résultats}}","{{Résultats}}")
        # Results(self).play()
        # self.play(FadeOut(*self.mobjects))
        



