# Plant-Spraying-Robot
ECE 314: Elements of Robotics final project, Theoretical plant spraying robot, finished top project in class (95% score result).


MainRobotCode.ino
This is the main code for control of motor power and driving functionality. It is degraded from the last lab to early labs to enable manual drive and motor control, rather than self driving with encoders. This is due to the inability of the encoders to proper function, combined with the absurd weight addition of the new components. It is in Arduino C.

Remote.ino
This is the code that allows for the remote and joystick control of the robot.  It is in Arduino C.

Sprayer.ino 
This is the code that communicates with the raspberry pi and receives coordinates. It then converts the coordinates to readable positions for the servo motor to enable movement of the sprayer. It is in Arduino C.

sprayerG.py
This is the code that drives the image processing of the robot. It uses opencv RGB library to create boundary boxes around green objects. It then serially communicates with the arduino and sends these coordinates separated by an X and Y. See figures One and Two. It is in python.

314FinalReport.pdf

Report for more information.
