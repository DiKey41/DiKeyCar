import pygame
import RPi.GPIO as GPIO
from time import sleep
import car_control as cc
GPIO.setwarnings(False)


def init():
    pygame.init()
    win = pygame.display.set_mode((100,100))
 
def press(keyName):
    ans = False
    for eve in pygame.event.get():pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame,'K_{}'.format(keyName))
    if keyInput [myKey]:
        ans = True
    pygame.display.update()
    
    return ans
 

def main():
    if press('UP'):
        cc.move_forward()      
        
    elif press('DOWN'):
        cc.move_backward()
        
    elif press('SPACE'):
        cc.car_stop()

    else:
        cc.car_neutral()
        
    if press('LEFT'):
        cc.turn_left()
        
    elif press('RIGHT'):
        cc.turn_right()
        
    else:
        cc.turn_neutral()

        

 
if __name__ == '__main__':
    init()
    while True:
        main()
