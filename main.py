from flask import Flask, render_template, request, redirect, url_for
import openai, json, os
from datetime import datetime

app = Flask(__name__)
openai.api_key = "sk-..."  # ta clé ici

HISTORIQUE_FILE = "historique.json"

def build_prompt(data, schema=False):
    composants = {
        'cuivre': "copper spiral",
        'amethyste': "amethyst crystals",
        'quartz': "clear quartz",
        'obsidienne': "obsidian",
        'lapis': "lapis lazuli",
        'tourmaline': "black tourmaline"
    }

    effets = {
        'galaxie': "galaxy swirl effect",
        'chakra': "chakra rainbow energy glow",
        'feu': "lava and fire-like patterns",
        'glace': "icy and blue crystalline look"
    }

    styles = {
        'spirituel': "sacred geometry, ethereal, spiritual light",
        'blueprint': "technical blueprint, schematic drawing",
        'realiste': "hyper-realistic lighting and textures"
    }

    prompt_parts = ["Highly detailed illustration of an orgonite pyramid"]

    selected_comps = [v for k, v in composants.items() if k in data]
    if selected_comps:
        prompt_parts.append("made with " + ", ".join(selected_comps))

    if 'effet' in data and data['effet'] in effets:
        prompt_parts.append(f"with {effets[data['effet']]}")

    if not schema:
        if 'style' in data and data['style'] in styles and data['style'] != 'blueprint':
            prompt_parts.append(styles[data['style']])
        prompt_parts.append("4K, cinematic light, magical energy, fantasy vibe")
    else:
        prompt_parts.append("technical blueprint of the same object, schematic view, clean lines, monochrome")

    return ". ".join(prompt_parts)

def save_to_history(prompt, url_image, url_schema):
    entry = {
        "date": datetime.now().isoformat(),
        "prompt": prompt,
        "image": url_image,
        "schema": url_schema
    }

    if os.path.exists(HISTORIQUE_FILE):
        with open(HISTORIQUE_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = []

    history.insert(0, entry)

    with open(HISTORIQUE_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

@app.route("/", methods=["GET", "POST"])
def index():
    image_url = None
    schema_url = None

    if request.method == "POST":
        prompt = build_prompt(request.form, schema=False)
        prompt_schema = build_prompt(request.form, schema=True)

        try:
            img_response = openai.Image.create(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                n=1
            )
            image_url = img_response["data"][0]["url"]

            schema_response = openai.Image.create(
                model="dall-e-3",
                prompt=prompt_schema,
                size="1024x1024",
                n=1
            )
            schema_url = schema_response["data"][0]["url"]

            save_to_history(prompt, image_url, schema_url)

        except Exception as e:
            image_url = f"Erreur : {e}"

    return render_template("index.html", image_url=image_url, schema_url=schema_url)

@app.route("/historique")
def historique():
    if os.path.exists(HISTORIQUE_FILE):
        with open(HISTORIQUE_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = []

    return render_template("historique.html", history=history)
