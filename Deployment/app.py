from detect_image import *
from get_info import *

import dash
from dash import dcc, html, Input, Output, State
import base64
import os
import shutil
import dash_bootstrap_components as dbc
import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Face Mesh
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
                cv2.circle(image, (x, y), 2, (0, 255, 0), -1)  # smaller dot for better visibility

    _, buffer = cv2.imencode('.jpg', image)
    base64_image = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{base64_image}"


# Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])

app.layout = html.Div([
    html.Div(
        html.H1("Smart Identity Recognition", style={"textAlign": "center", "color": "#4CAF50", "fontWeight": "bold"}),
        style={"marginBottom": "20px", "backgroundColor": "#f0f8ff", "padding": "10px", "borderRadius": "10px"}
    ),

    html.Div([
        dcc.Upload(
            id="upload-image",
            children=html.Div([
                html.I(className="fa fa-upload", style={"fontSize": "20px", "marginRight": "10px"}),
                html.Span("Drag and Drop or Select an Image")
            ]),
            style={
                "width": "60%", "height": "60px", "lineHeight": "60px", "borderWidth": "2px", "borderStyle": "dashed",
                "borderRadius": "10px", "textAlign": "center", "margin": "auto",
                "backgroundColor": "#eaf7ff", "color": "#007BFF", "cursor": "pointer"
            },
            multiple=False
        ),
    ], style={"textAlign": "center", "marginBottom": "30px"}),

    html.Div(id="output-image-upload", style={"marginTop": "20px"}),
], style={"fontFamily": "Arial, sans-serif", "backgroundColor": "#f8f9fa", "padding": "20px"})


@app.callback(
    Output("output-image-upload", "children"),
    Input("upload-image", "contents"),
    State("upload-image", "filename")
)
def update_output(contents, filename):
    if contents is not None:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)

        if os.path.exists("temp"):
            shutil.rmtree("temp")
        os.makedirs("temp", exist_ok=True)

        temp_image_path = os.path.join("temp", filename)
        with open(temp_image_path, "wb") as f:
            f.write(decoded)

        # Step 1: Visualize landmarks
        processed_image = add_landmarks_to_image(temp_image_path)

        # Step 2: Recognize person
        # recognized_name = recognize_face(temp_image_path)
        recognized_name = str(recognize_face(temp_image_path))




        print(recognized_name)

        # Step 3: Get info about person
        info_text = get_person_info(recognized_name)

        print(info_text)

        shutil.rmtree("temp")

        return html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H4(recognized_name, style={"textAlign": "center", "color": "#007BFF"}),
                        html.Img(
                            src=processed_image,
                            style={
                                "width": "100%", "maxWidth": "300px", "margin": "auto", "display": "block",
                                "border": "2px solid #007BFF", "borderRadius": "10px"
                            }
                        )
                    ], style={"padding": "10px", "backgroundColor": "#eaf7ff", "borderRadius": "10px"})
                ], width=6),

                dbc.Col([
                    html.Div([
                        html.H4("Information", style={"textAlign": "left", "color": "#28a745", "marginBottom": "20px"}),
                        html.P(info_text)
                    ], style={
                        "padding": "10px", "backgroundColor": "#eaffea", "borderRadius": "10px",
                        "color": "#333", "lineHeight": "1.8"
                    })
                ], width=6)
            ])
        ], style={"marginTop": "40px"})

    return html.Div(
        "Please upload an image to see results.",
        style={"textAlign": "center", "color": "#dc3545", "fontWeight": "bold", "marginTop": "20px"}
    )


if __name__ == "__main__":
    app.run(debug=True)
