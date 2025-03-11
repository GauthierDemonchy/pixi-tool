import gradio as gr
import matplotlib.pyplot as plt
import numpy as np


def calcul_imc(poids, taille):
    """
    Fonction pour calculer l'IMC et afficher un graphique.
    """
    # Calcul de l'IMC
    imc = poids / ((taille/100) ** 2)

    # Créer un graphique
    fig, ax = plt.subplots()
    ax.plot([0, 1], [18.5, 18.5], label='Seuil sous-poids', color='red', linestyle='--')
    ax.plot([0, 1], [24.9, 24.9], label='Seuil normal', color='green', linestyle='--')
    ax.plot([0, 1], [29.9, 29.9], label='Seuil surpoids', color='orange', linestyle='--')

    ax.scatter(0.5, imc, color='blue', label=f'IMC={imc:.2f}', zorder=5)
    ax.set_title(f'IMC: {imc:.2f}')
    ax.set_ylim(10, 40)
    ax.set_ylabel('IMC')
    ax.set_xticks([])

    # Ajouter les légendes
    ax.legend()

    return fig


# Interface Gradio
iface = gr.Interface(
    fn=calcul_imc,
    inputs=[gr.Number(label="Poids (kg)"), gr.Number(label="Taille (cm)")],
    outputs=gr.Plot()
)

# Lancer l'application Gradio
iface.launch()

