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
from robot import Robot # importando tudo da biblioteca utils

# ---------- Parametros
motor_esquerdo = OUTPUT_A # setando motor_esquerdo como saída OUTPUT_A
motor_direito = OUTPUT_B # setando motor_direito como saída OUTPUT_B

diametro_roda = 6.88 # setando o valor do diamentro da roda 
diatancia_roda = 13 # setando o valor da distancia entre os centro das rodas

robot = Robot(motor_esquerdo, motor_direito, diametro_roda, diatancia_roda) # setando o comando robot para utilizar  as saidas OUTPU_A e OUTPUT_B
pos = Odometry(motor_esquerdo, motor_direito, diametro_roda, diatancia_roda, 360, 360, debug=True)

# ---------- Configura os sensores

InfraredSensor.mode = 'IR-PROX' # modo do sensor de infravermelho por aproximação

# ---------- Sensores do primeiro Brick
color_sensor_esq = ColorSensor(INPUT_1)  # setando sensor de cor na entrada in1
color_sensor_esq.mode = 'COL-COLOR' # modo do sensor de cor RGB

color_sensor_dir = ColorSensor(INPUT_2)  # setando sensor de cor na entrada in2
color_sensor_dir.mode = 'COL-COLOR' # modo do sensor de cor RGB

ultrasonic_sensor = UltrasonicSensor(INPUT_3)  # setando sensor ultrassonico na entrada in3
ultrasonic_sensor.mode = 'US-DIST-CM' # modo do sensor ultrasonico em cm

robot._gyro = GyroSensor(INPUT_4) # setando o sensor de giro na entra in4
_gyro = 'GYRO-ANG' # modo do sensor gyroscopio em angulhos

cont = 0

while True:
    print(pos.get_pos())
    direction = 90 * cont
    robot.move(75,direction,20)
    sleep(1)
    cont += 1
    # robot.rotate(90,100,20)
    # sleep(1)
    # cont += 1
