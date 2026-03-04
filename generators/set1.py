import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def make_viz(output_folder: str = "out", export_dpi: int = 200) -> None:
    """
    Generates 6 Weber’s Law stimulus images (3 pairs) and a questions.txt file.

    Output:
      <output_folder>/
        V1_bar_no_aids.png
        V2_bar_gridlines.png
        V3_line_no_aids.png
        V4_line_gridlines.png
        V5_dots_no_aids.png
        V6_dots_boxes.png
        questions.txt
    """
    os.makedirs(output_folder, exist_ok=True)

    def save_figure(fig, filename) -> str:
        path = os.path.join(output_folder, filename)
        fig.tight_layout()
        fig.savefig(path, dpi=export_dpi, bbox_inches="tight")
        plt.close(fig)
        return path

    items = []
    items += _build_bar_pair(save_figure)
    items += _build_line_pair(save_figure)
    items += _build_dot_count_pair(save_figure)

    questions_path = _write_questions(output_folder, items)

    print(f"Saved files to: {os.path.abspath(output_folder)}")
    print(f"Questions file: {os.path.abspath(questions_path)}")
    for image_path, _, _ in items:
        print(" -", os.path.basename(image_path))


def _build_bar_pair(save_figure):
    district_names = ["Riverton", "Northvale", "Marigold", "Eastpoint", "Cedar Bay", "Doverfield"]
    broken_hydrant_percent = np.array([12.20, 12.725, 12.43, 12.59, 12.00, 12.51], dtype=float)

    y_min, y_max = 11.90, 13.10
    y_ticks = np.arange(y_min, y_max + 1e-9, 0.05)

    fig, ax = plt.subplots(figsize=(8.6, 4.0))
    ax.bar(district_names, broken_hydrant_percent, width=0.7)
    ax.set_ylim(y_min, y_max)
    ax.set_yticks(y_ticks)
    ax.grid(axis="y", alpha=0.0)
    ax.set_title("V1 — Percent of Broken Fire Hydrants (Astra City Districts)")
    ax.tick_params(axis="x", rotation=20)
    p1 = save_figure(fig, "V1_bar_no_aids.png")

    fig, ax = plt.subplots(figsize=(8.6, 4.0))
    ax.bar(district_names, broken_hydrant_percent, width=0.7)
    ax.set_ylim(y_min, y_max)
    ax.set_yticks(y_ticks)
    ax.grid(axis="y", alpha=0.35)
    ax.set_title("V2 — Percent of Broken Fire Hydrants (Astra City Districts)")
    ax.tick_params(axis="x", rotation=20)
    p2 = save_figure(fig, "V2_bar_gridlines.png")

    return [
        (p1, "Which percent difference is larger: Riverton vs Northvale, or Cedar Bay vs Doverfield?", "Riverton vs Northvale"),
        (p2, "Which percent difference is larger: Riverton vs Northvale, or Cedar Bay vs Doverfield?", "Riverton vs Northvale"),
    ]


def _build_line_pair(save_figure):
    price_points = np.linspace(10.0, 60.0, 26)

    p = price_points
    curve_a = 130.0 + 28.0 * np.sin((p - 12.0) / 7.5) - 1.35 * p + 0.018 * (p - 34.0) ** 2
    curve_b = 118.0 + 24.0 * np.cos((p + 4.0) / 8.2) - 1.05 * p + 0.030 * (p - 42.0) ** 2

    demand_curves = {
        "Product Alder": np.clip(curve_a, 0.0, None),
        "Product Birch": np.clip(curve_b, 0.0, None),
    }

    y_min, y_max = 0.0, 170.0
    y_ticks = np.arange(y_min, y_max + 1e-9, 10.0)

    fig, ax = plt.subplots(figsize=(8.4, 4.0))
    for name, y in demand_curves.items():
        ax.plot(price_points, y, linewidth=1.6, color="0.35", label=name)
    ax.set_xlim(10.0, 60.0)
    ax.set_ylim(y_min, y_max)
    ax.set_yticks(y_ticks)
    ax.grid(True, alpha=0.0)
    ax.set_title("V3 — Demand (Price vs Quantity)")
    ax.set_xlabel("Price (credits)")
    ax.set_ylabel("Quantity (units)")
    ax.legend(frameon=False, loc="upper right")
    p3 = save_figure(fig, "V3_line_no_aids.png")

    fig, ax = plt.subplots(figsize=(8.4, 4.0))
    v4_curves = {
        "Product Alder": demand_curves["Product Alder"],
        "Product Birch": demand_curves["Product Birch"],
    }
    color_list = ["tab:blue", "tab:orange"]
    for (name, y), c in zip(v4_curves.items(), color_list):
        ax.plot(price_points, y, linewidth=1.6, color=c, label=name)
    y1 = v4_curves["Product Alder"]
    y2 = v4_curves["Product Birch"]
    ax.fill_between(price_points, y1, y_min, alpha=0.18, color="tab:blue")
    ax.fill_between(price_points, y2, y_min, alpha=0.18, color="tab:orange")
    ax.set_xlim(10.0, 60.0)
    ax.set_ylim(y_min, y_max)
    ax.set_yticks(y_ticks)
    ax.grid(True, alpha=0.0)
    ax.set_title("V4 — Demand (Filled Area Aid)")
    ax.set_xlabel("Price (credits)")
    ax.set_ylabel("Quantity (units)")
    ax.legend(frameon=False, loc="upper right")
    p4 = save_figure(fig, "V4_line_gridlines.png")

    areas_v3 = {name: float(np.trapezoid(y, price_points)) for name, y in demand_curves.items()}
    correct_product_v3 = max(areas_v3, key=areas_v3.get)
    areas_v4 = {name: float(np.trapezoid(y, price_points)) for name, y in v4_curves.items()}
    correct_product_v4 = max(areas_v4, key=areas_v4.get)
    #Areas of line 1 and line 2 (birch and alder)
    print("alder" , areas_v3["Product Alder"], areas_v4["Product Alder"])
    print("birch" , areas_v3["Product Birch"], areas_v4["Product Birch"])

    return [
        (p3, "From price 12 to 58, which product has the largest total quantity (area under the curve)?", correct_product_v3),
        (p4, "From price 12 to 58, which product has the largest total quantity (area under the curve)?", correct_product_v4),
    ]


