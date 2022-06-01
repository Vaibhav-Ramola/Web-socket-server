from fastapi  import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import mediapipe as mp
import cv2 
import json


app = FastAPI()
mp_holistic = mp.solutions.holistic
cap = cv2.VideoCapture('test.mp4')


@app.get('/')
async def root():
    return {'message' : "Hello World !!!"}


def converLandmarksToJson(landmarks):
    print(f'Number of landmarks sent : {len(landmarks)}')
    frame = {}
    for i, landmark in enumerate(landmarks):
        frame[f'{i}'] = {
            'x' : str(landmark.x),
            'y' : str(landmark.y),
            'z' : str(landmark.z),
            'visibility' : str(landmark.visibility)
        }
    return frame

# def dealWithVideo():
#     with mp_holistic.Holistic(min_tracking_confidence=0.5, min_detection_confidence=0.5) as holistic:
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break
#             frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#             results = holistic.process(frame_rgb)
            
    
@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    print("Welcome Flutter :):")
    await websocket.accept()
    while True:
        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = holistic.process(frameRGB)
                await websocket.send_json(converLandmarksToJson(results.pose_landmarks.landmark))  # send frame array
            cap.release()

@app.websocket('/socket')
async def test(websocket: WebSocket):
    print("Accepting Connection")
    await websocket.accept()
    print("Connected to flutter")
    while True:
        try:
            data = await websocket.send_text("Hi there")
            print(data)
        except:
            pass 
            break

            
