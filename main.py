from flask import Flask, render_template, request
import openai

app = Flask(__name__)
openai.api_key = "sk-..."  # ta clé ici

def build_prompt(data):
    composants = {
        'cuivre': "copper spiral",
        'amethyste': "amethyst crystals",
        'quartz': "clear quartz",
        'obsidienne': "obsidian",
        'lapis': "lapis lazuli",
        'tourmaline': "black tourmaline"
    }

    couleurs = {
        'galaxie': "galaxy swirl effect",
        'chakra': "chakra rainbow energy glow",
        'feu': "lava and fire-like patterns",
        'glace': "icy and blue crystalline look"
    }

    style = {
        'spirituel': "sacred geometry, ethereal, spiritual light",
        'blueprint': "technical blueprint, schematic drawing",
        'realiste': "hyper-realistic lighting and textures",
    }

    prompt_parts = ["Highly detailed image of an orgonite pyramid"]

    # Ajouter les composants sélectionnés
    selected_comps = [v for k, v in composants.items() if k in data]
    if selected_comps:
        prompt_parts.append("made with " + ", ".join(selected_comps))

    # Ajouter les effets visuels
    if 'effet' in data and data['effet'] in couleurs:
        prompt_parts.append(f"with {couleurs[data['effet']]}")

    # Ajouter le style global
    if 'style' in data and data['style'] in style:
        prompt_parts.append(style[data['style']])

    # Effet visuel final
    prompt_parts.append("4K, dramatic lighting, cinematic, magical atmosphere")

    return ". ".join(prompt_parts)

@app.route("/", methods=["GET", "POST"])
def index():
    image_url = None
    if request.method == "POST":
        prompt = build_prompt(request.form)

        try:
            response = openai.Image.create(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                n=1
            )
            image_url = response['data'][0]['url']
        except Exception as e:
            image_url = f"Erreur : {e}"

    return render_template("index.html", image_url=image_url)
