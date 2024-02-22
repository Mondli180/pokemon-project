from flask import Flask, render_template, request, redirect, jsonify
import requests

app = Flask(__name__)

def get_pokemon_list():
    url = "https://pokeapi.co/api/v2/pokemon?limit=151"
    response = requests.get(url)
    return response.json()["results"]


def get_pokemon_details(pokemon_name):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = requests.get(url)
    return response.json()


def compare_pokemon(pokemon1, pokemon2):
    differences = []

    if pokemon1["height"] != pokemon2["height"]:
        differences.append(
            {"attribute": "Height",  "pokemon1_value": pokemon1["height"],
              "pokemon2_value": pokemon2["height"]})

    if pokemon1["weight"] != pokemon2["weight"]:
        differences.append(
            {"attribute": "Weight",  "pokemon1_value": pokemon1["weight"],
              "pokemon2_value": pokemon2["weight"]})

    if pokemon1["base_experience"] != pokemon2["base_experience"]:
        differences.append({"attribute": "Base Experience",
                            "pokemon1_value": pokemon1["base_experience"],
                            "pokemon2_value": pokemon2["base_experience"]})

    return differences


@app.route("/")
def home():
    pokemon_list = get_pokemon_list()
    return render_template("index.html", pokemon_list=pokemon_list)


@app.route("/view_pokemon_details", methods=["GET"])
def view_pokemon_details():
    selected_pokemon = request.args.get("selected_pokemon")

    if selected_pokemon:
        pokemon_details = get_pokemon_details(selected_pokemon)
        return render_template("pokemon.html", pokemon_details=pokemon_details)
    else:
        return redirect(url_for("home"))

@app.route("/compare", methods=["POST"])
def compare():
    pokemon1_name = request.form.get("pokemon1")
    pokemon2_name = request.form.get("pokemon2")

    pokemon1_details = get_pokemon_details(pokemon1_name)
    pokemon2_details = get_pokemon_details(pokemon2_name)

    differences = compare_pokemon(pokemon1_details, pokemon2_details)
    return render_template("comparison_tab.html", differences=differences,
                           pokemon1_name=pokemon1_name, pokemon2_name=pokemon2_name)

from flask import render_template

@app.route("/filter_pokemon", methods=["POST"])
def filter_pokemon():
    try:
        min_height = int(request.form.get("min_height"))
        max_height = int(request.form.get("max_height"))
        prefix = request.form.get("prefix").lower()

        if not 50 <= min_height <= 1000 or not 50 <= max_height <= 1000:
            raise ValueError("Invalid height range. Height should be between 50 and 1000.")

        filtered_pokemon = [pokemon for pokemon in get_pokemon_list() if
                            'height' in pokemon and
                            min_height <= pokemon['height'] <= max_height and
                            pokemon['name'].lower().startswith(prefix)]

        return render_template("filtered_pokemon.html", success=True, filtered_pokemon=filtered_pokemon)

    except ValueError as e:
        error_message = str(e)
        return render_template("filtered_pokemon.html", success=False, error=error_message)


if __name__ == "__main__":
    app.run(debug=True)
