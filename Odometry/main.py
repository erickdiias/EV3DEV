#!/usr/bin/env python3

# ---------- Importa as bibliotecas necessarias
import time # importando o tempo para a logica de programacao
import math # importando a matematica para a logica de programação
from ev3dev2.motor import * # importando tudo da biblioteca ev3dev2.motor
from ev3dev2.sound import Sound # importando o som da biblioteca ev3dev2.sound
from ev3dev2.button import Button # importando os botoes da biblioteca ev3dev2.button
from ev3dev2.sensor import * # importando tudo da biblioteca ev3dev2.sensor
from ev3dev2.sensor.lego import *  # importando tudo da biblioteca ev3dev2.sensor.lego
from ev3dev2.sensor.virtual import * # importando tudo da biblioteca ev3dev2.sensor.virtual
from odometry import Odometry # importando tudo da biblioteca odometry
from utils import * # importando tudo da biblioteca utils
#from robot import *
from time import sleep #importando sleep da biblioteca time


robot = Robot(OUTPUT_A,OUTPUT_B) # setando o comando robot para utilizar  as saidas OUTPU_A e OUTPUT_B
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
