# import statements
import numpy as np
import cv2
import face_recognition as fr
import os
from datetime import datetime
from typing import Tuple, List



def image_loader(path: str) -> Tuple[List[str], list]:
    """
    Loading images from given directory
    :param path: str, address of images directory
    :return: list, images class names
    """
    images = []
    class_names = []
    list_of_contents = os.listdir(path)
    for cl in list_of_contents:
        current_image = cv2.imread(f"{path}/{cl}")
        images.append(current_image)
        class_names.append(os.path.splitext(cl)[0])
    return class_names, images


# Encoding process
def find_encodings(list_of_images):
    encode_list = []
    for img in list_of_images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = fr.face_encodings(img)[0]
        encode_list.append(encode)
    return encode_list

encode_list_known = find_encodings(images)
print("Encoding completed!")


def mark_attendance(name_of_person):
    with open("attendance.csv", "r+") as f:
        my_data_list = f.readlines()
        list_of_names = []
        for line in my_data_list:
            entry = line.split(", ")
            list_of_names.append(entry[0])
        if name_of_person not in list_of_names:
            now = datetime.now()
            date_string = now.strftime("%H:%M:%S")
            f.writelines(f"\n{name_of_person}, {date_string}")


# capturing the webcam
cap = cv2.VideoCapture(0)
while True:
    success, img = cap.read()
    img_small = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    img_small = cv2.cvtColor(img_small, cv2.COLOR_BGR2RGB)
    faces_in_current_frame = fr.face_locations(img_small)
    encodings_in_current_frame = fr.face_encodings(img_small, faces_in_current_frame)

    for encodeFaces, faceLoc in zip(encodings_in_current_frame, faces_in_current_frame):
        matches = fr.compare_faces(encode_list_known, encodeFaces)
        faceDistance = fr.face_distance(encode_list_known, encodeFaces)
        matchIndex = np.argmin(faceDistance)

        if matches[matchIndex]:
            name = classNames[int(matchIndex)].upper()
            y_1, x_2, y_2, x_1 = faceLoc
            y_1, x_2, y_2, x_1 = y_1 * 4, x_2 * 4, y_2 * 4, x_1 * 4
            cv2.rectangle(img, (x_1, y_1), (x_2, y_2), (0, 255, 0), 2)
            cv2.putText(img, name, (x_1 + 6, y_2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            mark_attendance(name)
    cv2.imshow("Webcam", img)
    cv2.waitKey(1)
