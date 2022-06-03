# make sure your system satisfies requirements.txt

# run uvicorn main:app --host 0.0.0.0 on your terminal to run the server
# in general it's app.main:app --host 0.0.0.0 if you are in the websocket folder

from fastapi  import FastAPI, WebSocket, WebSocketDisconnect     # importing FastAPI and WebSocket
import mediapipe as mp                      # importing mediapipe
import cv2
import websockets.exceptions                                 # importing opencv



app = FastAPI()                         # initializing the app
mp_holistic = mp.solutions.holistic     # initailizing holistic model of mediapipe
cap = cv2.VideoCapture('test.mp4')      # opening the 'test.mp4' video usually it's: the <path of the video file>/<name_of_the_video_file_with_extension>
                                        # NOTE : The test.mp4 video is not on github, cuz it was my video :)


@app.get('/')                           # function defined for root path
async def root():
    return {'message' : "Hello World !!!"}

# Function to extract landmarks from each frame of the video 
def converLandmarksToJson(landmarks):
    print(f'Number of landmarks sent : {len(landmarks)}')       # printing the number of frames sent, should always be 33
    frame = {}                                                  # dictionary to contain landmark points with proper indexing as keys
                                                                # the keys are appropriately assigned as in the landmark_description.jpg
    for i, landmark in enumerate(landmarks):                    # loop to go through each landmark and store them in the dictionary
        frame[f'{i}'] = {   # ith landmark
            'x' : str(landmark.x),  # x : co-ordinate
            'y' : str(landmark.y),  # y : co-ordinate
            'z' : str(landmark.z),  # z : co-ordinate
            'visibility' : str(landmark.visibility) # visibility : parameter
        }
    # print(len(frame))
    return frame        # returning the dictionary


# function which is invoked to stream the data

@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    print("Welcome Flutter :):")        # greeting message
    await websocket.accept()            # function to accept the connection
    while True:                 # an infinite loop to keep the connection on continuously
        try:
            # For the code below check test.py
            with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
                cap = cv2.VideoCapture('test.mp4')
                while True:
                    ret, frame = cap.read()
                    if not ret:
                        print("broke out")
                        break
                    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    results = holistic.process(frameRGB)
                    await websocket.send_json(converLandmarksToJson(results.pose_landmarks.landmark))  # sending frame as a dictionary of landmarks
                cap.release() # release the resource to free memory
        except WebSocketDisconnect:     # catching the error to handle it and show that the client has disconnected
            print('Client disconnected')
        except websockets.exceptions.ConnectionClosedError:
            print("Client disconnected")

# test websocket from documentation
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

            
