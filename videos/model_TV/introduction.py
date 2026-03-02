from manim import *

class Introduction:
    def __init__(self, scene:Scene):
           self.scene = scene

    def tests(self):
        eq1 = MathTex(r"x^{2}","-","1","=","0")
        eq2 = MathTex(r"x^{2}","=","1")

        raph = Tex("Rahphël Barret",font_size=25)
        jules = Tex("Jules Grivot Pélisson",font_size=25)

        fonction = MathTex("{{x}}", "^{{2}}")
        derivee = MathTex("{{2}}", "{{x}}")

        jules.next_to(raph,DOWN)
        
        #Animation de présentation
        #self.play(Write(intro))
        self.scene.wait(1)
        self.scene.play(Write(raph),Write(jules))

        self.scene.play(
            raph.animate.shift(UP),
            FadeOut(jules)
        )
        
        self.scene.wait(1)


        self.scene.play(Write(eq1))
        self.scene.wait(1)
        self.scene.play(TransformMatchingTex(eq1,eq2))
        self.scene.wait(1)

        self.scene.remove(eq1,eq2)

        self.scene.play(Write(fonction))
        self.scene.wait(1)
        self.scene.play(TransformMatchingTex(fonction,derivee))
        
    def images(self):
        img = ImageMobject("ImagesPresentation/Lambda_mu_ok/allImages.png")
        self.scene.play(FadeIn(img))

    def play(self):
        self.tests()
        self.images()
            
        