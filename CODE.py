#!/usr/bin/env python3

# ---------- Importa as bibliotecas necessarias
import time # importando o tempo para a logica de programacao
import math # importando a matematica para a logica de programaaao
from ev3dev2.motor import * # importando tudo da biblioteca ev3dev2.motor
from ev3dev2.sound import Sound # importando o som da biblioteca ev3dev2.sound
from ev3dev2.button import Button # importando os botoes da biblioteca ev3dev2.button
from ev3dev2.sensor import * # importando tudo da biblioteca ev3dev2.sensor
from ev3dev2.sensor.lego import * # importando tudo da biblioteca ev3dev2.sensor.lego
#from ev3dev2.sensor.virtual import * # importando tudo da biblioteca ev3dev2.sensor.virtual


# ----------
sound = Sound() # Setando a variavel som
#button = Button() # Setando a variavel botao
#radio = Radio()  # Setando a variavel radio

# ---------- Configura os motores
motorA = LargeMotor(OUTPUT_A) # Setando o motor na saida A como motorA
motorB = LargeMotor(OUTPUT_B) # Setando o motor na saida B como motorB

left_motor = motorA # Traduzindo que o motorA como motor da esquerda
right_motor = motorB # Traduzindo que o motorB como motor da direita
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B) # Setando o comando Tank_drive para utilizar os motores A e B juntos
steering_drive = MoveSteering(OUTPUT_A, OUTPUT_B) # Setando o comando steering_drive para utilizar a curva com os motores A e B

# ---------- Configura os sensores



InfraredSensor.mode = 'IR-PROX' # modo do sensor de infravermelho por aproximação

# ---------- Sensores do primeiro Brick
color_sensor_in1 = ColorSensor(INPUT_1)  # setando sensor de cor na entrada in1
color_sensor_in1.mode = 'COL-COLOR' # modo do sensor de cor RGB

color_sensor_in2 = ColorSensor(INPUT_2)  # setando sensor de cor na entrada in2
color_sensor_in2.mode = 'COL-COLOR' # modo do sensor de cor RGB

ultrasonic_sensor_in3 = UltrasonicSensor(INPUT_3)  # setando sensor ultrassonico na entrada in3
ultrasonic_sensor_in3.mode = 'US-DIST-CM' # modo do sensor ultrasonico em cm

gyro_sensor_in4 = GyroSensor(INPUT_4) # setando o sensor de giro na entra in4
gyro_sensor_in4.mode = 'GYRO-ANG' # modo do sensor gyroscopio em angulhos


# ---------- Aqui é onde seus codigos começam


# ---------- Inicio das Funções


def corrigir_alinhamento_sensor_cor():
    if color_sensor_in1.color == 5 and color_sensor_in2 == 6:
        while color_sensor_in2 == 6:
            tank_drive.on(0,2)
        gyro_sensor_in4.reset() # Reset no sensor de gyro para o vaor de zero

    elif color_sensor_in1.color == 6 and color_sensor_in2 == 5:
        while color_sensor_in1 == 6:
            tank_drive.on(2,0)
        gyro_sensor_in4.reset() # Reset no sensor de gyro para o vaor de zero
    
def localizar_zona_azul():
    
    while color_sensor_in1.color != 2: # Realiza o comando ate identificar a cor azul(2)
        
        if color_sensor_in1.color == 6 and color_sensor_in2.color == 6: # verifica se o valor do sensor1 é igual 6(branco)
            tank_drive.on(10,10) # movimenta os motorA e motorB
            
        elif color_sensor_in1.color == 1 or color_sensor_in1.color == 4: # Verifica se o sensor1 não está lendo preto ou amarelo
            tank_drive.on_for_seconds(-5,-5,5) # Movimenta o motorA e motorB por 5segundos para trás
            while gyro_sensor_in4.angle < 90: # Enquanto o sensor de gyro estiver menor que 90
                tank_drive.on(5,-5) # Movimenta o motorA e o motorB em direções opostas para esquerda
            gyro_sensor_in4.reset() # Reseta o valor do sensor de gyro par 0 graus
            
        elif color_sensor_in1.color == 5 and color_sensor_in2.color == 5: # Os dois sensores e cor então alinhados e identificando a mesma cor
            tank_drive.on_for_seconds(-5,-5,5) # O motorA emotor B vão se movimentar por 5seg para trás
            while gyro_sensor_in4.angle < 180: # Enquanto o o sensor de gyro identificar que o valor do angulo é menor que 180 graus ele gira  
                tank_drive.on(5,-5) # MotorA e motorB se movimentam em direções opostas 
            gyro_sensor_in4.reset() # Reset no sensor de gyro para o vaor de zero

        elif color_sensor_in1.color == 5 and color_sensor_in2 == 6:
            while color_sensor_in2 == 6:
                tank_drive.on(0,2)
            gyro_sensor_in4.reset() # Reset no sensor de gyro para o vaor de zero

        elif color_sensor_in1.color == 6 and color_sensor_in2 == 5:
            while color_sensor_in1 == 6:
                tank_drive.on(2,0)
            gyro_sensor_in4.reset() # Reset no sensor de gyro para o vaor de zero

    tank_drive.off()


executado = False
def inicializando():
    global executado
    if executado != True: #código desejada é executada apenas quando a variável executado é falsa. Após a execução da linha, a variável executado é atualizada para True, garantindo que a linha não seja executada novamente
        sound.speak('lets go') #Executa um comando de voz no brick 'lets go', signicando que ocorreu tudo certo com o codigo 
        gyro_sensor_in4.reset() #reseta o valor do gyro para iniciar em 0 graus
        executado = True  #torna o executando um valor verdadeiro, encerrando o laço

# ---------- Inicio do código

while True:
    
    inicializando() #Função de inicialização para saber se o robo não está em falha. Vai emitir um sinal sonoro
    localizar_zona_azul() #Função que procura a zona azul