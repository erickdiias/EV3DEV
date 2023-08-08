#!/usr/bin/env python3

# ---------- Importa as bibliotecas necessarias
from time import sleep #importando sleep da biblioteca time
from math import pi, sin, cos, sqrt
from ev3dev2.motor import * # importando tudo da biblioteca ev3dev2.motor


def get_position_delta(distance_left, distance_right, previous_angle, wheel_distance, curve_adjustment=0.875):
    # toma a distância percorrida pela roda esquerda e direita (e sua distância)
    # e um ângulo inicial, calcula a nova posição e orientação

    # movimento reto ou curva?
    if distance_right == distance_left:
        # movimento reto
        delta_angle = 0
        delta_distance = abs(distance_left)
        delta_x = distance_left * sin(previous_angle)
        delta_y = distance_left * cos(previous_angle)
    else:
        # movimento da curva

        # ajustes de distância da curva. olhe para leia-me
        try:
            relation = distance_left / distance_right
        except ZeroDivisionError:
            relation = 0

        if relation > 0.5 and relation < 2:
            factor = 1
        else:
            factor = curve_adjustment

        distance_left *= factor
        distance_right *= factor

        distance_difference = distance_left - distance_right
        radius_left = (distance_left * wheel_distance) / distance_difference
        radius_right = (distance_right * wheel_distance) / distance_difference

        try:
            angle = distance_left / radius_left
        except ZeroDivisionError:
            angle = distance_right / radius_right

        radius = (radius_left + radius_right) / 2
        delta_angle = angle
        euclidean_distance = sqrt(2 * radius * radius * (1 - cos(angle)))
        # conforme definido por readme
        angle_lambda = ((pi - angle) / 2) - previous_angle
        delta_x = euclidean_distance * cos(angle_lambda)
        delta_y = euclidean_distance * sin(angle_lambda)
        delta_distance = abs(radius * angle)

    # construir dados de retorno
    delta_dict = {
        'delta_angle': delta_angle,
        'delta_distance': delta_distance,
        'delta_x': delta_x,
        'delta_y': delta_y,
    }
    return delta_dict

