import gradio as gr
from calculs import calculate_and_plot

# Message explicatif
description = """
###
Ce calculateur vous aide à évaluer si le remplacement des cadres de fenêtres est optimal ou s'il est préférable de les réutiliser.  
Il compare :  
🔴 **Les émissions de GES évitées** grâce à une meilleure performance thermique (chauffage)  
🔵 **Les émissions de GES dues** à la fabrication du nouveau cadre  
Si le point de croisement est atteint, le remplacement est intéressant. Sinon, la réutilisation est préférable !  
💡 **Attention :** Uf du nouveau cadre doit être inférieur à celui de l'ancien.
"""

# Interface Gradio
interface = gr.Interface(
    fn=calculate_and_plot,
    inputs=[
        gr.Radio(["Pac COPA 2.7", "Pac COPA 5.3", "Chaudière gaz naturel"], label="Système de chauffage"),
        gr.Radio(["Cadre bois", "Cadre bois métal", "Cadre PVC", "Cadre alu"], label="Matériau du nouveau cadre"),
        gr.Number(label="Uf cadre existant (W/m².K)"),
        gr.Number(label="Uf nouveau cadre (W/m².K)")
    ],
    outputs=["text", "image"],
    title="Calculateur d'aide à la décision sur le remplacement des cadres de fenêtres",
    description=description
)

interface.launch()
