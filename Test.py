import gradio as gr


def calculer_imc(poids, taille):
    taille_m = taille / 100  # Convertir en mètres
    if taille_m <= 0 or poids <= 0:
        return "Erreur : valeurs invalides."

    imc = poids / (taille_m ** 2)

    # Déterminer la catégorie
    if imc < 18.5:
        categorie = "Maigreur"
        color = "blue"
    elif 18.5 <= imc < 25:
        categorie = "Corpulence normale"
        color = "green"
    elif 25 <= imc < 30:
        categorie = "Surpoids"
        color = "orange"
    else:
        categorie = "Obésité"
        color = "red"

    return f"<p style='color:{color}; font-size:18px;'>IMC : {imc:.2f} - {categorie}</p>"


interface = gr.Interface(
    fn=calculer_imc,
    inputs=[gr.Number(label="Poids (kg)"), gr.Number(label="Taille (cm)")],
    outputs="html",
    title="Calculateur d'IMC",
    description="Entrez votre poids et votre taille pour calculer votre IMC."
)

interface.launch()
