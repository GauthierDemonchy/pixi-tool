
# Données pour la régression Uf selon le type de cadre
data = {
    "Bois": [1.8, 0.9],
    "Bois-métal": [1.8, 1],
    "PVC": [1.8, 1.3],
    "Alu": [3.6, 1.35]
}

# Coefficients des systèmes et matériaux pour le calcul des GES
coefficients = {
    "Pac COPA 2.7": (0.086, 0.000),
    "Pac COPA 5.3": (0.143, 0.000),
    "Chaudière gaz naturel": (0.575, 0.000),
    "Cadre bois": (0.000, 0.041),
    "Cadre bois métal": (0.000, 0.074),
    "Cadre PVC": (0.000, 0.072),
    "Cadre alu": (0.000, 0.149),
}
