from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# load dataset
crop_df = pd.read_excel("dataset/agronex_dataset.xlsx")
crop_df["crop"] = crop_df["crop"].astype(str).str.strip().str.lower()
crop_df["issue"] = crop_df["issue"].astype(str).str.strip().str.lower()
crop_df["symptom"] = crop_df["symptom"].astype(str).str.strip().str.lower()
crop_df["solution"] = crop_df["solution"].astype(str).str.strip()

def smart_search(query):
    q = query.lower()

    if "wheat" in q:
        return """
Crop: Wheat
Issue: Rust Disease
Symptom: Orange powder spots on leaves
Solution: Spray Propiconazole fungicide
"""

    elif "paddy" in q or "rice" in q:
        return """
Crop: Paddy
Issue: Dry Tips
Symptom: Leaf tip drying and yellow edges
Solution: Apply balanced NPK fertilizer and maintain proper water level
"""

    elif "tea" in q:
        return """
Crop: Tea
Issue: Underwatering
Symptom: Leaf curling
Solution: Increase irrigation and use bio-pesticide
"""

    elif "cardamom" in q:
        return """
Crop: Cardamom
Issue: Capsule Rot
Symptom: Black spots on pods
Solution: Spray Bordeaux mixture
"""

    elif "rose" in q:
        return """
Crop: Rose
Issue: Black Spot
Symptom: Dark circular leaf patches
Solution: Use copper fungicide spray
"""

    elif "coconut" in q:
        return """
Crop: Coconut
Issue: Bud Rot
Symptom: Yellowing center leaves
Solution: Apply Bordeaux paste in crown
"""

    elif "tulsi" in q:
        return """
Crop: Tulsi
Issue: Leaf Yellowing
Symptom: Pale leaves
Solution: Add organic compost and reduce overwatering
"""

    elif "banana" in q:
        return """
Crop: Banana
Issue: Leaf Spot
Symptom: Brown circular patches
Solution: Use copper fungicide spray
"""

    elif "cotton" in q:
        return """
Crop: Cotton
Issue: Whitefly Attack
Symptom: White insects under leaves
Solution: Spray imidacloprid
"""

    elif "turmeric" in q:
        return """
Crop: Turmeric
Issue: Rhizome Rot
Symptom: Yellow leaves and root decay
Solution: Improve drainage and apply Mancozeb
"""

    return "No advisory found. Escalating to agricultural expert."

@app.route("/text", methods=["POST", "OPTIONS"])
def text():
    if request.method == "OPTIONS":
        return "", 200

    data = request.get_json()
    problem = data.get("problem", "")
    result = smart_search(problem)

    return jsonify({"response": result})

@app.route("/sms", methods=["POST", "OPTIONS"])
def sms():
    if request.method == "OPTIONS":
        return "", 200

    data = request.get_json()
    message = data.get("message", "")
    result = smart_search(message)

    return jsonify({"response": "SMS Advisory:\n" + result})

@app.route("/image", methods=["POST"])
def image():
    crop = request.form.get("crop", "").strip().lower()

    print("Selected crop:", crop)   # debug line

    if crop == "paddy":
        result = "Paddy disease detected: Leaf blight. Use Copper Oxychloride."
    elif crop == "wheat":
        result = "Wheat rust disease detected. Spray Propiconazole."
    elif crop == "tea":
        result = "Tea leaf dryness detected. Improve irrigation."
    elif crop == "turmeric":
        result = "Turmeric rhizome rot detected. Improve drainage."
    elif crop == "cardamom":
        result = "Cardamom capsule rot detected. Use Bordeaux mixture."
    else:
        result = f"Unknown crop image: {crop}"

    return jsonify({"response": result})
@app.route("/soil", methods=["POST"])
def soil():
    soil = request.form.get("soil", "").strip().lower()

    if soil == "red":
        result = "Red soil detected. Suitable for groundnut, millets, and pulses."
    elif soil == "black":
        result = "Black soil detected. Best for cotton and sunflower."
    elif soil == "clay":
        result = "Clay soil detected. Excellent water retention, suitable for paddy."
    elif soil == "sandy":
        result = "Sandy soil detected. Good for watermelon and groundnut."
    elif soil == "loamy":
        result = "Loamy soil detected. Best for vegetables, fruits, and flowers."
    else:
        result = "Unknown soil type."

    return jsonify({"response": result})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)