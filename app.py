import gradio as gr
from calculs import calculate_and_plot, estimate_uf  # Importation des fonctions

# Message explicatif
description = """
### Ce calculateur vous aide à évaluer si le remplacement des cadres de fenêtres est optimal ou s'il est préférable de les réutiliser.

Il compare :

🔴 **Les émissions de GES évitées** grâce à une meilleure performance thermique (chauffage)  
🔵 **Les émissions de GES dues** à la fabrication du nouveau cadre  

Si le point de croisement est atteint, le remplacement des cadres est intéressant. Sinon, la réutilisation est la solution optimal sur l'aspect environnemental !  

💡 **Attention :** Uf du nouveau cadre doit être inférieur à celui de l'ancien.
"""

# Définition des choix possibles
options_chauffage = {
    "Pompe à chaleur": ["Pac COPA 2,7",  "Pac COPA 3,2", "Pac COPA 4,4", "Pac COPA 5,3"],
    "Chaudiere": ["Chaudiere gaz naturel", "Chaudiere pellet", "Chaudiere buche", "Chaudiere biogaz"]
}

# Mise à jour des options de chauffage dynamiquement
def update_heating_options(choice):
    return gr.update(choices=options_chauffage[choice], value=options_chauffage[choice][0])

# Fonction de gestion des entrées utilisateur
def handle_input(heating_type, system, material, uf_known, uf_existing, year, frame_type, uf_new):
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
with gr.Blocks(css="""
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        width: 100%;
    }
""") as demo:

    with gr.Row(elem_classes="header-container"):
        gr.Markdown(description)
        gr.Image("picture_1.jpeg", elem_id="top-right-image", show_label=False, container=False, width=250, height=250)

    # Sélection du type de chauffage
    with gr.Row():
        heating_type = gr.Radio(["Pompe à chaleur", "Chaudiere"], label="Type de chauffage", value="Pompe à chaleur")
        system = gr.Dropdown(choices=options_chauffage["Pompe à chaleur"], label="Système de chauffage")

    # Mise à jour dynamique des systèmes de chauffage
    heating_type.change(fn=update_heating_options, inputs=heating_type, outputs=system)

    # Sélection du matériau
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
    result = gr.Textbox(label="Résultat",container=False)
    image_output = gr.Image(label="Graphique",container=False)

    submit_button.click(fn=handle_input, inputs=[heating_type, system, material, uf_known, uf_existing, year, frame_type, uf_new],
                        outputs=[result, image_output])

# Lancer l'interface
demo.launch()
