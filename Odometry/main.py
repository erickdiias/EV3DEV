#!/usr/bin/env python3

# ---------- Importa as bibliotecas necessarias
import time
import math
from ev3dev2.motor import *
from ev3dev2.sound import Sound
from ev3dev2.button import Button
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
from ev3dev2.sensor.virtual import *
from odometry import Odometry
from utils import *

from time import sleep


robot = Robot(OUTPUT_A,OUTPUT_B)
pos = Odometry(OUTPUT_A,OUTPUT_B,5.6,15.2,360,360,debug=True)
robot._gyro = GyroSensor(INPUT_3)
cont = 0
pen = Pen(INPUT_5)
pen.down()
while True:
    print(pos.get_pos())
    direction = 90 * cont
    robot.move(75,direction,35)
    sleep(0.5)
    robot.rotate(90,100,20)
    sleep(0.5)
    cont += 1
