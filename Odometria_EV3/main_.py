#!/usr/bin/env python3

from ev3dev2.motor import * # importando tudo da biblioteca ev3dev2.motor
from odometria_ import _odometria
from time import sleep


# left='B'                      A roda esquerda está conectada à porta B                                    
# right='C'                     A roda direita está conectada à porta c
# wheel_diameter=6.8            Diâmetro da roda em centímetros
# wheel_distance=13.4           Distância entre as rodas em centímetros
# count_per_rot_left=None       Contagens de tacho por rotação do motor esquerdo
# count_per_rot_right=360       Contagens de tacho por rotação do motor direito
# debug=False                   Imprime a posição atual (na alteração da velocidade do motor)
# curve_adjustment=0.875        Use o fator de ajuste da curva

# Criar o objeto da classe _odometria                             
pos_info = _odometria(left='A', right='B', wheel_diameter=6.8, wheel_distance=13.4,
                      count_per_rot_left=None, count_per_rot_right=360, debug=True,
                      curve_adjustment=1)