# Classe para controlar o robô e sua odometria
class _odometria:
    def __init__(self, left=None, right=None, wheel_diameter=5.5, wheel_distance=12, count_per_rot_left=None, count_per_rot_right=None, debug=False, curve_adjustment=0.875):
        allowed_ports = ['A', 'B', 'C', 'D'] # Portas permitidas para conectar o brick (A, B, C e D)
        if left not in allowed_ports or right not in allowed_ports: # Verificação se a porta left e right está dentro das portas permitidas 
            if left not in allowed_ports: # Se a porta left não estiver dentro das portas permitidas
                error_location = 'left' # Guarda na variavel "error_location" que a left não esta dentro das portas permitidas
            if right not in allowed_ports: # Se a porta right não estiver dentro das portas permitidas
                if left not in allowed_ports: # Se a porta left não estiver dentro das portas peritidas
                    error_location = 'left and right' # Guarda na variavel "error_location" que as left e right não está dentro das portas permitidas
                error_location = 'right' # Guardar na varial "error_location" que a right nãi está dentro das portas permitidas
            raise RuntimeError('The ' + error_location + ' motor port given is none of the allowed ports: ' + ', '.join(allowed_ports)) # Retornara a mensagem de erro informado as portas
        
        # self, serve para voce acessar as propriedades os metodos de uma instancia
        self.__wheel_diameter = wheel_diameter # Armazenando a propriedade de wheel_diameter
        self.__wheel_distance = wheel_distance # Armazenando a propriedade wheel_distance

        self.__debug = debug # Armazenando a propriedade de debug

        self.__curve_adjustment = curve_adjustment # Armazenado a propriedade curve_adjustment

        # Roda do motor de inicialização
        self.__motor_left = LargeMotor('out' + left) # Armazenado a propriedade do motor esquerdo
        self.__motor_right = LargeMotor('out' + right) # Armazenado a propriedade do motor direito

        if count_per_rot_left is None: # Se "count_per_rot_left" eh nada
            self.__count_per_rot_left = self.__motor_left.count_per_rot # Armazenado a propriedade de contagem de tachos por resolucao do motor esquerdo
        else:
            self.__count_per_rot_left = count_per_rot_left # Armazenado a propriedade de contagem de tachos do motor esquerdo

        if count_per_rot_right is None:
            self.__count_per_rot_right = self.__motor_right.count_per_rot # Armazenado a propriedade de contagem de tachos por resolucao do motor direito
        else:
            self.__count_per_rot_right = count_per_rot_right # Armazenado a propriedade de contagem de tachos do motor direito

       # init logs
        self.__movement_logs = [] # Registro de momento
        self.__save_current_pos() # Salva a posicao atual
        self.stop() #Para

        # cache de posição inicial
        self.__pos_cache = {
            'x': 0, # Armazenado o valor de posicao inicial 0 em x
            'y': 0, # Armazenado o valor de posicao inicial 0 em y
            'angle': 0, # Armazenado o valor de posicao inicial 0 em angle
            'distance': 0, # Armazenado o valor de posicao inicial 0 em distance
        }

    # Funcao para salvar a posicao atual
    def __save_current_pos(self):
        # Criado um instancia para salvar a ultima posicao dos motores
        self.__last_pos = {
            'left': self.__motor_left.position, # Armazenado o valor da posição atual do motor em pulsos do encoder rotativo "left"
            'right': self.__motor_right.position # Armazenado o valor da posição atual do motor em pulsos do encoder rotativo "right"
        }

    def __add_log(self):
        # obtém a diferença desde a última medição ate atual
        new_log = {
            'delta_position_left': self.__motor_left.position - self.__last_pos['left'],
            'delta_position_right': self.__motor_right.position - self.__last_pos['right'],
        }
        # Vai adicionando o valor new_log ao final da lista __movement_logs. O resultado será uma lista que contém todos os registrados durante a execução do código.
        self.__movement_logs.append(new_log) 
        self.__save_current_pos() # Salva a posição atual

    def __get_deltas(self, log_dict, previous_angle):
        # pega um dicionário de log e calcula as diferenças para a nova posição e orientação
        # apenas calcula a distância percorrida e passa para a função
        wheel_diameter = self.__wheel_diameter
        wheel_distance = self.__wheel_distance
        count_per_rot_left = self.__count_per_rot_left
        count_per_rot_right = self.__count_per_rot_right

        circumference = wheel_diameter * pi

        tacho_counts_left = log_dict['delta_position_left']
        tacho_counts_right = log_dict['delta_position_right']
        rotations_left = tacho_counts_left / count_per_rot_left
        rotations_right = tacho_counts_right / count_per_rot_right
        distance_left = rotations_left * circumference
        distance_right = rotations_right * circumference

        return get_position_delta(
            distance_left=distance_left,
            distance_right=distance_right,
            previous_angle=previous_angle,
            wheel_distance=wheel_distance,
            curve_adjustment=self.__curve_adjustment
        )

    def __print_current_pos(self):
        # prints the current position
        if self.__debug:
            current_pos = self.__current_pos()
            print('currently at x=' + str(current_pos['x']) + ', y=' + str(current_pos['y']) + ', angle=' + str(current_pos['angle']) +
                  ' (' + str((current_pos['angle'] / pi) * 180) + ' degrees), total distance=' + str(current_pos['distance']))

    def __current_pos(self):
        self.__add_log()
        current_x = self.__pos_cache['x']
        current_y = self.__pos_cache['y']
        current_angle = self.__pos_cache['angle']
        current_distance = self.__pos_cache['distance']

        while len(self.__movement_logs) > 0:
            single_log_dict = self.__movement_logs.pop(0)

            # calculate position
            deltas = self.__get_deltas(single_log_dict, current_angle)

            current_x += deltas['delta_x']
            current_y += deltas['delta_y']
            current_angle += deltas['delta_angle']
            current_angle = current_angle % (2 * pi)
            current_distance += deltas['delta_distance']

        self.__pos_cache = {
            'x': current_x,
            'y': current_y,
            'angle': current_angle % (2 * pi),
            'distance': current_distance,
        }

        return self.__pos_cache

    def get_current_pos(self):
        current_pos = self.__current_pos()
        return current_pos['x'], current_pos['y']

    @property
    def x(self):
        return self.__current_pos()['x']

    @x.setter
    def x(self, newx):
        self.__add_log()
        self.__set_position(delta_x=newx - self.x)

    @property
    def y(self):
        return self.__current_pos()['y']

    @y.setter
    def y(self, newy):
        self.__add_log()
        self.__set_position(delta_y=newy - self.y)

    @property
    def orientation(self):
        return self.__current_pos()['angle']

    @orientation.setter
    def orientation(self, new_orientation):
        self.__set_position(delta_angle=new_orientation - self.orientation)

    @property
    def distance(self):
        return self.__current_pos()['distance']

    @distance.setter
    def distance(self, new_distance):
        self.__add_log()
        self.__set_position(delta_distance=new_distance - self.distance)

    def stop(self):
        self.__add_log()
        self.__motor_left.stop()
        self.__motor_right.stop()

    def wait(self):
        self.__motor_left.wait_while('running')
        self.__motor_right.wait_while('running')

    def move(self, right=None, left=None, time=None, blocking=None):
        # # adiciona um waypoint (log de movimento)
        self.__add_log()
        # debugging
        self.__print_current_pos()

        if time is not None:
            if left is not None:
                self.__motor_left.run_timed(time_sp=time * 1000, speed_sp=left)
            if right is not None:
                self.__motor_right.run_timed(time_sp=time * 1000, speed_sp=right)

            # time given: blocking by default
            # => block when blocking=None (default) or blocking=True
            if blocking is None or blocking:
                self.wait()
        else:
            # no time is set => run indefinitely
            if left is not None:
                self.__motor_left.run_forever(speed_sp=left)
            if right is not None:
                self.__motor_right.run_forever(speed_sp=right)
            # no time given: non-blocking by default
            # => only block when blocking=True is given
            if blocking:
                self.wait()

    def change_speed(self, left=0, right=0):
        self.move(left=self.speed_left + left)
        self.move(right=self.speed_right + right)

    def __set_position(self, delta_x=0, delta_y=0, delta_angle=0, delta_distance=0):
        # clear logs
        self.get_current_pos()
        self.__pos_cache = {
            'x': self.__pos_cache['x'] + delta_x,
            'y': self.__pos_cache['y'] + delta_y,
            'angle': self.__pos_cache['angle'] + delta_angle,
            'distance': self.__pos_cache['distance'] + delta_distance,
        }

    @property
    def speed_left(self):
        return self.__motor_left.speed

    @speed_left.setter
    def speed_left(self, new_speed):
        self.move(left=new_speed)

    @property
    def speed_right(self):
        return self.__motor_right.speed

    @speed_right.setter
    def speed_right(self, new_speed):
        self.move(right=new_speed)

    def __get_log_str(self, log):
        log_line = ''
        log_line += 'Left:  ' + str(log['speed_left']) + '; '
        log_line += 'Right: ' + str(log['speed_right']) + '; '
        log_line += 'Time:  ' + str(log['time'])
        return log_line

    def print_movement_logs(self):
        if self.__debug:
            print('\tleft\tright\tdeltax\tdeltay\tdeltaphi')
            cnt = 0
            current_angle = 0
            for single_log_dict in self.__movement_logs:
                cnt += 1
                deltas = self.__get_deltas(single_log_dict, current_angle)
                current_angle += deltas['delta_angle']
                print('#' + str(cnt) + '\t' +
                      str(round(single_log_dict['delta_position_left'])) + '\t' +
                      str(round(single_log_dict['delta_position_right'])) + '\t' +
                      str(round(deltas['delta_x'], 2)) + '\t' +
                      str(round(deltas['delta_y'], 2)) + '\t' +
                      str(round((deltas['delta_angle'] / pi) * 180))
                      )

    def __exit__(self):
        self.stop()

    def __del__(self):
        self.__print_current_pos()
        self.print_movement_logs()
