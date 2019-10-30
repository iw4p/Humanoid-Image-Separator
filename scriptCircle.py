import json
import os
from fnmatch import fnmatch
import numpy as np
import cv2
import math

def coord(x,y):
    "Convert world coordinates to pixel coordinates."
    return int(450+170*x), int(300-170*y)


def getData(root, shouldShowField):
    
    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, "*.json"):
                pathJson = os.path.join(path, name)
                jsonSize = os.path.getsize(pathJson)
                if jsonSize > 0 and jsonSize < 300:
                    fh = open(pathJson)
                    data = json.load(fh)
                    detected = data["Ball"]["detected"]
                    with open(pathJson) as json_file:
                        data = json.load(json_file)
                        x_corBall = int(data["Ball"]["x"])
                        y_corBall = int(data["Ball"]["y"])
                        radius = int(data["Ball"]["r"])
                        x_corRobotPose = float(data["RobotPose"]["x"])
                        y_corRobotPose = float(data["RobotPose"]["y"])
                        angleRobotPose = float(data["RobotPose"]["angle"])

                        jpgFiles = (jsonToJPG(os.path.join(path, name)))
                        showImage(jpgFiles,destPath, x_corBall, y_corBall, radius, detected)
                        key = cv2.waitKey(0)
                        if shouldShowField is True:
                            drawField(x_corRobotPose,y_corRobotPose,angleRobotPose) 
                        
                        # # DEBUG
                        # print(path + name + " exists")
                        # print(x_corBall, y_corBall, radius)
                        # print(x_corRobotPose, y_corRobotPose, angleRobotPose)
                        # print(jsonToJPG(os.path.join(path, name)))
                        # jsonSize = os.path.getsize(pathJson)
                        # print("Size of json is : " + str(jsonSize))
                        # print("Size of image is : " + str(FileSize))
                        # fileExistsBool = os.path.isfile(jsonToJPG(os.path.join(path, name)))
                        # FileSize = os.path.getsize(jsonToJPG(os.path.join(path, name)))
                        # # DEBUG


                        
def drawField(x_corRobotPose,y_corRobotPose,angleRobotPose):
    greenField = np.full((600, 900, 3), 127, np.uint8) 
    greenField[:] = (5, 144, 51)
    width = 900
    height = 600
    center_coordinates = (900 - (width/2),600 - (height/2))
    color = (0, 0, 0) 
    thickness = 2

    cv2.circle(greenField, center_coordinates, (150/2), color, thickness)
    cv2.line(greenField, (450,0), (450,600), color, thickness) 

    x_corRobotPose = math.sin(x_corRobotPose)
    y_corRobotPose = math.cos(y_corRobotPose)
    angleInDegree = math.cos(math.radians(angleRobotPose))
    angleXSin = math.sin(angleRobotPose)
    angleXCos = math.cos(angleRobotPose)

    cv2.line(greenField, coord(x_corRobotPose,y_corRobotPose), coord(angleXCos,angleXSin), color, thickness) 
    cv2.circle(greenField, coord(angleXCos,angleXSin), 10, color, -1)
    cv2.rectangle(greenField,(0,0),(900,600),(0,0,0),15)
    cv2.imshow('Field', greenField)
    cv2.waitKey(0)
    cv2.destroyWindow('Field')


def jsonToJPG(path):
    path = path.strip('.json')
    path = path + ".jpg"
    return path
                     

def showImage(path, destPath, x_cor, y_cor, radius, ballDetected):
    img = cv2.imread(path)
    if ballDetected:
        center_coordinates = (x_cor*2, y_cor*2) 
        color = (0, 0, 255) 
        thickness = 2
        cv2.circle(img, center_coordinates, radius*2, color, thickness)
    cv2.imshow(path,img)
    key = cv2.waitKey(0)
    if key == 27:
        cv2.destroyAllWindows()         # It's escape button to exit
        exit()
    if key == 102 or key == 70:         # It's F button to save
        print(path + " added succressfully")
        file1 = open(destPath,"a")
        file1.write(path + "\n") 
        file1.close() 
        cv2.destroyAllWindows()
    if key == 106 or key == 74:         # It's J button to skip
        print(path + " dismissed")
        cv2.destroyAllWindows()

    cv2.destroyAllWindows()
                
# print("Enter the directory: ")
# p = raw_input() 

path = "/media/rider/New Volume/Arshia/Logs-2019-RoboCup/Amir/2019-06-01-13-22"

destPath = (path + "file.txt")

shouldShowFieldState = False

getData(path, shouldShowFieldState)

