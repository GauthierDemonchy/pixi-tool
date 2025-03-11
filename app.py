import numpy as np
import gradio as gr
import matplotlib.pyplot as plt
import io
from PIL import Image


def calculate_and_plot(system, material):
    # Coefficients des droites (a * Delta_Uf + b)
    coefficients = {
        "Pac COPA 2.7": (0.143, 0.000),
        "Pac COPA 5.3": (0.086, 0.000),
        "Chaudière gaz naturel": (0.575,0.000),
        "Cadre bois": (0.000, 0.041),
        "Cadre bois métal": (0.000, 0.074),
        "Cadre PVC": (0.000, 0.072),
    }

    a_system, b_system = coefficients[system]
    a_material, b_material = coefficients[material]

    # Définition de Delta_Uf
    delta_uf = np.arange(0, 1.4, 0.1)

    # Calcul des valeurs GES
    ges_system = a_system * delta_uf + b_system
    ges_material = a_material * delta_uf + b_material

    # Trouver l'intersection avec interpolation linéaire
    def find_intersection(delta_uf, ges_system, ges_material):
        for i in range(len(delta_uf) - 1):
            # Si les courbes passent de l'autre côté (changement de signe)
            if (ges_system[i] - ges_material[i]) * (ges_system[i + 1] - ges_material[i + 1]) < 0:
                # Interpolation linéaire pour trouver l'intersection exacte
                x1, x2 = delta_uf[i], delta_uf[i + 1]
                y1, y2 = ges_system[i] - ges_material[i], ges_system[i + 1] - ges_material[i + 1]
                # Formule d'interpolation linéaire
                intersection_uf = x1 - y1 * (x2 - x1) / (y2 - y1)
                intersection_ges = a_system * intersection_uf + b_system  # ou a_material * intersection_uf + b_material
                return intersection_uf, intersection_ges
        return None, None

    # Trouver l'intersection
    intersection_uf, intersection_ges = find_intersection(delta_uf, ges_system, ges_material)

    # Création de la figure
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(delta_uf, ges_system, 'r--', label=f"GES évités Exploitation ({system})")
    ax.plot(delta_uf, ges_material, 'b-', label=f"GES émis nouveau cadre ({material})")

    # Marquer le point d'intersection s'il existe
    if intersection_uf is not None:
        ax.scatter(intersection_uf, intersection_ges, color='black', zorder=3)
        ax.annotate(f"Intersection: ({intersection_uf:.2f}, {intersection_ges:.2f})",
                    (intersection_uf, intersection_ges), textcoords="offset points", xytext=(-30, -10), ha='center')
        decision = f"Point de croisement à ΔUf = {intersection_uf:.2f}. Au-delà, remplacement optimal."
    else:
        decision = "Pas de croisement: réutilisation du cadre préférable."

    ax.set_xlabel("ΔUf (W/m².K)")
    ax.set_ylabel("GES (kgCO₂/m²)")
    ax.legend()
    ax.set_title("Analyse des émissions de GES en fonction de ΔUf")
    ax.grid()

    # Sauvegarde dans un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    # Conversion du buffer en image compatible Gradio
    img = Image.open(buf)

    # Retourner l'image et la décision
    return decision, img


# Interface Gradio
interface = gr.Interface(
    fn=calculate_and_plot,
    inputs=[
        gr.Radio(["Pac COPA 2.7", "Pac COPA 5.3", "Chaudière gaz naturel"], label="Système de chauffage"),
        gr.Radio(["Cadre alu", "Cadre bois", "Cadre bois métal", "Cadre PVC"], label="Matériau du cadre"),
    ],
    outputs=["text", "image"]
)

interface.launch()
