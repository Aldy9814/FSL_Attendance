import firebase_admin
from firebase_admin import credentials, firestore
import numpy as np

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def save_data_student(nim, nama, face_embedding):
    """Saves student data to Firestore."""
    try:
        embedding_list = face_embedding.tolist() if isinstance(face_embedding, np.ndarray) else face_embedding
        doc_ref = db.collection('mahasiswa').document(nim)

        doc_ref.set({
            'nim': nim,
            'nama': nama,
            'face_embedding': embedding_list
        })
        print(f"Successfully saved student data for {nama} (NIM: {nim}) to Firestore.")
    except Exception as e:
        print(f"Error saving student data: {e}")

def get_all_students():
    """Retrieves all student data from Firestore."""
    print("Fetching all student data from Firestore...")
    collection = db.collection('mahasiswa').stream()

    db_face = []
    for doc in collection:
        data = doc.to_dict()
        db_face.append({
            'nim': data['nim'],
            'nama': data['nama'],
            'face_embedding': np.array(data['face_embedding'])
        })
    print(f"Retrieved {len(db_face)} students from Firestore.")
    return db_face

# ========
# (TEST)
# ========
if __name__ == "__main__":
    print("Menguji pengiriman data ke Firestore...")
    
    vektor_dummy = [0.1, 0.2, 0.3, 0.4] 
    save_data_student("999999", "Test Koneksi", vektor_dummy)