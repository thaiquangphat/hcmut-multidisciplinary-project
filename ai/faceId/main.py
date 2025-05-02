import cv2
import numpy as np
from scipy.spatial.distance import cosine
import requests
import json
from insightface.app import FaceAnalysis
from facenet_pytorch import MTCNN
import torch
import time
from fastapi import FastAPI, HTTPException
import threading


mtcnn = MTCNN(keep_all=True, device='cuda' if torch.cuda.is_available() else 'cpu') 
app_insightface = FaceAnalysis()
app_insightface.prepare(ctx_id=0)
FPS = 5
frame_interval = 1.0 / FPS
API_URL_LOGIN = "http://localhost:8000/api/v1/auth/loginface" 
API_URL_SIGNUP = "http://localhost:8000/api/v1/auth/signupface"
is_running = False
app = FastAPI()
def get_face_embedding(faces):
    """Extract face embedding from image"""
    # faces = mtcnn(image)
    if faces is None:
        return None
        
    embeddings = app_insightface.get(faces)
    return embeddings[0].embedding if embeddings else None

def send_to_api(embedding,isSignUp,email=None,password=None):
    """Send face embedding to API for comparison"""
    if isSignUp:
        API_URL = API_URL_SIGNUP
        try:
            response = requests.post(
                API_URL,
                json={
                    "email": email,
                    "password": password,
                    "faceID": embedding.tolist() if isinstance(embedding, np.ndarray) else embedding
                }
            )
            if response.status_code == 200:
                print("Matches found:", response.json())
            else:
                print("Error:", response.text)
        except Exception as e:
            print("API Error:", str(e))
    else:
        API_URL = API_URL_LOGIN
        try:
            response = requests.post(
                API_URL,
                json={
                    "email": email,
                    "faceID": embedding.tolist() if isinstance(embedding, np.ndarray) else embedding
                }
            )
            if response.status_code == 200:
                print("Matches found:", response.json())
            else:
                print("Error:", response.text)
        except Exception as e:
            print("API Error:", str(e))

def camera_loop(isSignUp=False,email=None,password=None):
    """Capture video from camera and process frames"""
    global is_running
    if not is_running:
        return
    cap = cv2.VideoCapture(0)
    start_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # rgb_frame = cv2.imread("test.jpg")
        # rgb_frame = cv2.cvtColor(rgb_frame, cv2.COLOR_BGR2RGB)
        # cv2.imshow('Frame', frame)
        rgb_frame_np = np.array(rgb_frame)

        faces = mtcnn(rgb_frame_np)
        if faces is not None:
            for i, face in enumerate(faces):
                embedding = get_face_embedding(rgb_frame_np)
                
                if embedding is not None:
                    send_to_api(embedding,isSignUp,email,password)
                    # print("Face embedding:", embedding)
                    return
        elapsed_time = time.time() - start_time
        if elapsed_time < frame_interval:
            time.sleep(frame_interval - elapsed_time)
        start_time = time.time()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
@app.post("/start-camera-login")
async def start_camera(email: str):
    """Start camera for face login"""
    global is_running, camera_thread
    isSignUp = False
    if is_running:
        raise HTTPException(status_code=400, detail="Camera already running")


    is_running = True
    camera_thread = threading.Thread(target=camera_loop, args=(isSignUp,email))
    camera_thread.start()
    return {"message": "Camera started"}
@app.post("/start-camera-signup")
async def start_camera(email: str,password: str):
    """Start camera for face login"""
    global is_running, camera_thread
    isSignUp = True
    if is_running:
        raise HTTPException(status_code=400, detail="Camera already running")


    is_running = True
    camera_thread = threading.Thread(target=camera_loop, args=(isSignUp,email,password))
    camera_thread.start()
    return {"message": "Camera started"}


@app.post("/stop-camera")
async def stop_camera():
    global is_running, camera_thread

    try:
        if camera_thread and camera_thread.is_alive():
            is_running = False
            camera_thread.join(timeout=5)  

            if camera_thread.is_alive():
                print("Camera thread is unresponsive. Terminating forcefully.")

        is_running = False
        camera_thread = None

        cv2.destroyAllWindows()

        return {"message": "Camera stopped successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error stopping camera: {str(e)}")
if __name__ == "__main__":
    app.run(host='localhost', port=5001, debug=True)