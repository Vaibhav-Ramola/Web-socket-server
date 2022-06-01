import mediapipe as mp
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic

with mp_holistic.Holistic(min_tracking_confidence=0.5, min_detection_confidence=0.5) as holistic:
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(frameRGB)
        frame = cv2.cvtColor(frameRGB, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        cv2.imshow("Frame", frame)
        if cv2.waitKey(13) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
