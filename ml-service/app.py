from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image
from io import BytesIO
import torch
import torchvision.models as models
import torchvision.transforms as transforms

app = Flask(__name__)
CORS(app)

# CNN model will be initialized only when image analysis is requested
cnn_model = None

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
])

def get_cnn_model():
    global cnn_model

    if cnn_model is None:
        cnn_model = models.mobilenet_v2(weights=None)
        cnn_model.eval()

    return cnn_model

def extract_cnn_score(img):
    model = get_cnn_model()

    pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    x = transform(pil).unsqueeze(0)

    with torch.no_grad():
        features = model.features(x)
        score = features.mean().item()

    return score

# ---------------- LEAF CNN ----------------
def analyze_leaf(img):
    score = extract_cnn_score(img)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    yellow_pixels = cv2.countNonZero(
        cv2.inRange(hsv, (20, 50, 50), (35, 255, 255))
    )

    if yellow_pixels > 5000:
        return {
            "disease": "Leaf Yellow Spot",
            "solution": "Apply zinc + fungicide spray"
        }
    elif score > 0.2:
        return {
            "disease": "Leaf Curl",
            "solution": "Use neem oil + pest control"
        }
    else:
        return {
            "disease": "Healthy Leaf",
            "solution": "No major disease detected"
        }

# ---------------- SOIL CNN ----------------
def analyze_soil(img):
    score = extract_cnn_score(img)

    # average color
    avg = np.mean(img, axis=(0, 1))
    b, g, r = avg

    # brightness
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(gray)

    # texture variance
    texture = cv2.Laplacian(gray, cv2.CV_64F).var()

    # HSV hue analysis
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hue_mean = np.mean(hsv[:, :, 0])

    # -------- RED SOIL --------
    if r > g + 25 and r > b + 25 and hue_mean < 20:
        return {
            "soil_type": "Red Soil",
            "age": "New Soil",
            "ph": "6.8",
            "color": "Red",
            "nutrients": "Iron rich",
            "crops": "Cotton, Groundnut, Millets"
        }

    # -------- BLACK SOIL --------
    elif brightness < 70:
        return {
            "soil_type": "Black Soil",
            "age": "Old Soil",
            "ph": "7.2",
            "color": "Black",
            "nutrients": "Potassium rich",
            "crops": "Cotton, Wheat, Sugarcane"
        }

    # -------- SANDY SOIL --------
    elif brightness > 150 and texture < 80:
        return {
            "soil_type": "Sandy Soil",
            "age": "Dry Old Soil",
            "ph": "5.9",
            "color": "Light Brown",
            "nutrients": "Low nitrogen",
            "crops": "Coconut, Groundnut, Watermelon"
        }

    # -------- LOAMY SOIL --------
    else:
        return {
            "soil_type": "Loamy Soil",
            "age": "Balanced Fertile Soil",
            "ph": "6.5",
            "color": "Brown",
            "nutrients": "Balanced NPK",
            "crops": "Paddy, Banana, Vegetables"
        }

@app.route("/predict-leaf", methods=["POST"])
def predict_leaf():
    file = request.files["image"]
    img = Image.open(BytesIO(file.read())).convert("RGB")
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    return jsonify(analyze_leaf(img))

@app.route("/predict-soil", methods=["POST"])
def predict_soil():
    file = request.files["image"]
    img = Image.open(BytesIO(file.read())).convert("RGB")
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    return jsonify(analyze_soil(img))

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)