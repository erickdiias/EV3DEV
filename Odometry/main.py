#!/usr/bin/env python3

# ---------- Importa as bibliotecas necessarias
import time # importando o tempo para a logica de programacao
from time import sleep #importando sleep da biblioteca time
import math # importando a matematica para a logica de programação
from ev3dev2.motor import * # importando tudo da biblioteca ev3dev2.motor
from ev3dev2.sound import Sound # importando o som da biblioteca ev3dev2.sound
from ev3dev2.button import Button # importando os botoes da biblioteca ev3dev2.button
from ev3dev2.sensor import * # importando tudo da biblioteca ev3dev2.sensor
from ev3dev2.sensor.lego import *  # importando tudo da biblioteca ev3dev2.sensor.lego
#from ev3dev2.sensor.virtual import * # importando tudo da biblioteca ev3dev2.sensor.virtual

from odometry import Odometry # importando tudo da biblioteca odometry
from utils import * # importando tudo da biblioteca utils
#from robot import * # importando tudo da biblioteca robot


robot = Robot(OUTPUT_A, OUTPUT_B, 13, 6.88) # setando o comando robot para utilizar  as saidas OUTPU_A e OUTPUT_B
pos = Odometry(OUTPUT_A, OUTPUT_B, 6.88, 13, 360,360, debug=True)

# ----irec------ Configura os sensores

InfraredSensor.mode = 'IR-PROX' # modo do sensor de infravermelho por aproximação

# ---------- Sensores do primeiro Brick
color_sensor_in1 = ColorSensor(INPUT_1)  # setando sensor de cor na entrada in1
color_sensor_in1.mode = 'COL-COLOR' # modo do sensor de cor RGB

color_sensor_in2 = ColorSensor(INPUT_2)  # setando sensor de cor na entrada in2
color_sensor_in2.mode = 'COL-COLOR' # modo do sensor de cor RGB

ultrasonic_sensor_in3 = UltrasonicSensor(INPUT_3)  # setando sensor ultrassonico na entrada in3
ultrasonic_sensor_in3.mode = 'US-DIST-CM' # modo do sensor ultrasonico em cm

robot._gyro = GyroSensor(INPUT_4) # setando o sensor de giro na entra in4
_gyro = 'GYRO-ANG' # modo do sensor gyroscopio em angulhos

cont = 0
# pen = Pen(INPUT_5)
# pen.down()

while True:
    print(pos.get_pos())
    direction = 90 * cont
    robot.move(75,direction,35)
    sleep(1)
    # # robot.rotate(90,100,20)
    # # sleep(0.5)
    # # cont += 1
