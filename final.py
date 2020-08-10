#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 19:13:43 2020

@author: akula
"""

import face_recognition #to recognise and verify faces
import cv2 #for capturing the video from camera and showing images
import numpy as np 
import time #to stop the execution of program for some time
import speech_recognition as sr # recognise speech

import os # to remove previous image files
import glob #for managing directories of the images 
import pyttsx3 #for text to speech

import pandas as pd #for dataframes from google spreadsheets

import pymysql #for connecting mysql database 
from datetime import datetime #for getting datetime

import pytz #for timezone

import mysql.connector

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
        
def add_details(list1): #this function add details to the database when a new user is registered
    try:
        enrolled_on = list1[0]
        full_name = list1[1]
        email = list1[2]
        department = list1[3]
        phone = list1[4]
        designation = list1[5]
        website = list1[6]
        if email:
            conn = mysql.connector.connect(user='root', password='nopassword',
                              host='localhost',
                              database='Visual_Welcome_center')
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO Visual_Welcome_center.user(email,full_name,enrolled_on,designation,department,phone,website) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            bindData = (email,full_name,enrolled_on,designation,department,phone,website)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            #respone = jsonify("Recorded successfully!")
            #respone.status_code = 200
            
            
            return "Recorded!"
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()       

def add_time(email): #this function inputs the email of the user and adds the time of entry in the database
    try:
        conn = mysql.connector.connect(user='root', password='nopassword',
                              host='localhost',
                              database='Visual_Welcome_center')
        now = datetime.now(pytz.timezone('America/New_York'))
        _dtstring = str(now.strftime("%Y-%m-%d"))
        _timestring = str(now.strftime("%H:%M"))
        print(email,_dtstring,_timestring)
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "INSERT INTO Visual_Welcome_center.timesheet(email,date,clock_in) VALUES(%s,%s,%s)"
        bindData = (str(email),_dtstring,_timestring)
        cursor.execute(sqlQuery, bindData)
        conn.commit()
        #respone = jsonify("Recorded successfully!")
        #respone.status_code = 200
        return "Recorded!"
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()       

def view_timesheet(email): #this function inputs the email of the user and displays all the entries of the user stored in the database
    try:
        conn = mysql.connector.connect(user='root', password='nopassword',
                              host='localhost',
                              database='Visual_Welcome_center')
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        #cursor.execute("SELECT u.email,u.full_name,u.department,u.designation,u.enrolled_on,u.phone,u.website,t.date,t.clock_in FROM Visual_Welcome_Center.user u inner join Visual_Welcome_Center.timesheet t WHERE u.email = %s", (email,))
        cursor.execute("SELECT u.email,u.full_name,t.date,t.clock_in FROM Visual_Welcome_Center.user u inner join Visual_Welcome_Center.timesheet t on u.email=t.email WHERE u.email = %s", (email,))
        
        row = cursor.fetchall()
        #respone = jsonify(row)
        #respone.status_code = 200
        return row
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
        
def google_form(prev_row_count): 
#this function is called for checking new information stored in the google form and returns the latest entry in the form. this checks for new entries after every 10 seconds.
    count=10
    while count>0:#to loop for check for new entries every 10 seconds 
        print(count)
        list1=[]
        
        sheet_id = '1axfRgWWEt-A6WCPyqxFau_Yi3O0-TDjrcuvTjd8_r_0'
        df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
        total_count= df.shape[0]
        print(total_count,prev_row_count)
        if(total_count>prev_row_count):  #if there is a new entry then it will add those details in the list and returns it.
            list1.append(df.at[total_count-1,'Timestamp'])
            list1.append(df.at[total_count-1,'Full Name'])
            list1.append(df.at[total_count-1,'Email'])
            list1.append(df.at[total_count-1,'Department '])
            list1.append(str(df.at[total_count-1,'Phone number']))
            list1.append(df.at[total_count-1,'Designation'])
            list1.append(df.at[total_count-1,'Website'])
            print (list1)
            return list1
            break;
        else:
            time.sleep(10)
            count-=1
    return -1

def there_exists(terms):#a simple function to check if there exists particular terms in the input speech.
    for term in terms:
        if term in voice_data:
            return True

def record_audio(ask=False):
    #this function records the audio from the user and then converts it to text using google speech to text engine and then returns the text.
    a=3
    while a>0:
        
        with sr.Microphone() as source: # microphone as source
            if ask:
                speak(ask)
            r.adjust_for_ambient_noise(source)
            audio = r.record(source,5)
          # listen the audio via source
            voice_data = ''
            try:
                voice_data = r.recognize_google(audio) #recognizes the audio and returns the text data
                a= 0
            except sr.UnknownValueError: # error: recognizer does not understand
                speak('I did not get that. Please try again')
                a= a-1
            except sr.RequestError:
                speak('Sorry, the service is down') # error: recognizer is not connected
            print(f">> {voice_data.lower()}") # print what user said
    return voice_data.lower()

def speak(audio_string):
    #this function uses offline library of pyttsx3 to convert text to speech.
    
    print(audio_string)
    engine = pyttsx3.init()
    engine.say(audio_string)
    engine.runAndWait()

def register_user():
    #this function will register the user who is standing in front of the system. it captures the user photograph and then asks the user to fill out the google form and then uses those details to register the user in the database. It also saves the photograph in the local directory.
     v=verify_face() #it will verify that the same person who started the interaction with the system is registering himself.
     image= cv2.imread("QR.jpg")
     
     if v == True: #if the same person is standing in the front of the camera.
         speak("Please smile for a photograph")
         time.sleep(2) #waits for the person to smile
         ret,frame = video_capture.read()
         speak("Please scan the code and fill out the google form to register")
         cv2.imshow("QR",image)#shows the QR code to register the user in the database 
         cv2.waitKey(10000)
         cv2.destroyWindow("QR")
         sheet_id = '1axfRgWWEt-A6WCPyqxFau_Yi3O0-TDjrcuvTjd8_r_0'
         df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
         print (df)
         total_count= df.shape[0] #counts the total number of rows in the spreadsheet before starting the loop to check for new entries
         listtemp= google_form(total_count) #calls the google_form function to check for new entries and then returns it as a list
         if listtemp==-1:
             speak("you have not filled the form")
             return True
         print (add_details(listtemp)) #add the details to the database
         print (add_time(listtemp[2])) #add the timestamp entry
         print (view_details(listtemp[2]))#view the added details
         #voice_data = record_audio()
         final= listtemp[2] + ".jpg"
         
         #cv2.waitKey(1)

         cv2.imwrite(os.path.join(path_to_directory,final),frame)#saves the image with email as its name as email will be unique.
     return True  
         
def verify_face():
    #this function verifies the person standing in front of the camera as the same person who started the interation
    ret, frame = video_capture.read()
    
        # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    
    
    face2_locations = face_recognition.face_locations(rgb_small_frame)
    face2_encodings = face_recognition.face_encodings(rgb_small_frame, face2_locations)
    if not face2_encodings:
        print("Please stand in the front of the camera")
            
        return False
    
    #compare the face encodings
    matches = face_recognition.compare_faces(aaa, face2_encodings[0])
    
    print(matches)
    
    if matches[0]== True:
        print("Same person")
        #speak("Hello Jatt Saab")
        return True
    
    if matches[0]== False:
        print("Not the same person")
        return False

def find_matches():
    #this function finds the matches from the given set of images in the directory and returns the best match. 
    
    path_to_directory = './KNOWN_FACES_DIR'
    known_face_encodings=[]
    known_face_names=[]
    image_paths = glob.glob(path_to_directory + "/*.jpg")
    name = "Unknown"
    if image_paths:
        
        for names in image_paths:
        #loads all the face encodings 
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


        ret, frame = video_capture.read()
        
            # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]
        
        
        face2_locations = face_recognition.face_locations(rgb_small_frame)
        face2_encodings = face_recognition.face_encodings(rgb_small_frame, face2_locations)
        
        if not face2_encodings:
            return True
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face2_encodings[0],0.5 )
        
    
        # # If a match was found in known_face_encodings, just use the first one.
       
    
        # Or instead, use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(known_face_encodings, face2_encodings[0])
        best_match_index = np.argmin(face_distances)
        
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            #to update the images in the database
        
            
            #to add the entry into the database
            add_time(str(name))
            
            
            #deletes the previous image
            os.remove(os.path.join(path_to_directory,name+".jpg"))
            #stores the new image
            cv2.imwrite(os.path.join(path_to_directory,name+".jpg"),frame)
            #returns the name of the best match

    return(name)

###################################################################

#loading all the face encodings before running into the while True loop
r = sr.Recognizer() 

path_to_directory = './KNOWN_FACES_DIR'
known_face_encodings=[]
known_face_names=[]
image_paths = glob.glob(path_to_directory + "/*.jpg")
if image_paths:
    
    for name in image_paths:
        
            # Load an image
            image = face_recognition.load_image_file(name)
    
            # Get 128-dimension face encoding
            # Always returns a list of found faces, for this purpose we take first face only (assuming one face per image as you can't be twice on one image)
            encoding = face_recognition.face_encodings(image)[0]
    
            # Append encodings and name
            known_face_encodings.append(encoding)
            name=name.split(".")
            name=name[1].split("/") 
            known_face_names.append(name[-1])

while True:

    video_capture = cv2.VideoCapture(0)
    # Grab a single frame of video
    ret, frame = video_capture.read()
    
        # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    
        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    
    
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    if not face_encodings:
        continue
    aaa= [face_encodings[0]]
    #if a person is recognised by the camera then it waits for 3 seconds before checking again
    print ("testing next in 3 sec")
    time.sleep(3)
    
    v=verify_face()
    #if the same person initiated the interaction is standing in front of the camera after 3 seconds then it will try to find the match. if no match is found then it will ask the user to register themselves.
    if v == True:
        n=find_matches()
        print(n)
        if n=="Unknown":
            speak("Hello! You are not registered. Do you want to register yourself? Say YES or NO")
           
            #record the user audio for the response
            voice_data = record_audio()
            if there_exists(['yes','yeah']):
            
               #it will start the register user function. 
                register_user()
                speak ("Congratulations! you are successfully registered.")
            continue
        if n==True:
            continue
        name = (view_details(str(n))[1])
        #greet if a person is recognised 
        speak("Hello! %s! how can I help you today?"%name)
        #put in all the options that can be used to interact 
        #for this example i have used the command to show my previous entries in the system
        voice_data = record_audio()
        if there_exists(['show','entries','previous']):
            r=(view_timesheet(str(n)))
            for i in r:
                print (i)
            time.sleep(10)
