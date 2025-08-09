📸 IDSnap – Photo-Based Identity Lookup System
IDSnap is an AI-powered identification system that recognizes a person from a photo and retrieves detailed information about them. It uses facial embeddings, a vector similarity search engine, and a metadata database to enable secure and accurate person lookup. Ideal for use cases like military attendance, school check-ins, corporate access control, or visitor registration.

🚀 Features
🧠 Face embedding and recognition using deep learning.

📦 Vector database (e.g., FAISS, Pinecone) to store and search facial representations.

🗂️ Relational/SQLite database to store personal information.

📤 Image upload interface (or real-time webcam support).

🔍 Instant identity lookup and data display.

🔐 Secure access and data handling.

🛠️ Tech Stack
Layer Technology
Frontend HTML / CSS / React / Bolt AI
Backend Python, Flask
Face Embedding DeepFace / InsightFace / Mediapipe
Vector Database FAISS / Pinecone
Image Processing OpenCV / PIL
Deployment Docker, Render, Vercel

🏗️ System Architecture

User → Uploads Photo
↓
Face Embedding Model (DeepFace)
↓
Vector Database → Find Closest Match
↓
Info Database → Retrieve Person's Info
↓
Return JSON or UI Display of Full Profile

🧪 API Endpoints
Method Endpoint Description
POST /upload_photo Uploads a face photo
GET /get_info/{id} Returns user details by ID
POST /add_person Add a new person + vector

📚 Example Use Case: Military Attendance
A soldier stands in front of a camera or uploads a selfie.
The system generates an embedding and finds the closest match.
The system returns:
Name
ID Number
Status (e.g., enlisted / discharged)
Last Seen
Assigned Unit

📚 2nd Example Use Case: Gym Member Recognition

A gym member signs up by submitting a photo along with their membership ID, preferred training plan, and locker number.
When they arrive, the system spots their face at the entrance.
It retrieves and displays:
Name
Membership ID
Training Plan
Assigned Locker Number

⚠️ Security Notes
All embeddings are stored securely, not raw images.

API access should be restricted via authentication.

Sensitive data should be encrypted at rest and in transit.

🧠 Inspiration
This system is inspired by practical real-world needs like:

Military or school attendance automation

Employee/visitor face check-in

Fast identity verification with minimal interaction

👤 Author
Saidabrorkhon Shavkatbekov
Building AI solutions for real-world problems 🌍
LinkedIn | GitHub
