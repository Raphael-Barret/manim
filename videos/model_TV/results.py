from pathlib import Path
import numpy as np
from manim import *
from utils.results_utils import *


# -----------------------------
# 4) Exemple d’usage dans une Scene
# -----------------------------
class Results:
    def __init__(self,scene:Scene):
        self.scene = scene
        self.partie1 = make_image_gallery(
            [
                ("Textures", "Imgpresnpz/Lambda_grand_mu_petit/u_texture.png"),
                ("Cartoon", "Imgpresnpz/Lambda_grand_mu_petit/v_cartoon.png"),
                ("Reconstruction", "Imgpresnpz/Lambda_grand_mu_petit/reconstruction.png"),
            ],
            ("Lambda grand Mu petit", "Imgpresnpz/Lambda_grand_mu_petit/data.npz")  # <-- NPZ ici
        )
        self.partie2 = make_image_gallery(
            [
                ("Textures", "Imgpresnpz/Lambda_petit_mu_grand/u_texture.png"),
                ("Cartoon", "Imgpresnpz/Lambda_petit_mu_grand/v_cartoon.png"),
                ("Reconstruction", "Imgpresnpz/Lambda_petit_mu_grand/reconstruction.png"),
            ],
            ("Lambda petit Mu grand", "Imgpresnpz/Lambda_petit_mu_grand/data.npz")  # <-- NPZ ici
        )
        self.partie3 = make_image_gallery(
            [
                ("Textures", "Imgpresnpz/Lambda_mu_ok/u_texture.png"),
                ("Cartoon", "Imgpresnpz/Lambda_mu_ok/v_cartoon.png"),
                ("Reconstruction", "Imgpresnpz/Lambda_mu_ok/reconstruction.png"),
            ],
            ("Lambda et Mu optimal", "Imgpresnpz/Lambda_mu_ok/data.npz")  # <-- NPZ ici
        )
        self.partie4 = make_image_gallery(
            [
                ("Textures", "Imgpresnpz/lambda_mu_plus_1/u_texture.png"),
                ("Cartoon", "Imgpresnpz/lambda_mu_plus_1/v_cartoon.png"),
                ("Reconstruction", "Imgpresnpz/lambda_mu_plus_1/reconstruction.png"),
            ],
            ("Lambda et Mu > 1", "Imgpresnpz/lambda_mu_plus_1/data.npz")  # <-- NPZ ici
        )
        self.fft1_img = make_image_gallery(
            [
                ("Passe Bas(u)", "Imgpresnpz/Passe_bas/u_texture.png"),
                ("Passe Bas(v)", "Imgpresnpz/Passe_bas/v_cartoon"),
                ("Cartoon/Texture(u)", "Imgpresnpz/Lambda_mu_ok/u_texture.png"),
                ("Cartoon/Texture(v)", "Imgpresnpz/Lambda_mu_ok/v_cartoon.png"),
            ],
            ("", "Imgpresnpz/Lambda_mu_ok/data.npz"),  # <-- NPZ ici
            top_img_height=1.9,
            bottom_graph_height=1.3,
            row_buff=0,
        )
        self.fft1 = make_image_gallery(
            [
                ("Passe Bas(u)", "Imgpresnpz/Passe_bas/fft_u_texture.png"),
                ("Passe Bas(v)", "Imgpresnpz/Passe_bas/fft_v_cartoon"),
                ("Cartoon/Texture(u)", "Imgpresnpz/Lambda_mu_ok/fft_u_texture.png"),
                ("Cartoon/Texture(v)", "Imgpresnpz/Lambda_mu_ok/fft_v_cartoon.png"),
            ],
            ("", "Imgpresnpz/Lambda_mu_ok/data.npz"),  # <-- NPZ ici
            top_img_height=1.9,
            bottom_graph_height=1.3,
            row_buff=0,
        )
        
    
    def parties(self,gallery,bottom_parts,mse=False):
        # 1) On affiche la galerie (ça place aussi le graphe, mais pas animé)
        
        # 2) On anime UNIQUEMENT le bottom (axes/ticks/curves/legend)
        self.scene.play(FadeIn(gallery))
        #animate_npz_logy(self.scene, bottom_parts)
        if mse:
            self.scene.play(
                    Group
                    (
                        Text("MSE: 0.0088",font_size=16),
                        Text("SSIM: 0.7160",font_size=16)
                    ).arrange(DOWN,buff=.2).animate.to_edge(RIGHT)
            )

        self.scene.wait(1)
        self.scene.play(FadeOut(gallery))

        
    def play(self):
        self.parties(self.partie1[0],self.partie1[1])
        self.parties(self.partie2[0],self.partie2[1])
        self.parties(self.partie3[0],self.partie3[1])
        self.parties(self.partie4[0],self.partie4[1],True)
    
    def play2(self):
        self.parties(self.fft1_img[0],self.fft1_img[1])

        self.parties(self.fft1[0],self.fft1[1])
        
