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
from ev3dev2.sensor.virtual import * # importando tudo da biblioteca ev3dev2.sensor.virtual
from math import pi, sin, cos, sqrt

class Robot(MoveSteering):
    def __init__(self, left_motor_port=None, right_motor_port=None, wheel_diam=None, wheel_distance=None, desc=None, motor_class=LargeMotor):
        MoveSteering.__init__(self, left_motor_port, right_motor_port, desc, motor_class)
        
        # Medidas do robo e rodas
        self.wheel_distance = wheel_distance  # Distância entre as rodas do robô
        self.wheel_diam = wheel_diam  # Diâmetro das rodas do robô
        self.wheel_radius = wheel_diam / 2  # Raio das rodas do robô
        self.wheel_circumference = wheel_diam * math.pi  # Circunferência das rodas do robô
        self.C = wheel_distance * math.pi  # Circunferência do círculo de rotação completo do robô
        
        # GYRO
        self._gyro = None  # Sensor giroscópio (não está implementado no código fornecido)
        
        self.left_motor = LargeMotor(left_motor_port)  # Motor esquerdo
        self.right_motor = LargeMotor(right_motor_port)  # Motor direito

    def on_for_distance(self, steering, speed, distance, brake=True, block=True):
        rotations = distance / self.wheel_circumference  # Número de rotações necessárias para percorrer a distância
        MoveSteering.on_for_rotations(self, steering, speed, rotations, brake, block)

    def rotate(self, n, steering, vel):
        arc = (n) * self.C  # Comprimento do arco a ser percorrido em uma rotação completa
        degrees = (arc / self.wheel_circumference)  # Número de graus a serem girados
        MoveSteering.on_for_degrees(self, steering, vel, degrees)  # Gira o robô pelo número de graus especificado
        self.left_motor.wait_while('running', 5000)  # Aguarda até que o motor esquerdo pare de girar
        MoveSteering.stop(self)  # Para o movimento do robô

    def move(self, distance, direction, vel, use_gyro=True, factor=10):
        degrees = (distance / self.wheel_circumference) * 360  # Número de graus a serem percorridos
        target = self.left_motor.position + degrees  # Posição de destino para o movimento

        if use_gyro:
            while self.left_motor.position <= target:
                error = (direction - self._gyro.angle) * factor  # Cálculo do erro para correção com o uso do giroscópio
                error = max(min(error, 100), -100)  # Limita o erro no intervalo [-100, 100]
                MoveSteering.on(self, error, vel)  # Move o robô com base no erro e na velocidade
            MoveSteering.stop(self)  # Para o movimento do robô

        else:
            raise NotImplementedError("Não implementado")  # Lança uma exceção se o uso do giroscópio não estiver implementado


class Odometry:
    def __init__(self, left=None, right=None, wheel_diameter=None, wheel_distance=None, count_per_rot_left=None, count_per_rot_right=None, debug=False) -> None:

        #motores
        self.left_motor = LargeMotor(left)
        self.right_motor = LargeMotor(right)
        #medidas

        self.wheel_diameter = wheel_diameter
        self.wheel_radius = wheel_diameter / 2
        self.wheel_distance = wheel_distance
        self.wheel_circumference = wheel_diameter * pi

        #
        self.ticks_right = count_per_rot_right
        self.ticks_left = count_per_rot_left
        #
        self.C = wheel_distance * pi
        self.cm_per_tick = self.wheel_circumference / 360

        #debug 
        self.debug = debug

        #odometria
        self.x = 0
        self.y = 0
        self.theta = 0

        self.ticks_count_left = 0  # Contagem de ticks do motor esquerdo
        self.ticks_count_right = 0  # Contagem de ticks do motor direito
        self.last_ticks_left = 0  # Última contagem de ticks do motor esquerdo
        self.last_ticks_right = 0  # Última contagem de ticks do motor direito  

        # Se possível usar o time.time_ns() 
        try:
            self.start_time = time.time_ns()
        except:
            self.start_time = time.time()
    
    def get_pos(self):
        #TODO: Implementar filtro de Kalman, o robô está perdendo a posição com o tempo
        t = time.time()
        dt = t - self.start_time

        delta_ticks_left = self.left_motor.position - self.last_ticks_left  # Diferença de ticks no motor esquerdo
        delta_ticks_right = self.right_motor.position - self.last_ticks_right  # Diferença de ticks no motor direito

        # Atualiza as contagens
        self.last_ticks_left = self.left_motor.position
        self.last_ticks_right = self.right_motor.position
        self.start_time = t

        Dl = self.cm_per_tick * delta_ticks_left  # Distância percorrida pelo motor esquerdo
        Dr = self.cm_per_tick * delta_ticks_right  # Distância percorrida pelo motor direito
        Dc = (Dl + Dr) / 2  # Distância percorrida pelo centro do robô

        x_dt = Dc * math.cos(self.theta)  # Componente x do deslocamento
        y_dt = Dc * math.sin(self.theta)  # Componente y do deslocamento
        theta_dt = (Dr - Dl) / self.wheel_distance  # Variação do ângulo de rotação

        self.x = self.x + x_dt  # Atualiza a posição x
        self.y = self.y + y_dt  # Atualiza a posição y
        self.theta = self.theta + theta_dt  # Atualiza o ângulo de rotação

        return self.x, self.y, self.theta

    def log_pos(self):
        x, y, theta = self.get_pos()
        if self.debug:
            print('x =', x)
            print('y =', y)
            print('theta =', theta)
            #print(f'x: {x} y: {y} theta: {theta}')
        else:
            raise Exception("Debug mode is not enabled")




# ---------- Parametros
motor_esquerdo = OUTPUT_A # setando motor_esquerdo como saída OUTPUT_A
motor_direito = OUTPUT_B # setando motor_direito como saída OUTPUT_B

diametro_roda = 6.88 # setando o valor do diamentro da roda 
diatancia_roda = 13 # setando o valor da distancia entre os centro das rodas

robot = Robot(motor_esquerdo, motor_direito, diametro_roda, diatancia_roda) # setando o comando robot para utilizar  as saidas OUTPU_A e OUTPUT_B
odometry = Odometry(motor_esquerdo, motor_direito, diametro_roda, diatancia_roda, None, 360, debug=False)

# ---------- Configura os sensores



# ---------- Sensores do primeiro Brick
color_sensor_esq = ColorSensor(INPUT_1)  # setando sensor de cor na entrada in1
color_sensor_esq.mode = 'COL-COLOR' # modo do sensor de cor RGB

ultrasonic_sensor = UltrasonicSensor(INPUT_2)  # setando sensor ultrassonico na entrada in3
ultrasonic_sensor.mode = 'US-DIST-CM' # modo do sensor ultrasonico em cm

robot._gyro = GyroSensor(INPUT_3) # setando o sensor de giro na entra in4
robot._gyro.mode = 'GYRO-ANG' # modo do sensor gyroscopio em angulhos

cont = 0

while True:
    print(odometry.get_pos())
    direction = 90 * cont
    robot.move(75,direction,20)
    sleep(1)
    cont += 1
    # robot.rotate(90,100,20)
    # sleep(1)
    # cont += 1