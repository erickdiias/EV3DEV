from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
import math
import time

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
