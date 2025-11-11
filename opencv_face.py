import cv2
from PIL import Image, ImageTk


class FaceDetector:
    def __init__(self, window_label, minute_label, timer_callback):
        self.window_label = window_label        # window_label: Tkinter label to show the webcam video
        self.minute_label = minute_label        # minute_label: Label to show the timer
        self.timer_callback = timer_callback    # timer_callback: Function to call for resetting timer

        # Load Haar cascades
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        self.webcam_video_stream = cv2.VideoCapture(0)
        self.running = True

    def draw_facial_landmarks(self, frame, landmarks):
        for facial_feature in landmarks.keys():
            color = (0, 255, 0)
            for point in landmarks[facial_feature]:
                x, y = point
                x *= 4
                y *= 4
                cv2.circle(frame, (x, y), 2, color, -1)
            if len(landmarks[facial_feature]) > 1:
                for i in range(len(landmarks[facial_feature]) - 1):
                    x1, y1 = landmarks[facial_feature][i]
                    x2, y2 = landmarks[facial_feature][i + 1]
                    x1 *= 4
                    y1 *= 4
                    x2 *= 4
                    y2 *= 4
                    cv2.line(frame, (x1, y1), (x2, y2), color, 1)
        return frame

    def process_frame(self):
        ret, current_frame = self.webcam_video_stream.read()
        gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

        all_face_landmarks = []
        for (x, y, w, h) in faces:
            # Draw a green rectangle around each detected face
            cv2.rectangle(current_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Detect eyes inside face region
            landmarks = {"left_eye": [], "right_eye": []}
            roi_gray = gray[y:y + h, x:x + w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=10)

            for (ex, ey, ew, eh) in eyes:
                # Draw small rectangles around eyes for clarity
                cv2.rectangle(current_frame, (x + ex, y + ey), (x + ex + ew, y + ey + eh), (255, 255, 0), 1)

                if ex + ew / 2 < w / 2:
                    landmarks["left_eye"].append((ex, ey))
                else:
                    landmarks["right_eye"].append((ex, ey))

            all_face_landmarks.append(landmarks)

        for landmarks in all_face_landmarks:
            current_frame = self.draw_facial_landmarks(current_frame, landmarks)

        frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)
        frame = ImageTk.PhotoImage(frame)

        self.window_label.config(image=frame)
        self.window_label.image = frame

        # call timer callback
        self.timer_callback(faces)

    def start(self):
        while self.running:
            self.process_frame()
            cv2.waitKey(50)

    def stop(self):
        self.running = False
        self.webcam_video_stream.release()
        cv2.destroyAllWindows()




