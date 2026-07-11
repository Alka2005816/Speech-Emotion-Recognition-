from flask import Flask, render_template, request
import librosa
import numpy as np
import joblib
import os

app = Flask(__name__)

# Load Model
model = joblib.load("models/emotion_model.pkl")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Feature Extraction
def extract_feature(file_name):
    audio, sample_rate = librosa.load(file_name, sr=22050)

    mfcc = np.mean(
        librosa.feature.mfcc(
            y=audio,
            sr=sample_rate,
            n_mfcc=40
        ).T,
        axis=0
    )

    chroma = np.mean(
        librosa.feature.chroma_stft(
            y=audio,
            sr=sample_rate
        ).T,
        axis=0
    )

    mel = np.mean(
        librosa.feature.melspectrogram(
            y=audio,
            sr=sample_rate
        ).T,
        axis=0
    )

    feature = np.hstack((mfcc, chroma, mel))

    return feature


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    if "audio" not in request.files:
        return render_template("index.html", prediction="No audio file uploaded")

    file = request.files["audio"]

    if file.filename == "":
        return render_template("index.html", prediction="No file selected")

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        features = extract_feature(filepath)

        prediction = model.predict([features])[0]

        confidence = np.max(model.predict_proba([features])) * 100

        print("Prediction:", prediction)
        print("Confidence:", confidence)

        return render_template(
            "index.html",
            prediction=prediction,
            confidence=f"{confidence:.2f}%"
        )

    except Exception as e:
        return render_template("index.html", prediction=f"Error: {e}")


if __name__ == "__main__":
    app.run(debug=True)