# ADAS
## all codes tested on modifiyed electrical VW Beetle with 3 phase AC motor
## this repo contains mobile application connected with esp32 car from mobile to control ADAS modules: ACC/AEB/LDWS/LKAS/Drowsy Detection

## Mobile APP
1- upload esp32 code \
2- setup ADASDriver.apk on android device

## ACC and AEB
this contains ros nodes for making ACC and AEB
### files
**acc_aeb** :make lidar to detect the rear bumper of the front car to get it position (edge detection)\
**acc_aebECU**: this node get the front car detection distance subsceibed from acc_aeb node and control the car
## Drowsy detection
this directory operates drowsy detection by yolov5 trained and fine tuned CV model
## LDWS and LKAS
**best.pt** is the trained model for detecting lanes
**Lanes.ino** to control the the car steering to keep the lane 
**final.py** is the file that apply lane detection, you can run this file without ros 
