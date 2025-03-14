import numpy as np
import pandas as pd

# Chargement des facteurs d'émission depuis output1.csv
file_path = "output2.txt"
factors_df = pd.read_csv(file_path, delimiter=";", names=["Producer", "Emission Factor"], dtype=str, encoding="latin1")


# Nettoyage des données
factors_df["Emission Factor"] = factors_df["Emission Factor"].str.replace(",", ".").astype(float)  # Conversion des nombres

# Définition des valeurs de Qh en fonction de Delta Uf établi à partir de lesosai
q_h_values = np.array([0.000,0.250,0.500,0.750,1.000,1.250,1.472,1.722,1.972,2.222,2.472,2.722,2.944])
delta_uf_values = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2])


# Fonction pour calculer les coefficients GES
def calculate_ges_coefficients(producer_name):
    """
    Calcule le coefficient GES (a) en imposant b = 0.
    """
    factor = factors_df.loc[factors_df["Producer"] == producer_name, "Emission Factor"].values
    if len(factor) == 0:
        raise ValueError(f"Facteur d'émission introuvable pour {producer_name}")

    factor = factor[0]
    ges_values = q_h_values * factor

    # Régression linéaire sans intercept (forcée à 0)
    a, _, _, _ = np.linalg.lstsq(delta_uf_values.reshape(-1, 1), ges_values, rcond=None)

    return a[0], 0  # b est forcé à 0


# Calcul des coefficients pour les systèmes de chauffage
coefficients = {
    "Pac COPA 2,7": calculate_ges_coefficients("Pac COPA 2,7"),
    "Pac COPA 5,3": calculate_ges_coefficients("Pac COPA 5,3"),
    "Chaudiere gaz naturel": calculate_ges_coefficients("Chaudiere gaz naturel"),
    "Chaudiere biogaz": calculate_ges_coefficients("Chaudiere biogaz"),
    "Pac COPA 4,4": calculate_ges_coefficients("Pac COPA 4,4"),
    "Pac COPA 3,2": calculate_ges_coefficients("Pac COPA 3,2"),
    "Chaudiere pellet": calculate_ges_coefficients("Chaudiere pellet"),
    "Chaudiere buche": calculate_ges_coefficients("Chaudiere buche"),
    "Cadre bois": (0.000, 0.041),
    "Cadre bois métal": (0.000, 0.074),
    "Cadre PVC": (0.000, 0.072),
    "Cadre alu": (0.000, 0.149),
}

# Affichage des coefficients calculés
for key, value in coefficients.items():
    print(f"{key}: a = {value[0]:.3f}, b = {value[1]:.3f}")

# Données pour la régression Uf selon le type de cadre
data = {
    "Bois": [1.8, 0.9],
    "Bois-métal": [1.8, 1],
    "PVC": [1.8, 1.3],
    "Alu": [3.6, 1.35]
}
