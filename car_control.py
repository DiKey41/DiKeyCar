import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


#GPIO.setmode(GPIO.BOARD)
#Motor1B = 18 #Gpio 24
#Motor1A= 22 #Gpio 25
#PWM = 12 #Gpio 18

GPIO.setup(13, GPIO.OUT)
p = GPIO.PWM(13, 50)  # channel=23 frequency=50Hz
p.start(5.3)



speed1 = 99
speed2 = 49

motor1b=24
motor1a=25
motorEn=18

GPIO.setmode(GPIO.BCM)
GPIO.setup(motor1b,GPIO.OUT)
GPIO.setup(motor1a,GPIO.OUT)
GPIO.setup(motorEn,GPIO.OUT)

motorPwm=GPIO.PWM(motorEn,100)
motorPwm.start(0)





def move_forward():
    GPIO.output(motor1a,GPIO.HIGH)
    GPIO.output(motor1b,GPIO.LOW)
    motorPwm.ChangeDutyCycle(speed1)
        
def move_backward():
    GPIO.output(motor1a,GPIO.LOW)
    GPIO.output(motor1b,GPIO.HIGH)
    motorPwm.ChangeDutyCycle(speed1)
    
def car_neutral():
    GPIO.output(motor1a,GPIO.LOW)
    GPIO.output(motor1b,GPIO.LOW)
    
def clean_GPIO():
    GPIO.cleanup()
    motorPwm.stop()
    
def car_stop():
    GPIO.output(motor1a,GPIO.HIGH)
    GPIO.output(motor1b,GPIO.HIGH)
    
def turn_left():
    p.ChangeDutyCycle(3.3)

def turn_right():
    p.ChangeDutyCycle(8.3)


def turn_neutral():
    p.ChangeDutyCycle(5.3)

      
if __name__== '__main__':
    move_forward()
    time.sleep(1)
    clean_GPIO()
