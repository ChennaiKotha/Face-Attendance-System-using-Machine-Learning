# script to generate embeddings
import os
import cv2
import numpy as np
import mediapipe as mp
import json

mp_face = mp.solutions.face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.6)

faces = []
labels = {}
label_idx = 0

data_dir = "data/faces"

for person in os.listdir(data_dir):
    person_path = os.path.join(data_dir, person)
    if not os.path.isdir(person_path): continue

    labels[label_idx] = person
    for img_file in os.listdir(person_path):
        path = os.path.join(person_path, img_file)
        img = cv2.imread(path)
        if img is None: continue

        result = mp_face.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if result.detections:
            for det in result.detections:
                bbox = det.location_data.relative_bounding_box
                h, w, _ = img.shape
                x1 = int(bbox.xmin * w)
                y1 = int(bbox.ymin * h)
                x2 = int(x1 + bbox.width * w)
                y2 = int(y1 + bbox.height * h)
                face = img[y1:y2, x1:x2]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                face = cv2.resize(face, (100, 100)).flatten().astype(np.float32)
                norm = np.linalg.norm(face)
                face = face / norm if norm != 0 else face
                faces.append(face)
                break
    label_idx += 1

np.save("data/embeddings.npy", np.array(faces))
with open("data/labels.json", "w") as f:
    json.dump(labels, f)

print("✅ Embeddings generated and saved!")
