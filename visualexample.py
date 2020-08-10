#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 19:46:11 2020

@author: https://github.com/ageitgey/face_recognition
"""

import face_recognition
import cv2
import numpy as np
import glob
import pymysql
import mysql.connector
# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
def view_details(email): #this function inputs the email of the user and displays the details stored in the database
    
    try:
        conn = mysql.connector.connect(user='root', password='nopassword',
                              host='localhost',
                              database='Visual_Welcome_center')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM Visual_Welcome_Center.user WHERE email =%s", (email,))
        #row_headers=[x[0] for x in cursor.description]
        row = cursor.fetchone()
        
        #json_data=[]
        #for result in row:
         #   json_data.append(dict(zip(row_headers,result)))
        #return json.dumps(json_data)
        return row

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
# Load a sample picture and learn how to recognize it.
path_to_directory = './KNOWN_FACES_DIR'
known_face_encodings=[]
known_face_names=[]
image_paths = glob.glob(path_to_directory + "/*.jpg")
for names in image_paths:

    # Load an image
    image = face_recognition.load_image_file(names)

    # Get 128-dimension face encoding
    # Always returns a list of found faces, for this purpose we take first face only (assuming one face per image as you can't be twice on one image)
    encoding = face_recognition.face_encodings(image)[0]

    # Append encodings and name
    known_face_encodings.append(encoding)
    names=names[:-4]
    names=names.split("/") 
    known_face_names.append(names[-1])
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding,0.5)
            name = "Unknown"

            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                
            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()