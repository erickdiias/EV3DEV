#!/usr/bin/env python3

# Para que o script possa ser executado no Brickman
import termios, tty, sys, time
from ev3dev2.motor import *
from threading import *
from ev3dev2.sound import Sound # importando o som da biblioteca ev3dev2.sound

sound = Sound() # Setando a variavel som

motor_right = LargeMotor('outB')
motor_left = LargeMotor('outC')


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    ch = sys.stdin.read(1)
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch

def forward():
    sound.speak('forward')
    motor_left.run_forever(speed_sp=400)
    motor_right.run_forever(speed_sp=400)
    
#==============================================

def back():
    sound.speak('back')
    motor_left.run_forever(speed_sp=-400)
    motor_right.run_forever(speed_sp=-400)
    
#==============================================

def left():
    sound.speak('left')
    motor_left.run_forever(speed_sp=-200)
    motor_right.run_forever(speed_sp=200)
    
#==============================================

def right():
    sound.speak('right')
    motor_left.run_forever(speed_sp=200)
    motor_right.run_forever(speed_sp=-200)
    
#==============================================

def stop():
    sound.speak('stop')
    motor_left.run_forever(speed_sp=0)
    motor_right.run_forever(speed_sp=0)
    
#==============================================

while True:
    k = getch()
    print(k)
    if k == 's':
        back()
    if k == 'w':
        forward()
    if k == 'd':
        right()
    if k == 'a':
        left()
    if k == ' ':
        stop()
    if k == 'q':
        exit()
