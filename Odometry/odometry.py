from math import pi, sin, cos, sqrt
import math
from ev3dev2.motor import *
import time


class Odometry:
    def __init__(self, left=None, right=None, wheel_diameter=5.6, wheel_distance=15.2, count_per_rot_left=None, count_per_rot_right=None, debug=False) -> None:

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
            print('oi')
        else:
            raise Exception("Debug mode is not enabled")
