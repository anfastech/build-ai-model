# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle, base64, io
import numpy as np
import cv2
from PIL import Image

# load model
with open("digits_model.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)
CORS(app)

def preprocess_dataurl(data_url):
    # decode base64
    header, encoded = data_url.split(",", 1)
    img_bytes = base64.b64decode(encoded)
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)  # 0-255

    # if background is bright, invert, so strokes become bright -> consistent
    if np.mean(img) > 127:
        img = 255 - img

    # small blur, then threshold to remove light noise
    img = cv2.GaussianBlur(img, (3, 3), 0)
    _, img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)

    # crop to bounding box of the digit
    coords = cv2.findNonZero(img)
    if coords is not None:
        x, y, w, h = cv2.boundingRect(coords)
        img = img[y:y+h, x:x+w]

    # preserve aspect ratio, scale so largest side == 8, then pad to 8x8
    if img.size == 0:
        img8 = np.zeros((8, 8), dtype=np.uint8)
    else:
        h, w = img.shape
        scale = 8.0 / max(h, w)
        new_w = max(1, int(round(w * scale)))
        new_h = max(1, int(round(h * scale)))
        img_small = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

        img8 = np.zeros((8, 8), dtype=np.uint8)
        xoff = (8 - new_w) // 2
        yoff = (8 - new_h) // 2
        img8[yoff:yoff+new_h, xoff:xoff+new_w] = img_small

    # scale pixel values to 0-16, same format sklearn digits uses
    img_scaled = (img8.astype(np.float32) / 255.0) * 16.0
    # return both the numeric features and the visual 8x8 image
    return img_scaled, img8

@app.route("/predict", methods=["POST"])
def predict():
    payload = request.get_json()
    data_url = payload.get("image")
    if not data_url:
        return jsonify({"error": "no image provided"}), 400

    img_scaled, img8 = preprocess_dataurl(data_url)
    features = img_scaled.flatten().reshape(1, -1)  # shape (1,64)

    # predict and probabilities
    pred = int(model.predict(features)[0])
    probs = None
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(features)[0]
        # top-3 labels and probs
        top_idx = np.argsort(proba)[::-1][:3]
        probs = [{"label": int(model.classes_[i]), "prob": float(proba[i])} for i in top_idx]

    # prepare debug image (upscaled for viewing)
    pil = Image.fromarray(img8).convert("L")
    pil = pil.resize((200, 200), Image.NEAREST)
    buf = io.BytesIO()
    pil.save(buf, format="PNG")
    debug_b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    debug_dataurl = f"data:image/png;base64,{debug_b64}"

    return jsonify({
        "prediction": pred,
        "top3": probs,
        "processed_image": debug_dataurl
    })

if __name__ == "__main__":
    app.run(debug=True)
