from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import base64
import shutil
import cv2
import numpy as np
import mediapipe as mp
import faiss
import pickle
import sqlite3
from insightface.app import FaceAnalysis

from detect_image import recognize_face
from get_info import get_person_info

# ======== Setup ========
app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load face model
face_model = FaceAnalysis(name='buffalo_l')
face_model.prepare(ctx_id=-1)

# Load FAISS index and names
faiss_index = faiss.read_index("faiss_index_cosine.bin")
with open("faiss_names_cosine.pkl", "rb") as f:
    classNames = pickle.load(f)

# Load MediaPipe
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)


# ======== Helper to draw landmarks ========
def add_landmarks_to_image(image_path):
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_image)
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for landmark in face_landmarks.landmark:
                x = int(landmark.x * image.shape[1])
                y = int(landmark.y * image.shape[0])
                cv2.circle(image, (x, y), 2, (0, 255, 0), -1)
    _, buffer = cv2.imencode('.jpg', image)
    return f"data:image/jpeg;base64,{base64.b64encode(buffer).decode()}"


# ======== FACE RECOGNITION ROUTE ========
@app.route('/recognize', methods=['POST'])
def recognize():
    try:
        file = request.files['file']
        temp_id = str(uuid.uuid4())
        temp_folder = os.path.join("temp", temp_id)
        os.makedirs(temp_folder, exist_ok=True)

        temp_path = os.path.join(temp_folder, file.filename)
        file.save(temp_path)

        img = cv2.imread(temp_path)
        if img is None:
            return jsonify({'error': 'Invalid image'}), 400

        processed_img = add_landmarks_to_image(temp_path)
        name = recognize_face(temp_path).strip().lower()
        info = get_person_info(name) or "No additional information available"

        shutil.rmtree(temp_folder)

        return jsonify({
            "name": name,
            "info": info,
            "landmarked_image": processed_img
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ======== ADD NEW USER ROUTE ========
@app.route('/add_user', methods=['POST'])
def add_user():
    try:
        name = request.form['name']
        info = request.form['info']
        file = request.files['image']

        img_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(img_path)

        img = cv2.imread(img_path)
        if img is None:
            return jsonify({'error': 'Failed to load image'}), 400

        img = cv2.resize(img, (200, 200))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        faces = face_model.get(img_rgb)

        if not faces:
            return jsonify({'error': 'No face detected'}), 400

        emb = faces[0].embedding
        emb = emb / np.linalg.norm(emb)
        emb = emb.astype('float32').reshape(1, -1)

        # Add to FAISS
        faiss_index.add(emb)
        faiss.write_index(faiss_index, "faiss_index_cosine.bin")

        # Save name
        classNames.append(name)
        with open("faiss_names_cosine.pkl", "wb") as f:
            pickle.dump(classNames, f)

        # Add to DB
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO data (name, information) VALUES (?, ?)", (name, info))
        conn.commit()
        conn.close()

        return jsonify({"message": "User added successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ======== TEST ROUTE ========
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Backend is running ✅"})


# ======== MAIN ========
if __name__ == '__main__':
    app.run(debug=True)
