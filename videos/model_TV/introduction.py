from manim import *

class Introduction:
    def __init__(self, scene:Scene):
           self.scene = scene

        
    def image(self):
        img = ImageMobject("ImagesPresentation/Lambda_mu_ok/allImages.png")
        self.scene.play(FadeIn(img))
    
    def intro(self):
        raph = Tex("Rahphël Barret",font_size=25)
        jules = Tex("Jules Grivot Pélisson",font_size=25)
        group = Group(Tex("by"),jules,raph)
        self.scene.wait(1)
        group.arrange(DOWN)
        self.scene.play(FadeOut(*group))



    def images(self):
        """
        Affichage des images puis mise en évidence de la décomposition
        """

        def img_block(path: str, title: str, *, scale=1.0) -> Group:
            im = ImageMobject(path).scale(scale)
            lab = Tex(title)
            return Group(im, lab).arrange(UP, buff=0.2)  # <- Group, pas VGroup

        # --- Blocs ---
        img_base = img_block("Imgpresnpz/Lambda_mu_ok/reconstruction.png", "Image de Base")
        img_reconstruite = img_block("Imgpresnpz/Lambda_mu_ok/reconstruction.png", "Image Reconstruite")

        img_u = img_block("Imgpresnpz/Lambda_mu_ok/u_texture.png", "Texture")
        img_v = img_block("Imgpresnpz/Lambda_mu_ok/v_cartoon.png", "Cartoon")
        plus = Tex("+", font_size=40)

        group_decomp = Group(img_u, plus, img_v).arrange(RIGHT, buff=0.6)  # <- Group

        # --- Entrée + placement ---
        self.scene.play(FadeIn(img_base))
        self.scene.play(img_base.animate.shift(UP * 1.5))
        self.scene.play(FadeIn(group_decomp), group_decomp.animate.shift(DOWN * 1.5))
        self.scene.wait(0.5)

        # --- Convergence de chaque élément vers le centre (et pas juste le groupe) ---
        self.scene.play(
            img_base.animate.move_to(ORIGIN),
            *[mob.animate.move_to(ORIGIN) for mob in group_decomp],
            run_time=1.2,
        )
        self.scene.wait(0.3)

        # --- Fade out du "+" et des titres ---
        self.scene.play(
            FadeOut(plus),
            FadeOut(img_u[1]),   # titre Texture
            FadeOut(img_v[1]),   # titre Cartoon
            FadeOut(img_base[1]),# titre Image de Base
            run_time=0.6,
        )
        self.scene.wait(0.2)

        # --- Image reconstruite ---
        img_reconstruite.move_to(ORIGIN)
        self.scene.play(FadeIn(img_reconstruite))
        self.scene.play(Indicate(img_reconstruite[0]))
        self.scene.wait(0.8)
        self.scene.play(FadeOut(img_reconstruite), FadeOut(img_u[0]), FadeOut(img_v[0]),FadeOut(img_base[0]))
    

    def play(self):
        #self.intro()
        self.images()
        equation_globale = MathTex(
            r"(\hat u,\hat v)=\arg\min_{\hat u,\hat v\in\mathbb{R}^N} {{\frac{1}{2}\|u+v-z\|_2^2}} + {{\frac{\lambda}{2}\|Su\|_2^2}} + {{\mu\|Dv\|_1}}",
            tex_environment="align*"
        )
        self.scene.play(Write(equation_globale))
        self.scene.wait(1)
        self.scene.play(FadeOut(equation_globale))
            
        