def _build_dot_count_pair(save_figure):
    fragrance_names = ["Citrus Sky", "Amber Noir", "Velvet Rose", "Saffron Mist", "Juniper Clean", "Iris Smoke"]
    dot_counts = np.array([169, 177, 181, 183, 195, 188], dtype=int)

    rng = np.random.default_rng(42)

    total_dots = 200

    x = np.arange(len(fragrance_names))

    y_min, y_max = 0.0, 1.0

    fig, ax = plt.subplots(figsize=(9.2, 4.0))
    for i, filled in enumerate(dot_counts):
        xs = i + rng.uniform(-0.30, 0.30, size=filled)
        ys = rng.uniform(0.06, 0.94, size=filled)

        ax.scatter(xs, ys, s=18)

    ax.set_xlim(-0.6, len(fragrance_names) - 0.4)
    ax.set_ylim(y_min, y_max)
    ax.set_xticks(x, fragrance_names)
    ax.tick_params(axis="x", rotation=20)
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title("V5 — Perfume Dot Counts (Filled Dots Only)")
    p5 = save_figure(fig, "V5_dots_no_aids.png")

    fig, ax = plt.subplots(figsize=(9.2, 4.0))
    for i, filled in enumerate(dot_counts):
        xs_all = i + rng.uniform(-0.30, 0.30, size=total_dots)
        ys_all = rng.uniform(0.06, 0.94, size=total_dots)

        ax.scatter(xs_all, ys_all, s=18, facecolors="none", edgecolors="0.65", linewidths=0.9, alpha=0.85)

        xs_fill = xs_all[:filled]
        ys_fill = ys_all[:filled]
        ax.scatter(xs_fill, ys_fill, s=18)

        ax.add_patch(Rectangle((i - 0.38, 0.04), 0.76, 0.92, fill=False, linewidth=1.4, alpha=0.55))

    ax.set_xlim(-0.6, len(fragrance_names) - 0.4)
    ax.set_ylim(y_min, y_max)
    ax.set_xticks(x, fragrance_names)
    ax.tick_params(axis="x", rotation=20)
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title("V6 — Perfume Dot Counts (200-Dot Reference)")
    p6 = save_figure(fig, "V6_dots_boxes.png")

    diff_1 = abs(dot_counts[1] - dot_counts[0])  # Amber Noir - Citrus Sky
    diff_2 = abs(dot_counts[5] - dot_counts[4])  # Iris Smoke - Juniper Clean

    if diff_1 >= diff_2:
        correct = "Amber Noir minus Citrus Sky"
    else:
        correct = "Iris Smoke minus Juniper Clean"

    return [
        (p5, "Which difference is larger: Amber Noir minus Citrus Sky, or Iris Smoke minus Juniper Clean?", correct),
        (p6, "Which difference is larger: Amber Noir minus Citrus Sky, or Iris Smoke minus Juniper Clean?", correct),
    ]

def _write_questions(output_folder, items) -> str:
    path = os.path.join(output_folder, "v1v6_questions.txt")
    lines = ["Questions and answer key\n"]

    for idx, (image_path, question, answer) in enumerate(items, start=1):
        lines.append(f"{idx}. {os.path.basename(image_path)}")
        lines.append(f"   Q: {question}")
        lines.append(f"   Correct: {answer}")
        lines.append("")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return path
