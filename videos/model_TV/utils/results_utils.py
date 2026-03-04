from pathlib import Path
import numpy as np
from manim import *


# -----------------------------
# 1) Construction du graphe (sans animation)
# -----------------------------
def build_npz_logy_graph(filepath, keys=None, colors=None):
    """
    Construit un graphe (Axes + ticks/labels + courbes + légende) depuis un .npz
    en log10 sur Y, SANS jouer d'animations.
    Retourne un dict de "parts" pour pouvoir animer finement ensuite.
    """
    data = np.load(filepath)

    if keys is None:
        keys = list(data.keys())

    arrays = [data[k] for k in keys]
    arrays_safe = [np.where(arr <= 0, 1e-12, arr) for arr in arrays]
    arrays_log = [np.log10(arr) for arr in arrays_safe]

    max_len = max(len(arr) for arr in arrays_log)
    y_min = min(arr.min() for arr in arrays_log)
    y_max = max(arr.max() for arr in arrays_log)

    axes = Axes(
        x_range=[0, max_len, 1],
        y_range=[y_min, y_max, 1],
        x_axis_config={"include_ticks": False},
    )

    # Labels Y en 10^k
    y_labels = Group()
    y_ticks = np.arange(np.floor(y_min), np.ceil(y_max) + 1)
    for y in y_ticks:
        if y_min <= y <= y_max:
            lab = MathTex(f"10^{{{int(y)}}}").scale(0.5)
            lab.next_to(axes.y_axis.n2p(y), LEFT, buff=0.1)
            y_labels.add(lab)

    # Ticks/labels X manuels (multiples de 100)
    tick_objs = Group()
    x_values = [x for x in range(100, int(max_len) + 1, 100)]
    tick_length = 0.2
    for x in x_values:
        tick = Line(
            start=axes.coords_to_point(x, 0),
            end=axes.coords_to_point(x, -tick_length * 0.25),
        )
        label = MathTex(f"{x}").scale(0.5)
        label.next_to(axes.x_axis.n2p(x), DOWN, buff=0.1 + tick_length * 0.25)
        tick_objs.add(tick, label)

    # Couleurs par défaut
    if colors is None:
        colors = [BLUE, RED, GREEN, YELLOW, PURPLE, ORANGE]

    graphs = Group()
    legend_items = Group()

    for i, (arr_log, name) in enumerate(zip(arrays_log, keys)):
        color = colors[i % len(colors)]
        g = axes.plot_line_graph(
            x_values=np.arange(len(arr_log)),
            y_values=arr_log,
            line_color=color,
            add_vertex_dots=False,
        )
        graphs.add(g)

        display_name = name.replace("_", " ").capitalize()
        line = Line(LEFT, RIGHT, color=color).scale(0.35)
        text = Text(display_name).scale(0.35)
        legend_item = Group(line, text).arrange(RIGHT, buff=0.25)
        legend_items.add(legend_item)

    legend = legend_items.arrange(DOWN, aligned_edge=LEFT)
    legend.to_corner(UR)

    # Group complet (utile si tu veux juste l’afficher d’un coup)
    full = Group(axes, tick_objs, y_labels, graphs, legend)

    return {
        "full": full,
        "axes": axes,
        "tick_objs": tick_objs,
        "y_labels": y_labels,
        "graphs": graphs,
        "legend": legend,
    }


# -----------------------------
# 2) Animation du graphe (avec scene.play)
# -----------------------------
def animate_npz_logy(scene: Scene, parts: dict, *, run_time_axes=0.8, run_time_ticks=0.6, run_time_graph=0.7):
    scene.play(Create(parts["axes"]), run_time=run_time_axes)
    scene.play(FadeIn(parts["y_labels"]), run_time=0.3)
    scene.play(*[Create(m) for m in parts["tick_objs"]], run_time=run_time_ticks)

    for g in parts["graphs"]:
        scene.play(Create(g), run_time=run_time_graph)

    scene.play(FadeIn(parts["legend"]), run_time=0.4)


# -----------------------------
# 3) Galerie : top images + bottom graphe
# -----------------------------
def make_image_gallery(
    top_items: list[tuple[str, str]],
    bottom_item: tuple[str, str],  # (titre, chemin_npz)
    *,
    top_img_height: float = 2.2,
    bottom_graph_height: float = 2.5,
    title_scale: float = 0.45,
    label_scale: float = 0.40,
    col_buff: float = 0.8,
    row_buff: float = 0.4,

) -> tuple[Group, dict]:
    """
    Retourne (gallery, bottom_graph_parts)
    bottom_graph_parts est un dict utilisable par animate_npz_logy.
    """

    def _one_panel(title: str, img_path: str, label: str, img_height: float) -> Group:
        p = Path(img_path)
        img = ImageMobject(str(p)).set_height(img_height)
        t = Text(title).scale(title_scale)
        lab = Text(label).scale(label_scale)
        return Group(t, img, lab).arrange(DOWN, buff=0.18)

    def _graph_panel(title: str, npz_path: str, label: str, height: float) -> tuple[Group, dict]:
        parts = build_npz_logy_graph(npz_path)
        graph = parts["full"]
        graph.set_height(height)

        t = Text(title).scale(title_scale)
        lab = Text(label).scale(label_scale)
        panel = Group(t, graph, lab).arrange(DOWN, buff=0.18)
        return panel, parts

    # --- Panels du haut ---
    top_panels = Group()
    for i, (title, path) in enumerate(top_items):
        label = f"({chr(ord('A') + i)})"
        top_panels.add(_one_panel(title, path, label, top_img_height))

    top_row = top_panels.arrange(RIGHT, buff=col_buff, aligned_edge=DOWN)

    # --- Panel du bas (graphe) ---
    bottom_label = f"({chr(ord('A') + len(top_items))})"
    bottom_panel, bottom_parts = _graph_panel(
        bottom_item[0],
        bottom_item[1],
        bottom_label,
        bottom_graph_height
    )

    # --- Assemblage global ---
    gallery = Group(top_row, bottom_panel).arrange(DOWN, buff=row_buff)
    bottom_panel.align_to(top_row, ORIGIN)
    gallery.move_to(ORIGIN)


    return gallery, bottom_parts
