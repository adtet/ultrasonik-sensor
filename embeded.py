import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522

 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13,GPIO.OUT)

servo = GPIO.PWM(13,50)
 
#set GPIO Pins
GPIO_TRIGGER = 12
GPIO_ECHO = 11
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    reader = SimpleMFRC522()
    try:
        
        while True:
            dist = distance()
            print(dist)
            servo.start(0)
            time.sleep(0.5)
            if dist<6:
                try:
                    print("Letakkan kartu :")     
                    id,text = reader.read()
                    print(id)
                    print(text)
                    servo.ChangeDutyCycle(7)
                    time.sleep(0.5)
                finally:
                    time.sleep(5)
                    servo.ChangeDutyCycle(2)
                    time.sleep(1)
                    servo.ChangeDutyCycle(0)
                    
            else:
                print("On")
                                 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        servo.stop()
        GPIO.cleanup()