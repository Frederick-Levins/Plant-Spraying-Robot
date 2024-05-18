# Frederick Levins and Parker Murphy 
# Main image processing code on Raspberry PI 5.

import numpy as np
from matplotlib import pyplot as plt
import serial
import math
import time
import cv2
import time


# Grab the image input from webcam 
vid = cv2.VideoCapture(0)
if not vid.isOpened():
	print("camera fail")

# Open serial connection with arduino at same baud rate	
ser = serial.Serial('/dev/ttyACM0', 9600)
ser.flush()

ex = 0
tp = 300
ty = 315

off = 'off'
  
# Function to detect green color in the object read by camera
def detect_green(image):

    # Need to set to HSV for proper color usage 
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define the lower and upper bounds for green color detection in HSV to properly fit correct RGB color range
    lower_green = np.array([40, 30, 100]) #40s
    upper_green = np.array([80, 255, 255]) #70
    
    # Create a mask set specific to green color bounds
    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Filter out unnecessary imaging noise occuring from varying objects in enviroment
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    contours,_= cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    min_area = 4000
    
    # Initalize temps for checking previously set position of box
    prev_ty, prev_tp = 0, 0
    
    # Draw bounding boxes around detected green objects
    for contour in contours:
        area = cv2.contourArea(contour)
       
        # Filter out small boxes that are obviously wrong/unneeded
        if area > min_area :

            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            ty = x + math.floor(w / 2)
            tp = y + math.floor((7 * h) / 20)
            if ty!= prev_ty or tp != prev_tp:
                # Converting coordinates to pitch and yaw angles for servos
                sendy = str(abs(math.floor(ty * (-45 / 573) + 117.9)))# Fix incorrect negative output
                sendp = str(abs(math.floor(tp * (-45 / 470) + 75)))
                send = 'X{0}Y{1}'.format((sendy), (sendp)) # Setup for ability to read difference between X and Y coordinates 
                # Send coordinates to servos over serial connection
                ser.write(send.encode('utf-8'))
                time.sleep(0.01)
                print(send)
                prev_ty, prev_t = ty, tp # Update temps

    return image
while True: 
  
  
    # Captures the current frame and flips it horizontally to fit the camera properly
    _, frame = vid.read()
    frame = cv2.flip(frame,1)
  
    # This would display the plain frame without boundary boxes for reference
    #cv2.imshow('frame', frame)  

    green_detected_frame = detect_green(frame)
    
    
    # Displays the frame with bounding boxes on green detected images 
    cv2.imshow('Green Object Detection', green_detected_frame)
    
    # Press the q key to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# End processes upon ending program
vid.release()
cv2.destroyAllWindows()
