from manim import *


def courbes_pb_dual(scene:Scene):
    # --- (tout ton code de création des objets, inchangé) ---
    x_range = [-4, 6, 2]
    y_range = [-3, 5, 2]
    axis_config = dict(axis_config={"stroke_width": 3}, tips=True)

    blue = BLUE_D
    orange = ORANGE

    a = 0.18
    x0 = 1.2
    y0 = -1.0
    f = lambda x: a * (x - x0) ** 2 + y0

    m = 0.75
    b = 0.15
    ell = lambda x: m * x + b

    b2 = -1.65
    ell2 = lambda x: m * x + b2

    axL = Axes(x_range=x_range, y_range=y_range, **axis_config).scale(0.85)
    axR = Axes(x_range=x_range, y_range=y_range, **axis_config).scale(0.85)
    panels = VGroup(axL, axR).arrange(RIGHT, buff=1.5).to_edge(DOWN).shift(UP * 0.2)

    graphL = axL.plot(f, x_range=[x_range[0], x_range[1]], color=blue, stroke_width=5)
    graphR = axR.plot(f, x_range=[x_range[0], x_range[1]], color=blue, stroke_width=5)

    dashedL = DashedVMobject(axL.plot(ell, x_range=[x_range[0], x_range[1]], color=BLACK, stroke_width=4), num_dashes=28)
    dashedR = DashedVMobject(axR.plot(ell, x_range=[x_range[0], x_range[1]], color=BLACK, stroke_width=4), num_dashes=28)

    lab_u_L = MathTex(r"\langle", "u", r",\cdot\rangle", color=BLACK).scale(0.5)
    lab_u_L[1].set_color(orange)
    lab_u_L.next_to(dashedL, UP, buff=0.15).shift(RIGHT * 1.2)

    lab_u_R = MathTex(r"\langle", "u", r",\cdot\rangle", color=BLACK).scale(0.5)
    lab_u_R[1].set_color(orange)
    lab_u_R.next_to(dashedR, UP, buff=0.15).shift(RIGHT * 1.2)

    x_u = 2.2
    y_top = ell(x_u)
    vline = Line(axL.c2p(x_u, 0), axL.c2p(x_u, y_top), color=orange, stroke_width=6)

    arrow_head = Arrow(
        start=axL.c2p(x_u, y_top - 0.01),
        end=axL.c2p(x_u, y_top),
        buff=0,
        color=orange,
        stroke_width=6,
        max_tip_length_to_length_ratio=0.35,
    )

    lab_fstar = MathTex(r"f^{*}(u)", color=orange).scale(1.05)
    lab_fstar.next_to(vline, LEFT, buff=0.25).shift(DOWN * 0.5)

    orange_line = axR.plot(ell2, x_range=[x_range[0], x_range[1]], color=orange, stroke_width=6)
    dot = Dot(axR.c2p(0, b2), color=orange, radius=0.12)

    lab_minus_f = MathTex(r"-f^{*}(u)", color=orange).scale(1.05)
    lab_minus_f.next_to(dot, RIGHT, buff=0.25).shift(DOWN * 0.15)

    # ---------------------------------------------------------
    # B) ANIMATION (remplace tes self.add par ça)
    # ---------------------------------------------------------

    # 1) Axes (les deux en même temps)
    scene.play(LaggedStart(Create(axL), Create(axR), lag_ratio=0.15), run_time=1.2)

    # 2) Courbes bleues
    scene.play(LaggedStart(Create(graphL), Create(graphR), lag_ratio=0.15), run_time=1.2)

    # 3) Lignes pointillées + labels <u,.>
    scene.play(
        LaggedStart(
            Create(dashedL), Write(lab_u_L),
            Create(dashedR), Write(lab_u_R),
            lag_ratio=0.12,
        ),
        run_time=1.2
    )

    # 4) Panneau gauche : segment vertical + pointe + label f*(u)
    scene.play(Create(vline), run_time=0.6)
    scene.play(GrowArrow(arrow_head), run_time=0.4)
    scene.play(Write(lab_fstar), run_time=0.5)

    # 5) Panneau droit : droite orange + point + label -f*(u)
    scene.play(Create(orange_line), run_time=0.8)
    scene.play(FadeIn(dot, scale=0.5), run_time=0.25)
    scene.play(Write(lab_minus_f), run_time=0.5)

    scene.wait(0.6)

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
    align = LEFT,
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
        scene.wait(.5)

    # 3) Construire la galerie finale (toutes les équations en colonne)
    #    On les construit avec une taille "raisonnable", puis on auto-scale.
    def _mt_final(s: str) -> MathTex:
        if use_align_env:
            return MathTex(s, font_size=final_font_size, tex_environment="align*")
        return MathTex(s, font_size=final_font_size)

    visible_eqs = Group(*[_mt_final(s) for s in visible_formulas]).arrange(DOWN, aligned_edge=align)
    if back_formulas != None:
        back_eqs = Group(*[_mt_final(s) for s in back_formulas]).arrange(DOWN, buff=vbuff)
        eqs = Group(visible_eqs,back_eqs).arrange(RIGHT,buff=.1)
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
    
    def sous_titre(self,soustitre:Text):
        self.scene.play(
            Write(soustitre),
            soustitre.animate.scale(0.5).to_edge(UP),
            run_time=.5
        )
        return soustitre
    
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

    def resolution(self):
        st = self.sous_titre(Text("Résolution"))
        
        visibleformulas = [
            r"(\hat u,\hat v)=\arg\min_{\hat u,\hat v\in\mathbb{R}^N} {{\frac{1}{2}\|u+v-z\|_2^2}} + {{\frac{\lambda}{2}\|Su\|_2^2}} + {{\mu\|Dv\|_1}}",
            r"\hat v=\arg\min_{v\in\mathbb{R}^N} {{\frac{1}{2}\|u+v-z\|_2^2}} + {{\mu\|Dv\|_1}}",
            r"\hat q=\arg\min_{q\in\mathbb{R}^N} {{f^*(-D^T q)}} + {{g^*(q)}}",
            r"\hat q=\arg\min_{q\in\mathbb{R}^N} {{\frac{1}{2}\|-D^T q+(z-u)\|_2^2}} - {{\frac{1}{2}\|z-u\|_2^2}} + {{\iota_{\|q\|_\infty\le\mu}}}",
            r"\hat q=\arg\min_{q\in\mathbb{R}^N} {{\frac{1}{2}\|-D^T q+(z-u)\|_2^2}} + {{\iota_{\|q\|_\infty\le\mu}}}",
            r"F(q)={{\frac{1}{2}\|-D^T q+(z-u)\|_2^2}}",
            r"q_{k+1}={{\operatorname{prox}_{\gamma G}}}\left({{q_k}}-{{\gamma\nabla F(q_k)}}\right)",
            r"q_{k+1}={{q_k}}-{{\gamma\nabla F(q_k)}}-{{\gamma\operatorname{prox}_{\frac{\mu}{\gamma}\|\cdot\|_1}}}\left({{\frac{q_k}{\gamma}}}-{{\nabla F(q_k)}}\right)",

        ]

        back_formulas = [
        r"f^*(\cdot)={{\frac{1}{2}\|\cdot+(z-u)\|_2^2}}-{{\frac{1}{2}\|z-u\|_2^2}}",
        r"\nabla f^*(\cdot)={{\cdot}}+{{z-u}}",
        r"F(q)={{\frac{1}{2}\|-D^T q+(z-u)\|_2^2}}",
        r"\nabla F(q)={{D^T(D^T q+(u-z))}}",

        ]

        gallery = animate_equation_gallery(self.scene, visibleformulas,back_formulas,font_size=50,final_font_size=25)
        self.scene.wait(1)
        self.scene.play(FadeOut(*gallery),FadeOut(st))
    
    def algorithme(self):
        st = self.sous_titre(Text("Algorithme"))
        visibleformulas = [
            r"\qquad p_{k+1}={{p_k}}-{{\gamma_{1}\nabla F_{1}(p_k)}}-{{\gamma_{1}\operatorname{prox}_{\frac{\lambda}{\gamma_{1}}\|\cdot\|_2}}}\left({{\frac{p_k}{\gamma_{1}}}}-{{\nabla F_{1}(p_k)}}\right)",
            r"\qquad q_{k+1}={{q_k}}-{{\gamma_{2}\nabla F_{2}(q_k)}}-{{\gamma_{2}\operatorname{prox}_{\frac{\mu}{\gamma_{2}}\|\cdot\|_1}}}\left({{\frac{q_k}{\gamma_{2}}}}-{{\nabla F_{2}(q_k)}}\right)",
            
            r"  u = -S^{T}p",
            r"  v = -D^{T}q",
        ]

        back_formulas = []

        gallery = animate_equation_gallery(self.scene, visibleformulas,back_formulas,font_size=50)
        boucle_for = MathTex(r"for(k : Niter):").to_edge(LEFT)
        boucle_for.next_to(gallery,UP).scale(.7).shift(LEFT*4)
        self.scene.play(FadeIn(boucle_for))
        self.scene.wait(1)
        self.scene.play(FadeOut(*gallery),FadeOut(st),FadeOut(boucle_for))
    
    def conjugue(self):
        st = self.sous_titre(Text("Fonctions conjuguées"))

        visibleformulas2 = [
            r"\min_{ {{x\in\mathbb{R}^N}} } \, {{f(x)}} + {{g(\Gamma x)}}",
            r"\min_{ {{u\in\mathbb{R}^M}} } \, {{f^{*}(-\Gamma^{\top} u)}} + {{g^{*}(u)}}",
            r"\min_{ {{x}} } \, {{f(x)}} + {{g(\Gamma x)}} = - \min_{ {{u}} } \, {{f^{*}(-\Gamma^{\top} u)}} + {{g^{*}(u)}}",
            r"\hat{{x}} = {{\nabla f^{*}(-\Gamma^{\top} \hat{{u}})}}",
        ]

        visibleformulas1 = [
            r"f^{*}(u) = \sup_{x \in \mathbb{R}^{N}} \left( \langle u,x\rangle - f(x) \right)",
            r"\left( \frac{1}{2}\|\cdot\|_2^2 \right)^{*} = \frac{1}{2}\|\cdot\|_2^2",
            r"\left( \lambda \|\cdot\|_1 \right)^{*} = \iota_{\|\cdot\|_{\infty} \le \lambda}",

        ]
        back_formulas = []

        gallery = animate_equation_gallery(self.scene, visibleformulas1,back_formulas,font_size=50)
        self.scene.wait(1)
        self.scene.play(FadeOut(*gallery))
        self.scene.play(FadeOut(*gallery),FadeOut(st))
        st = self.sous_titre(Text("Passage au dual"))
        gallery = animate_equation_gallery(self.scene, visibleformulas2,back_formulas,font_size=50)
        self.scene.play(FadeOut(*gallery),FadeOut(st))


    def op_prox(self):
        st = self.sous_titre(Text("Opérateur proximal"))
        vf = [
            r"prox_{\gamma f}(x)=\arg\min_{y\in\mathbb{R}^n}\left(f(y)+\frac{1}{2\gamma}\|y-x\|_2^2\right)"
        ]
        gallery = animate_equation_gallery(self.scene, vf,[],font_size=50)
        self.scene.wait(1)
        self.scene.play(FadeOut(*gallery),FadeOut(st))


    def play(self):
        self.conjugue()
        self.op_prox()
        self.resolution()
        self.algorithme()