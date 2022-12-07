import cv2
import face_recognition
import os
import numpy as np
from app import constants
import base64
import json
from imutils import paths
import base64
import shutil
from pathlib import Path
import pickle


current_face_encodings = []
current_face_names =[]
frame_resizing = 0.5#1#0.25

def check_existence(id):
    encoding_file_name = id + ".pic"
    filename = os.path.join(constants.PathToEncodings, encoding_file_name)
    my_file = Path(filename)
    return my_file.is_file()

def load_encoding_images(userName):
    encoding_file_name = userName + ".pic"
    filename = os.path.join(constants.PathToEncodings, encoding_file_name)
    current_face_encodings = pickle.loads(open(filename, "rb").read())
    current_face_names = [userName for i in range(len(current_face_encodings))]
    print("load_encoding_images Encoding images loaded", len(current_face_encodings))
    return current_face_encodings


def find_face(userName, frame) -> str:
    current_face_encodings = load_encoding_images(userName)
    
    frame = base64ToImage(frame)
    cv2.imwrite("imageToSave.png", frame)
    small_frame = cv2.resize(frame, (0, 0), fx=frame_resizing, fy=frame_resizing)
    # Find all the faces and face encodings in the current frame of video
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    print("face_encodings", len(face_encodings))
    print(len(current_face_encodings), current_face_names)
    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(current_face_encodings, face_encoding)
        
        print("matches", len(matches), matches)
        if True not in matches:
            return constants.FaceAuthStatus.Invalid

        face_distances = face_recognition.face_distance(current_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            return constants.FaceAuthStatus.Valid

    return constants.FaceAuthStatus.FaceNotFound


def base64ToImage(b64_str):
    im_bytes = base64.b64decode(b64_str)
    im_arr = np.frombuffer(im_bytes, dtype=np.uint8)
    return cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR)


def save_encodings(userName):
    
    imagePath = list(paths.list_images(os.path.join(constants.PathToImages, userName)))
    encoding_file_name = userName + ".pic"
    encodings = []
    for img_path in imagePath:
        img = cv2.imread(img_path)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        try:
            img_encoding = face_recognition.face_encodings(rgb_img)[0]
        except:
            print("Face not found!   ", img_path)
            continue
        encodings.append(img_encoding)
    filename = os.path.join(constants.PathToEncodings, encoding_file_name)
    with open(os.path.join(filename), "wb+") as f:
        f.write(pickle.dumps(encodings))
    print("encoding saved")



def save_faces(userName, images):
    folder = Path(constants.PathToImages + userName)
    print(folder)
    if folder.exists() and folder.is_dir():
            shutil.rmtree(folder)
    os.makedirs(folder)                             
    for i, image in enumerate(images):
        imgdata = base64.b64decode(image[22:])
        filename = str(i)+'.png'
        with open(os.path.join(folder, filename), "wb+") as fh:
            fh.write(imgdata)
        print("Photo ", i, " added")
