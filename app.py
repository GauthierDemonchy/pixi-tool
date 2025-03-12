import gradio as gr
from calculs import calculate_and_plot, estimate_uf  # Importation de la fonction de calcul

# Message explicatif
description = """
### <span style="font-size: 24px;">Ce calculateur vous aide à évaluer si le remplacement des cadres de fenêtres est optimal ou s'il est préférable de les réutiliser.  
Il compare :  
🔴 **Les émissions de GES évitées** grâce à une meilleure performance thermique (chauffage)  
🔵 **Les émissions de GES dues** à la fabrication du nouveau cadre  
Si le point de croisement est atteint, le remplacement est intéressant. Sinon, la réutilisation est préférable !  
💡 **Attention :** Uf du nouveau cadre doit être inférieur à celui de l'ancien.</span>
"""

# Fonction pour gérer l'entrée utilisateur
def handle_input(system, material, uf_known, uf_existing, year, frame_type, uf_new):
    if uf_known == "Je connais le Uf du cadre existant":
        # Si l'utilisateur connaît le Uf existant, on prend sa valeur
        result_text, img = calculate_and_plot(system, material, uf_existing, uf_new)
        return result_text, img

    if uf_known == "Je ne connais pas le Uf, je connais l'année et le type de cadre":
        if year and frame_type:
            uf_existing = estimate_uf(year, frame_type)
            result_text, img = calculate_and_plot(system, material, uf_existing, uf_new)
            return result_text, img

    return "Veuillez fournir des informations complètes pour le calcul.", None

# Fonction pour mettre à jour la visibilité des champs
def update_visibility(uf_known):
    if uf_known == "Je connais le Uf du cadre existant":
        return gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)  # Afficher uf_existing
    else:
        return gr.update(visible=False), gr.update(visible=True), gr.update(visible=True)  # Afficher year et frame_type

# Créer l'interface avec gr.Blocks() et appliquer le fichier CSS
with gr.Blocks(css="styles.css") as demo:  # Assurez-vous que le fichier CSS est au bon endroit
    # Affichage de la description avec la classe CSS
    gr.Markdown(description)

    # Champs d'entrée
    system = gr.Radio(["Pac COPA 2.7", "Pac COPA 5.3", "Chaudière gaz naturel"], label="Système de chauffage")
    material = gr.Radio(["Cadre bois", "Cadre bois métal", "Cadre PVC", "Cadre alu"], label="Matériau du nouveau cadre")
    uf_known = gr.Radio(
        ["Je connais le Uf du cadre existant", "Je ne connais pas le Uf, je connais l'année et le type de cadre"],
        label="Comment voulez-vous entrer le Uf du cadre existant ?")
    uf_existing = gr.Number(label="Uf cadre existant (W/m².K)", visible=False)
    year = gr.Number(label="Année du bâtiment", visible=False)
    frame_type = gr.Radio(["Bois", "Bois-métal", "PVC", "Alu"], label="Type de cadre existant", visible=False)
    uf_new = gr.Number(label="Uf du cadre nouveau (W/m².K)")

    # Mettre à jour la visibilité des champs
    uf_known.change(fn=update_visibility, inputs=uf_known, outputs=[uf_existing, year, frame_type])

    # Bouton de soumission
    submit_button = gr.Button("Calculer")

    # Résultat
    result = gr.Textbox()
    image_output = gr.Image()  # Ajout d'une sortie pour l'image

    # Quand le bouton est cliqué, on appelle handle_input
    submit_button.click(fn=handle_input, inputs=[system, material, uf_known, uf_existing, year, frame_type, uf_new],
                        outputs=[result, image_output])

# Lancer l'interface
demo.launch()
