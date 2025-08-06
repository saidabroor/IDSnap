
from detect_image import recognize_face
from get_info import get_person_info

import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

import base64
import os
import shutil
import cv2
import numpy as np
import mediapipe as mp
import faiss
import pickle
import sqlite3
from insightface.app import FaceAnalysis
import uuid


# ========== SETUP ==========
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Face analysis model
face_model = FaceAnalysis(name='buffalo_l')
face_model.prepare(ctx_id=-1)

# Load FAISS + names
faiss_index = faiss.read_index("faiss_index_cosine.bin")
with open("faiss_names_cosine.pkl", "rb") as f:
    classNames = pickle.load(f)

# MediaPipe for landmark visualization
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=1, refine_landmarks=True)

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

# ========== DASH SETUP ==========
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO], suppress_callback_exceptions=True)
app.title = "IDSnap"

from flask_cors import CORS
CORS(app.server)

# ========== LAYOUT ==========
app.layout = html.Div([
    html.H1("Smart Identity System", style={"textAlign": "center", "marginBottom": "30px"}),

    dcc.Tabs(id="tabs", value='recognition', children=[
        dcc.Tab(label='🔍 Face Recognition', value='recognition'),
        dcc.Tab(label='➕ Add New User', value='add_user'),
    ]),

    html.Div(id='tab-content')
], style={"padding": "40px"})


# ========== CALLBACK FOR TABS ==========
@app.callback(
    Output('tab-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'recognition':
        return html.Div([
            dcc.Upload(
                id="upload-image",
                children=html.Div(["Drag and Drop or Select an Image"]),
                style={
                    "width": "60%", "height": "60px", "lineHeight": "60px", "borderWidth": "2px", "borderStyle": "dashed",
                    "borderRadius": "10px", "textAlign": "center", "margin": "auto", "backgroundColor": "#f0f0f0"
                },
                multiple=False
            ),
            html.Div(id="output-image-upload", style={"marginTop": "40px"})
        ])
    
    elif tab == 'add_user':
        return html.Div([
            dbc.Input(id="input-name", placeholder="Enter name", type="text", style={"marginBottom": "10px"}),
            dbc.Textarea(id="input-info", placeholder="Enter info about the person", style={"marginBottom": "10px"}),
            dcc.Upload(
                id="upload-new-user-image",
                children=html.Div(["Click or Drag an Image"]),
                style={
                    "width": "60%", "height": "60px", "lineHeight": "60px", "borderWidth": "2px", "borderStyle": "dashed",
                    "borderRadius": "10px", "textAlign": "center", "margin": "auto", "backgroundColor": "#f0f0f0"
                },
                multiple=False
            ),
            html.Br(),
            dbc.Button("Add User", id="submit-user", color="success", style={"marginTop": "20px"}),
            html.Div(id="add-user-output", style={"marginTop": "20px", "color": "green", "fontWeight": "bold"})
        ], style={"maxWidth": "600px", "margin": "auto"})


# ========== FACE RECOGNITION CALLBACK ==========

@app.callback(
    Output("output-image-upload", "children"),
    Input("upload-image", "contents"),
    State("upload-image", "filename")
)
def update_output(contents, filename):
    if contents:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)

        # 🔐 Create unique temp folder for this upload
        temp_id = str(uuid.uuid4())
        temp_folder = os.path.join("temp", temp_id)
        os.makedirs(temp_folder, exist_ok=True)

        temp_path = os.path.join(temp_folder, filename)
        with open(temp_path, "wb") as f:
            f.write(decoded)

        # ✅ Read image safely
        image = cv2.imread(temp_path)
        if image is None:
            return "❌ Error: Failed to load the uploaded image. Please upload a valid JPG or PNG file."

        processed_img = add_landmarks_to_image(temp_path)
        if processed_img is None:
            return "❌ Error: Could not process the image."

        name = recognize_face(temp_path)
        info = get_person_info(name)

        # ✅ Cleanup only the unique temp folder
        try:
            shutil.rmtree(temp_folder)
        except Exception as e:
            print("Temp cleanup failed:", e)

        return dbc.Row([
            dbc.Col([
                html.H4(name, style={"textAlign": "center"}),
                html.Img(src=processed_img, style={"width": "100%", "maxWidth": "300px", "margin": "auto", "display": "block"})
            ], width=6),
            dbc.Col([
                html.H4("Information", style={"color": "#28a745"}),
                html.P(info)
            ], width=6)
        ])

    return "Upload an image to get started."



# ========== ADD NEW USER CALLBACK ==========
@app.callback(
    Output("add-user-output", "children"),
    Input("submit-user", "n_clicks"),
    State("input-name", "value"),
    State("input-info", "value"),
    State("upload-new-user-image", "contents"),
    State("upload-new-user-image", "filename")
)
def add_user(n_clicks, name, info, contents, filename):
    if n_clicks:
        if not all([name, info, contents]):
            return "❌ Please fill in all fields and upload an image."

        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        img_path = os.path.join(UPLOAD_FOLDER, filename)
        with open(img_path, "wb") as f:
            f.write(decoded)

        img = cv2.imread(img_path)
        if img is None:
            return html.Div(f"Error: Failed to load image at {img_path}"), None
        img = cv2.resize(img, (200, 200))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        faces = face_model.get(img_rgb)
        print(f"Faces detected while adding user: {len(faces)}")


        if not faces:
            return "❌ No face detected in the image."

        emb = faces[0].embedding
        emb = emb / np.linalg.norm(emb)
        emb = emb.astype('float32').reshape(1, -1)

        # Add to FAISS and save
        faiss_index.add(emb)
        faiss.write_index(faiss_index, "faiss_index_cosine.bin")
        

        classNames.append(name)
        with open("faiss_names_cosine.pkl", "wb") as f:
            pickle.dump(classNames, f)

        print("FAISS index total:", faiss_index.ntotal)
        print("Number of names stored:", len(classNames))


        # Add to DB
        conn = sqlite3.connect("my_database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO data (name, information) VALUES (?, ?)", (name, info))
        conn.commit()
        conn.close()

        return "✅ User added successfully!"
    return ""

# ========== MAIN ==========
if __name__ == "__main__":
    app.run(debug=True)
