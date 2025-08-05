import cv2
import numpy as np
import pickle
import faiss
from insightface.app import FaceAnalysis

# Load Faiss index and class names
index = faiss.read_index("faiss_index_cosine.bin")
with open("faiss_names_cosine.pkl", "rb") as f:
    classNames = pickle.load(f)

# Initialize InsightFace
model = FaceAnalysis(name='buffalo_l')
model.prepare(ctx_id=-1, det_size=(320, 320))  # 👈 Match training settings

def recognize_face(image_path, threshold=0.5):
    """
    Recognize face in the given image and return the class name.
    
    Args:
        image_path: Path to the image file
        threshold: Similarity threshold for recognition (default: 0.5)
    
    Returns:
        str: Recognized class name or "UNKNOWN" if below threshold
    """
    test_img = cv2.imread(image_path)
    if test_img is None:
        return "INVALID_IMAGE"
    
    # 👇 Resize to match training size
    test_img = cv2.resize(test_img, (200, 200))
    test_rgb = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)
    
    faces = model.get(test_rgb)
    if not faces:
        return "NO_FACE_DETECTED"
    
    face = faces[0]
    emb = face.embedding
    emb = emb / np.linalg.norm(emb)
    emb = emb.astype('float32').reshape(1, -1)

    D, I = index.search(emb, k=1)
    similarity_score = D[0][0]
    best_match_idx = I[0][0]

    if similarity_score > threshold:
        return classNames[best_match_idx].upper()
    else:
        return "UNKNOWN"

# Example usage:
# result = recognize_face('test3.jpg')
# print(result)





































# import cv2
# import numpy as np
# import pickle
# import faiss
# from insightface.app import FaceAnalysis

# # Load Faiss index and class names
# index = faiss.read_index("faiss_index_cosine.bin")
# with open("faiss_names_cosine.pkl", "rb") as f:
#     classNames = pickle.load(f)

# # Initialize InsightFace
# model = FaceAnalysis(name='buffalo_l')
# model.prepare(ctx_id=-1)

# def recognize_face(image_path, threshold=0.5):
#     """
#     Recognize face in the given image and return the class name.
    
#     Args:
#         image_path: Path to the image file
#         threshold: Similarity threshold for recognition (default: 0.5)
    
#     Returns:
#         str: Recognized class name or "UNKNOWN" if below threshold
#     """
#     # Load the test image
#     test_img = cv2.imread(image_path)
#     if test_img is None:
#         return "INVALID_IMAGE"
    
#     test_rgb = cv2.cvtColor(test_img, cv2.COLOR_BGR2RGB)
    
#     # Detect face(s) in the image
#     faces = model.get(test_rgb)
    
#     if not faces:
#         return "NO_FACE_DETECTED"
    
#     # For simplicity, we'll just process the first face found
#     face = faces[0]
    
#     # Normalize embedding for cosine similarity
#     emb = face.embedding
#     emb = emb / np.linalg.norm(emb)
#     emb = emb.astype('float32').reshape(1, -1)

#     # Search top 1 nearest in Faiss index
#     D, I = index.search(emb, k=1)
#     similarity_score = D[0][0]
#     best_match_idx = I[0][0]

#     # Threshold check
#     if similarity_score > threshold:
#         return classNames[best_match_idx].upper()
#     else:
#         return "UNKNOWN"

# # # Example usage:
# # result = recognize_face('test3.jpg')
# # print(result)