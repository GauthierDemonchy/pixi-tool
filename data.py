
# Données pour la régression Uf selon le type de cadre
data = {
    "Bois": [1.9, 0.7],
    "Bois-métal": [2.1, 0.9],
    "PVC": [1.7, 0.6],
    "Alu": [2.5, 1.5]
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
