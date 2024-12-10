from flask import Flask, render_template, request, jsonify
from PIL import Image
import numpy as np
import cv2
import base64
import io

app = Flask(__name__)

# 기본 캔버스 생성
canvas_width = 800
canvas_height = 600
canvas = np.ones((canvas_height, canvas_width, 3), dtype=np.uint8) * 255  # 흰색 배경

# 이미지 업데이트 함수
def update_canvas(data_url):
    global canvas
    header, encoded = data_url.split(',', 1)
    img_bytes = base64.b64decode(encoded)
    img = Image.open(io.BytesIO(img_bytes))
    canvas = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/save_canvas", methods=["POST"])
def save_canvas():
    global canvas
    update_canvas(request.json["imageData"])
    _, buffer = cv2.imencode(".png", canvas)
    img_str = base64.b64encode(buffer).decode("utf-8")
    return jsonify({"message": "Canvas saved", "imageData": img_str})

@app.route("/get_canvas", methods=["GET"])
def get_canvas():
    _, buffer = cv2.imencode(".png", canvas)
    img_str = base64.b64encode(buffer).decode("utf-8")
    return jsonify({"imageData": img_str})

if __name__ == "__main__":
    app.run(debug=True)
