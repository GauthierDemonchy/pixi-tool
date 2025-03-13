import numpy as np
import matplotlib.pyplot as plt
import io
from PIL import Image
from data import data, coefficients  # Importation des données depuis data.py

def estimate_uf(year, frame_type):
    """
    Estime Uf du cadre existant en fonction de l'année et du type de cadre
    via une régression linéaire entre les années 1950 et 2020.
    """
    # Années de référence
    x = np.array([1950, 2020])
    # Valeurs Uf correspondantes
    y = np.array(data[frame_type])

    # Calcul de la pente (coefficient directeur)
    slope = (y[1] - y[0]) / (x[1] - x[0])
    # Calcul de l'ordonnée à l'origine
    intercept = y[0] - slope * x[0]

    # Prédiction de Uf pour l'année donnée
    return slope * year + intercept


def calculate_and_plot(system, material, uf_existing, uf_new):
    # Vérifier que Uf du nouveau cadre est inférieur à Uf de l'ancien cadre
    if uf_new >= uf_existing:
        return "Erreur : Uf du nouveau cadre doit être inférieur à Uf de l'ancien cadre.", None

    a_system, b_system = coefficients[system]
    a_material, b_material = coefficients[material]

    # Calcul de Delta_Uf
    delta_uf = float(uf_existing) - float(uf_new)

    # Définition des valeurs de Delta_Uf pour le tracé
    delta_uf_values = np.linspace(0, 1.4, 100)
    ges_system = a_system * delta_uf_values + b_system
    ges_material = a_material * delta_uf_values + b_material

    # Trouver l'intersection entre les deux courbes (GES évités et GES émis)
    def find_intersection(a1, b1, a2, b2):
        if a1 != a2:  # Si les pentes sont différentes, on peut calculer l'intersection
            intersection_uf = (b2 - b1) / (a1 - a2)
            intersection_ges = a1 * intersection_uf + b1
            return intersection_uf, intersection_ges
        else:
            return None, None  # Si les pentes sont égales, les lignes sont parallèles et n'ont pas d'intersection

    intersection_uf, intersection_ges = find_intersection(a_system, b_system, a_material, b_material)

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
    plt.subplots_adjust(bottom=0.25)

    # Zone de réutilisation (bleue) - sous la courbe des GES du cadre et Zone de remplacement (rouge)
    ax.fill_between(delta_uf_values, 0, ges_material, color='blue', alpha=0.2, label="Réutilisation préférable")
    ax.fill_between(delta_uf_values, ges_material, max(ges_system.max(), ges_material.max()), color='red', alpha=0.2, label="Remplacement optimal")

    # Tracé des courbes
    ax.plot(delta_uf_values, ges_system, 'r--', label=f"GES évités Exploitation ({system})")
    ax.plot(delta_uf_values, ges_material, 'b-', label=f"GES émis nouveau cadre ({material})")

    # Ligne verticale pour ΔUf choisi
    ax.axvline(delta_uf, color='green', linestyle=':', label=f"ΔUf = {delta_uf:.2f}")

    # Affichage du point d'intersection (ancien point d'équilibre)
    if intersection_uf is not None:
        ax.scatter(intersection_uf, intersection_ges, color='black', zorder=3)
        ax.annotate(f"Point d'équilibre\n({intersection_uf:.2f})", (intersection_uf, intersection_ges),
                    textcoords="offset points", xytext=(-40, 5), ha='center', fontsize=10, fontweight='bold', color="black")

    # Affichage du nouveau point d'intersection avec la droite verticale
    ax.scatter(intersection_vertical_uf, ges_at_intersection_ges_system, color='purple', zorder=3)
    ax.annotate(f"Cas actuel\n({intersection_vertical_uf:.2f})", (intersection_vertical_uf, ges_at_intersection_ges_system),
                textcoords="offset points", xytext=(+35, -25), ha='center', fontsize=10, fontweight='bold', color="purple")

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
