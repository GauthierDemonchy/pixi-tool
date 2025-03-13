import gradio as gr
from calculs import calculate_and_plot, estimate_uf  # Importation des fonctions

# Message explicatif
description = """
### Ce calculateur vous aide à évaluer si le remplacement des cadres de fenêtres est optimal ou s'il est préférable de les réutiliser.

Il compare :

🔴 **Les émissions de GES évitées** grâce à une meilleure performance thermique (chauffage)  
🔵 **Les émissions de GES dues** à la fabrication du nouveau cadre  

Si le point de croisement est atteint, le remplacement est intéressant. Sinon, la réutilisation est préférable !  

💡 **Attention :** Uf du nouveau cadre doit être inférieur à celui de l'ancien.
"""


# Fonction de gestion des entrées utilisateur
def handle_input(system, material, uf_known, uf_existing, year, frame_type, uf_new):
    if uf_new <= 0:
        return "⚠️ Veuillez entrer une valeur de Uf valide pour le nouveau cadre.", None

    if uf_known == "Je connais le Uf du cadre existant":
        if uf_existing is None or uf_existing <= 0:
            return "⚠️ Veuillez entrer une valeur de Uf valide pour l'ancien cadre.", None
        result_text, img = calculate_and_plot(system, material, uf_existing, uf_new)
        return result_text, img

    if uf_known == "Je ne connais pas le Uf, je connais l'année et le type de cadre":
        if not year or not frame_type:
            return "⚠️ Veuillez entrer l'année et le type de cadre.", None
        uf_existing = estimate_uf(year, frame_type)
        result_text, img = calculate_and_plot(system, material, uf_existing, uf_new)
        return result_text, img

    return "⚠️ Informations incomplètes. Vérifiez vos entrées.", None


# Mise à jour dynamique de la visibilité des champs
def update_visibility(uf_known):
    is_known = uf_known == "Je connais le Uf du cadre existant"
    return gr.update(visible=is_known), gr.update(visible=not is_known), gr.update(visible=not is_known)


# Interface Gradio
with gr.Blocks(css="styles.css") as demo:
    gr.Markdown(description)

    # Système de chauffage et Matériau
    with gr.Row():
        system = gr.Radio(["Pac COPA 2.7", "Pac COPA 5.3", "Chaudière gaz naturel"], label="Système de chauffage")
        material = gr.Radio(["Cadre bois", "Cadre bois métal", "Cadre PVC", "Cadre alu"],
                            label="Matériau du nouveau cadre")
    # Uf du nouveau cadre
    uf_new = gr.Number(label="Uf du cadre nouveau (W/m².K)")

    # Mode d'entrée du Uf
    uf_known = gr.Radio(
        ["Je connais le Uf du cadre existant", "Je ne connais pas le Uf, je connais l'année et le type de cadre"],
        label="Comment voulez-vous entrer le Uf du cadre existant ?")

    # Champs dépendants
    uf_existing = gr.Number(label="Uf cadre existant (W/m².K)", visible=False)
    with gr.Row():
        year = gr.Number(label="Année du bâtiment", visible=False)
        frame_type = gr.Radio(["Bois", "Bois-métal", "PVC", "Alu"], label="Type de cadre existant", visible=False)


    # Mettre à jour la visibilité
    uf_known.change(fn=update_visibility, inputs=uf_known, outputs=[uf_existing, year, frame_type])

    # Bouton et résultats
    submit_button = gr.Button("Calculer")
    result = gr.Textbox(label="Résultat")
    image_output = gr.Image(label="Graphique")

    submit_button.click(fn=handle_input, inputs=[system, material, uf_known, uf_existing, year, frame_type, uf_new],
                        outputs=[result, image_output])

# Lancer l'interface
demo.launch()
