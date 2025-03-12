import matplotlib.pyplot as plt
import io
from PIL import Image


def create_graph(delta_uf_values, ges_system, ges_material, delta_uf, intersection_uf, intersection_ges):
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.subplots_adjust(bottom=0.25)

    ax.fill_between(delta_uf_values, 0, ges_material, color='blue', alpha=0.3, label="Réutilisation préférable")
    ax.fill_between(delta_uf_values, ges_material, max(ges_system.max(), ges_material.max()), color='red', alpha=0.3,
                    label="Remplacement optimal")

    ax.plot(delta_uf_values, ges_system, 'r--', label="GES évités Exploitation")
    ax.plot(delta_uf_values, ges_material, 'b-', label="GES émis nouveau cadre")

    ax.axvline(delta_uf, color='green', linestyle=':', label=f"ΔUf = {delta_uf:.2f}")

    if intersection_uf is not None:
        ax.scatter(intersection_uf, intersection_ges, color='black', zorder=3)
        ax.annotate(f"Point d'équilibre\n({intersection_uf:.2f})", (intersection_uf, intersection_ges),
                    textcoords="offset points", xytext=(-40, 10), ha='center', fontsize=10, fontweight='bold',
                    color="black")

    ax.set_xlabel("ΔUf (W/m².K)")
    ax.set_ylabel("GES (kgCO₂/m²)")
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False)
    ax.set_title("Analyse des émissions de GES en fonction de ΔUf")
    ax.grid()

    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    img = Image.open(buf)
    return img
