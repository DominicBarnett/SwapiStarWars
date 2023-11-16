from flask import Flask, render_template, request
import requests

app = Flask(__name__)

SWAPI_BASE_URL = "https://swapi.py4e.com/api/"

@app.route("/", methods=["GET", "POST"])
def index():
    data = None

    if request.method == "POST":
        category = request.form.get("category")
        entry_id = request.form.get("entry_id")
        if category and entry_id:
            data = fetch_data(category, entry_id)

    return render_template("index.html", data=data)

def fetch_data(category, entry_id):
    try:
        response = requests.get(f"{SWAPI_BASE_URL}{category}/{entry_id}")
        response.raise_for_status()
        entry_data = response.json()

        related_data_keys = ["films", "species", "vehicles", "starships"]
        for key in related_data_keys:
            if key in entry_data:
                related_data = []
                for item_url in entry_data[key]:
                    item_data = fetch_related_data(key, item_url)
                    if item_data:
                        related_data.append(item_data["name"] if "name" in item_data else item_data["title"])
                entry_data[key] = related_data

        return entry_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from SWAPI: {e}")
        return None

def fetch_related_data(category, item_url):
    try:
        response = requests.get(item_url)
        response.raise_for_status()
        item_data = response.json()
        return item_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {category} data from SWAPI: {e}")
        return None

if __name__ == "__main__":
    app.run(debug=True)
