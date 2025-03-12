import numpy as np
import matplotlib.pyplot as plt
import io
from PIL import Image

def calculate_and_plot(system, material, uf_existing, uf_new):
    # Vérifier que Uf du nouveau cadre est inférieur à Uf de l'ancien cadre
    if uf_new >= uf_existing:
        return "Erreur : Uf du nouveau cadre doit être inférieur à Uf de l'ancien cadre.", None

    # Coefficients des droites (a * Delta_Uf + b)
    coefficients = {
        "Pac COPA 2.7": (0.143, 0.000),
        "Pac COPA 5.3": (0.086, 0.000),
        "Chaudière gaz naturel": (0.575, 0.000),
        "Cadre bois": (0.000, 0.041),
        "Cadre bois métal": (0.000, 0.074),
        "Cadre PVC": (0.000, 0.072),
        "Cadre alu": (0.000, 0.149),
    }

    a_system, b_system = coefficients[system]
    a_material, b_material = coefficients[material]

    # Calcul de Delta_Uf
    delta_uf = float(uf_existing) - float(uf_new)

    # Définition des valeurs de Delta_Uf pour le tracé
    delta_uf_values = np.linspace(0, 1.4, 100)
    ges_system = a_system * delta_uf_values + b_system
    ges_material = a_material * delta_uf_values + b_material

    # Trouver l'intersection entre GES évités et GES émis par le producteur de chaleur
    def find_intersection(delta_uf_values, ges_system, ges_material):
        for i in range(len(delta_uf_values) - 1):
            if (ges_system[i] - ges_material[i]) * (ges_system[i + 1] - ges_material[i + 1]) < 0:
                x1, x2 = delta_uf_values[i], delta_uf_values[i + 1]
                y1, y2 = ges_system[i] - ges_material[i], ges_system[i + 1] - ges_material[i + 1]
                intersection_uf = x1 - y1 * (x2 - x1) / (y2 - y1)
                intersection_ges = a_system * intersection_uf + b_system
                return intersection_uf, intersection_ges
        return None, None

    intersection_uf, intersection_ges = find_intersection(delta_uf_values, ges_system, ges_material)

    # Trouver l'intersection avec la droite verticale définie par delta_uf
    def find_vertical_intersection(delta_uf, ges_system, ges_material):
        ges_at_delta_uf_system = a_system * delta_uf + b_system
        ges_at_delta_uf_material = a_material * delta_uf + b_material
        return delta_uf, ges_at_delta_uf_system, ges_at_delta_uf_material

    intersection_vertical_uf, ges_at_intersection_ges_system, ges_at_intersection_ges_material = find_vertical_intersection(delta_uf, ges_system, ges_material)

    # Déterminer si le remplacement est optimal
    if intersection_uf is not None:
        if delta_uf >= intersection_uf:
            decision = f"ΔUf = {delta_uf:.2f} entre nouveau cadre et ancien cadre, soit au-dessus du point seuil ({intersection_uf:.2f}) :\n✅ Le remplacement du cadre est optimal."
        else:
            decision = f"ΔUf = {delta_uf:.2f} entre nouveau cadre et ancien cadre, soit en dessous du point seuil ({intersection_uf:.2f}) :\n♻️ La réutilisation du cadre est préférable."
    else:
        decision = "Pas de croisement détecté : ♻️ Réutilisation préférable."

    # Création du graphique
    fig, ax = plt.subplots(figsize=(8, 6))
    plt.subplots_adjust(bottom=0.25)  # Ajoute plus d'espace sous le graphe

    # Zone de réutilisation (bleue) - sous la courbe des GES du cadre et Zone de remplacement (rouge) - au-dessus de la courbe des GES du cadre
    ax.fill_between(delta_uf_values, 0, ges_material, color='blue', alpha=0.3, label="Réutilisation préférable")
    ax.fill_between(delta_uf_values, ges_material, max(ges_system.max(), ges_material.max()), color='red', alpha=0.3, label="Remplacement optimal")

    # Tracé des courbes
    ax.plot(delta_uf_values, ges_system, 'r--', label=f"GES évités Exploitation ({system})")
    ax.plot(delta_uf_values, ges_material, 'b-', label=f"GES émis nouveau cadre ({material})")

    # Ligne verticale pour ΔUf choisi
    ax.axvline(delta_uf, color='green', linestyle=':', label=f"ΔUf = {delta_uf:.2f}")

    # Affichage du point d'intersection (ancien point d'équilibre)
    if intersection_uf is not None:
        ax.scatter(intersection_uf, intersection_ges, color='black', zorder=3)
        ax.annotate(f"Point d'équilibre\n({intersection_uf:.2f})",(intersection_uf, intersection_ges),textcoords="offset points", xytext=(-40, 5),ha='center', fontsize=10, fontweight='bold', color="black")

    # Affichage du nouveau point d'intersection avec la droite verticale
    ax.scatter(intersection_vertical_uf, ges_at_intersection_ges_system, color='purple', zorder=3)
    ax.annotate(f"Cas actuel\n({intersection_vertical_uf:.2f})", (intersection_vertical_uf, ges_at_intersection_ges_system), textcoords="offset points", xytext=(+35, -25), ha='center', fontsize=10, fontweight='bold', color="purple")

    # Paramètres du graphique
    ax.set_xlabel("ΔUf (W/m².K)")
    ax.set_ylabel("GES (kgCO₂/m²)")
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, frameon=False)
    ax.set_title("Analyse des émissions de GES en fonction de ΔUf")
    ax.grid()

    # Sauvegarde dans un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)

    img = Image.open(buf)
    return decision, img
