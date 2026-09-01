import cv2
from deepface import DeepFace
import database_manager as dbm
import os

def register_face():
    print("\n=== Face Registration ===")
    nim = input("Enter NIM: ")
    nama = input("Enter Name: ")

    print("\nPlease look at the camera. Press 's' to capture your face, or 'q' to quit.")
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame from camera. Exiting...")
            break
        cv2.imshow("Face Registration - Press 's' to capture", frame)


        key = cv2.waitKey(1)
        if key == ord('s'):
            file_name_temp = f"temp_{nim}.jpg"
            cv2.imwrite(file_name_temp, frame)

            print(f"\nProcessing {nama}...")
            try:
                representation = DeepFace.represent(img_path=file_name_temp, model_name='Facenet512', enforce_detection=True, detector_backend= 'mtcnn')
                face_vector = representation[0]["embedding"]

                dbm.save_data_student(nim, nama, face_vector)
            except ValueError:
                print("No face detected. Please try again.")
            except Exception as e:
                print(f"An error occurred: {e}")

            if os.path.exists(file_name_temp):
                os.remove(file_name_temp)
            break

        elif key == ord('q'):
            print("Exiting face registration.")
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    register_face()