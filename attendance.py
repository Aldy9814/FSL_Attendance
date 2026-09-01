import cv2
import numpy as np
from deepface import DeepFace
from scipy.spatial.distance import cosine
import database_manager as dbm

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
THRESHOLD = 0.35

def run_attendance():
    db_face = dbm.get_all_students()

    if not db_face:
        print("No student data found in the database. Please register students first.")
        return

    print("\nrunning Attendance System... press 'q' to quit.")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    frame_count = 0
    name_detected = "Unknown"

    while True:
        ret, frame = cap.read()
        if not ret: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_face = face_detector.detectMultiScale(gray, 1.3, 5)

        if frame_count % 10 == 0 and len(face_face) > 0:
            (x, y, w, h) = face_face[0]
            face_crop = frame[y:y+h, x:x+w]

            try:
                rep = DeepFace.represent(img_path=face_crop, model_name='Facenet512', enforce_detection=False, detector_backend='mtcnn')
                vector_cam = rep[0]["embedding"]

                min_distance = float('inf')
                name_detected = "Unknown"

                for student in db_face:
                    distance = cosine(vector_cam, student['face_embedding'])
                    if distance < min_distance:
                        min_distance = distance
                        if distance <= THRESHOLD:
                            name_detected = student['nama']

            except Exception as e:
                pass
        for (x, y, w, h) in face_face:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, name_detected, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)

        cv2.imshow("Attendance System", frame)
        frame_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_attendance()