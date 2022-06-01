# A test file to check the functionality and proper import of mediapipe and opencv in python

import mediapipe as mp          # importing mediapipe - package which contains libraries to find landmarks on images and videos
import cv2                      # for image and video processing and reading

mp_drawing = mp.solutions.drawing_utils         # instance to draw landmarks on each frame
mp_holistic = mp.solutions.holistic             # instance to process and calculate landmarks in each frame

with mp_holistic.Holistic(min_tracking_confidence=0.5, min_detection_confidence=0.5) as holistic:   # giving the instance holistic alias for the following code
    cap = cv2.VideoCapture(0)           # cv2 function to open video files, parameter 0 is for webcam
    while True:                         # An infinite loop to read each frame from the video till it's finished
        ret, frame = cap.read()         # function to read individual frame in BGR format
                                        # ret - boolean(if the frame was successfully read or not): frame - np.array(size=(width, height, 3))
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)           # converting the read frame from BGR to RGB format
        results = holistic.process(frameRGB)                        # process the frame and store it in results    
        frame = cv2.cvtColor(frameRGB, cv2.COLOR_RGB2BGR)           # convert frame back to BGR to display 
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)      # function to draw landmarks on the image, check docs for further info
        cv2.imshow("Frame", frame)                  # function to show the frame
        if cv2.waitKey(13) == ord('q'):             # keep reading till 'q' is pressed 
            break                                   # and then exit the loop    
    cap.release()                   # release the instance/pointer whatever it is
    cv2.destroyAllWindows()         # close all windows
