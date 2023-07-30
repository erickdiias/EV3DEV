from ev3dev2.motor import *
from ev3dev2.sensor import *
from ev3dev2.sensor.lego import *
import math
import time

class Encoder(LargeMotor):
    def __init__(self,ticks_p_revol, radius,port=None):
        LargeMotor.__init__(self,port)
        self.counter = 0
        self.ticks_p_revol = ticks_p_revol
        self.radius = radius
        

    def count(self):
        self.counter += 1
    
    def reset(self):
        self.counter = 0


class Odometry:
    def __init__(self,left_encoder,right_encoder,L,debug=False) -> None:
        self.left_encoder = left_encoder
        self.right_encoder = right_encoder
        self.L = L
        self.debug = debug

        self.left_wheel_last_count = 0
        self.right_wheel_last_count = 0

        self.x = 0
        self.y = 0
        self.theta = 0

        self.meters_per_tick_left = 2 * math.pi * self.left_encoder.radius / self.left_encoder.ticks_p_revol
        self.meters_per_tick_right = 2 * math.pi * self.right_encoder.radius / self.right_encoder.ticks_p_revol
    
    def step(self,left_direction=1,right_direction=1):
        delta_ticks_left = (self.left_encoder.position - self.left_wheel_last_count) * left_direction
        delta_ticks_right = (self.right_encoder.position - self.right_wheel_last_count) * right_direction

        self.left_wheel_last_count = self.left_encoder.position
        self.right_wheel_last_count = self.right_encoder.position


        DR = self.meters_per_tick_right * delta_ticks_right
        DL = self.meters_per_tick_left * delta_ticks_left
        D = (DR + DL) / 2


        x_dt = D * math.cos(self.theta)
        y_dt = D * math.sin(self.theta)
        theta_dt = (DR - DL) / self.L

        self.x = self.x + x_dt
        self.y = self.y + y_dt
        self.theta = self.theta + theta_dt

        return self.x, self.y, self.theta
    
    def reset(self):
        self.x = 0
        self.y = 0
        self.theta = 0
    
    def get_pos(self):
        return self.x, self.y, self.theta
    
    def log_pos(self):
        if self.debug:
            print(f'x: {self.x} y: {self.y} theta: {self.theta}')
        else:
            raise Exception('Debug mode is not enabled')




class Robot(MoveSteering):
    def __init__(self, left_motor_port, right_motor_port, wheel_distance=15.2, wheel_diam=5.6, desc=None, motor_class=LargeMotor):
        MoveSteering.__init__(self, left_motor_port, right_motor_port, desc, motor_class)
        #Medidas do robo e rodas
        self.wheel_distance = wheel_distance  # Distância entre as rodas do robô
        self.wheel_diam = wheel_diam  # Diâmetro das rodas do robô
        self.wheel_radius = wheel_diam / 2  # Raio das rodas do robô
        self.wheel_circumference = wheel_diam * math.pi  # Circunferência das rodas do robô
        self.C = wheel_distance * math.pi  # Circunferência do círculo de rotação completo do robô
        

        # GYRO
        self._gyro = None  # Sensor giroscópio


        self.left_motor = LargeMotor(left_motor_port)  # Motor esquerdo
        self.right_motor = LargeMotor(right_motor_port)  # Motor direito


        #Odometria
        self.left_encoder = Encoder(self.left_motor.count_per_rot, self.wheel_radius,port=left_motor_port)
        self.right_encoder = Encoder(self.right_motor.count_per_rot, self.wheel_radius,port=right_motor_port)
        self.odometry = Odometry(self.left_encoder, self.right_encoder, self.wheel_distance)


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
    

    def on_to_coordinates(self):
        pass

    def kalmmam_filter(self):
        pass
