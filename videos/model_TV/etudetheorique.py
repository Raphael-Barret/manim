from manim import *

def animate_equation_gallery(
    scene: Scene,
    visible_formulas: list[str],
    back_formulas: list[str] = None,
    *,
    font_size: int = 64,          # taille initiale (grosse)
    final_font_size: int = 36,     # taille cible si on ne scale pas auto
    vbuff: float = 0.25,
    margin: float = 0.4,          # marge écran
    use_align_env: bool = False,  # si tu mets des & / \\ dans tes formules
) -> Group:
    """
    Affiche une formule, puis la fait évoluer avec TransformMatchingTex
    vers les suivantes, puis finit par afficher toutes les formules
    empilées en plus petit (auto-fit).

    Retourne le VGroup final (galerie).
    """

    assert len(visible_formulas) >= 1, "Il faut au moins une formule"

    # Helper: construire un MathTex avec les bons réglages
    def _mt(s: str) -> MathTex:
        if use_align_env:
            return MathTex(s, font_size=font_size, tex_environment="align*")
        return MathTex(s, font_size=font_size)

    # 1) On écrit la première formule
    current = _mt(visible_formulas[0])
    scene.play(Write(current))

    # 2) Evolutions successives via TransformMatchingTex
    for s in visible_formulas[1:]:
        nxt = _mt(s)
        scene.play(TransformMatchingTex(current, nxt,run_time=1))
        current = nxt

    # 3) Construire la galerie finale (toutes les équations en colonne)
    #    On les construit avec une taille "raisonnable", puis on auto-scale.
    def _mt_final(s: str) -> MathTex:
        if use_align_env:
            return MathTex(s, font_size=final_font_size, tex_environment="align*")
        return MathTex(s, font_size=final_font_size)

    visible_eqs = Group(*[_mt_final(s) for s in visible_formulas]).arrange(DOWN, buff=vbuff, aligned_edge=LEFT)
    if back_formulas != None:
        back_eqs = Group(*[_mt_final(s) for s in back_formulas]).arrange(DOWN, buff=vbuff, aligned_edge=LEFT)
        eqs = Group(visible_eqs,back_eqs).arrange(RIGHT,buff=vbuff*2,aligned_edge=UP)
    else:
        eqs = visible_eqs
    # Placement : centré, puis auto-fit dans la fenêtre
    eqs.move_to(ORIGIN)

    # Auto-fit (width/height) pour que ça rentre dans l’écran
    max_w = config.frame_width - 2 * margin
    max_h = config.frame_height - 2 * margin

    if visible_eqs.width > max_w:
        visible_eqs.scale(max_w / visible_eqs.width)
    if visible_eqs.height > max_h:
        visible_eqs.scale(max_h / visible_eqs.height)

    # Optionnel : placer la colonne un peu plus haut/bas si tu veux
    # eqs.to_edge(UP)

    # 4) Transition finale : l’équation courante devient la galerie
    #    (très joli : la dernière formule "se transforme" en liste complète)
    scene.play(TransformMatchingTex(current, eqs))
    return eqs

class Etudetheorique:
    def __init__(self,scene:Scene):
        self.scene = scene
    
    def test(self):
        formulas = [
            r"{{f(x)}} = {{x}}^{{2}}",
            r"\frac{d}{dx}{{f(x)}} = \frac{d}{dx}{{x}}^{{2}}",
            r"{{f'(x)}} = {{2}}{{x}}",
            r"{{f'(x)}} = {{2}}{{x}} \quad \text{et } f'(0)=0",
        ]

        gallery = animate_equation_gallery(self.scene, formulas,formulas)
        self.scene.wait(1)
        self.scene.play(FadeOut(*gallery))
    
    def primal1(self):
        visible_formulas = [
            r"\hat{u}=argmin_{u{{\in\mathbb{R}}}}{{\frac{1}{2}\|}}u-{{(z-v)\|_{2}^{2}}} + {{\lambda\|}}Su{{\|_{2}^{2}}}",
            r"\hat{p}=argmin_{p{{\in\mathbb{R}}}}{{\frac{1}{2}\|}}-S^{T}p+{{(z-v)\|_{2}^{2}}} - \frac{1}{2}\|z-v\|_{2} + {{\lambda\|}}p{{\|_{2}^{2}}}",
            r"\hat{p}=argmin_{p\in\mathbb{R}}\frac{1}{2}\|-S^{T}p+(z-v)\|_{2}^{2} + \lambda\|p\|_{2}^{2}",
            r"\hat{p}=argmin_{p\in\mathbb{R}}f_{1}^{*}(-S^{T}p)+",
            r""

        ]
        back_formulas = [
            r"3+2"
        ]

        gallery = animate_equation_gallery(self.scene, visible_formulas,back_formulas,font_size=50)
        self.scene.wait(1)
        self.scene.play(FadeOut(*gallery))

    def play(self):
        self.test()
        self.primal1()