import math
import random

from flask import Flask, jsonify, request

app = Flask(__name__)

REGISTRATION_NUMBER = "FA23-BDS-032"

# Required coefficient generation procedure.
seed = 32
random.seed(seed)
a1 = random.uniform(-5, 5)
a2 = random.uniform(-5, 5)
a3 = random.uniform(-5, 5)
b = random.uniform(-10, 10)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/predict")
def predict():
    inputs = {}

    for name in ("x1", "x2", "x3"):
        raw_value = request.args.get(name)

        if raw_value is None:
            return jsonify({"error": f"Missing parameter: {name}"}), 400

        try:
            value = float(raw_value)
        except (ValueError, OverflowError):
            return jsonify({"error": f"{name} must be a finite number"}), 400

        if not math.isfinite(value):
            return jsonify({"error": f"{name} must be a finite number"}), 400

        inputs[name] = value

    prediction = (
        a1 * inputs["x1"]
        + a2 * inputs["x2"]
        + a3 * inputs["x3"]
        + b
    )

    if not math.isfinite(prediction):
        return jsonify({"error": "Prediction exceeds the numeric range"}), 400

    return jsonify({
        "registration number": REGISTRATION_NUMBER,
        "prediction": prediction
    })
