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
            ("Lambda grand mu petit", "Imgpresnpz/Lambda_grand_mu_petit/data.npz")  # <-- NPZ ici
        )
        self.partie2 = make_image_gallery(
            [
                ("Textures", "Imgpresnpz/Lambda_petit_mu_grand/u_texture.png"),
                ("Cartoon", "Imgpresnpz/Lambda_petit_mu_grand/v_cartoon.png"),
                ("Reconstruction", "Imgpresnpz/Lambda_petit_mu_grand/reconstruction.png"),
            ],
            ("Lambda petit mu grand", "Imgpresnpz/Lambda_petit_mu_grand/data.npz")  # <-- NPZ ici
        )
        self.partie4 = make_image_gallery(
            [
                ("Textures", "Imgpresnpz/Lambda_mu_ok/u_texture.png"),
                ("Cartoon", "Imgpresnpz/Lambda_mu_ok/v_cartoon.png"),
                ("Reconstruction", "Imgpresnpz/Lambda_mu_ok/reconstruction.png"),
            ],
            ("Lambda Mu ok", "Imgpresnpz/Lambda_mu_ok/data.npz")  # <-- NPZ ici
        )
        self.partie3 = make_image_gallery(
            [
                ("Textures", "Imgpresnpz/lambda_mu_plus_1/u_texture.png"),
                ("Cartoon", "Imgpresnpz/lambda_mu_plus_1/v_cartoon.png"),
                ("Reconstruction", "Imgpresnpz/lambda_mu_plus_1/reconstruction.png"),
            ],
            ("Lambda mu + 1", "Imgpresnpz/lambda_mu_plus_1/data.npz")  # <-- NPZ ici
        )
        
    
    def parties(self,gallery,bottom_parts):
        # 1) On affiche la galerie (ça place aussi le graphe, mais pas animé)
        
        # 2) On anime UNIQUEMENT le bottom (axes/ticks/curves/legend)
        animate_npz_logy(self.scene, bottom_parts)
        self.scene.play(FadeIn(gallery))
        self.scene.wait(1)
        self.scene.play(FadeOut(gallery))

    def play(self):
        self.parties(self.partie1[0],self.partie1[1])
        # self.parties(self.partie2[0],self.partie2[1])
        # self.parties(self.partie3[0],self.partie3[1])
        # self.parties(self.partie4[0],self.partie4[1])
