import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522

 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(13,GPIO.OUT)

servo = GPIO.PWM(13,50)
 
#set GPIO Pins IN
GPIO_TRIGGER_IN = 12
GPIO_ECHO_IN = 11

#set GPIO Pins  OUT
GPIO_TRIGGER_OUT = 15
GPIO_ECHO_OUT = 16

# set Minimal Distance 
min_distance = 6
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER_IN, GPIO.OUT)
GPIO.setup(GPIO_ECHO_IN, GPIO.IN)
 
def distance_in():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER_IN, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_IN, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO_IN) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO_IN) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

def distance_out():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER_OUT, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER_OUT, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO_OUT) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO_OUT) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    
    try:
        while True:
            car_in = False
            while car_in==False:
                time.sleep(0.5)
                dist = distance_in()
                print(dist)
                if dist<min_distance:
                    car_in = True
            servo.start(0)
            time.sleep(0.5)
            read_reader = False
            while read_reader==False:
                reader = SimpleMFRC522()
                print("Letakkan kartu")
                # print("Letakkan kartu atau dekatkan tangan anda")
                # FOR OTHER SENSOR
                id, text = reader.read_no_block()
                while not id:
                    # FOR OTHER SENSOR
                    id, text = reader.read_no_block()
                print("ID: ", id)
                print("ID: ",text)
                if id:
                    # to local server
                    read_reader = True
            servo.ChangeDutyCycle(7)
            car_out = False
            while car_out==False:
                time.sleep(0.5)
                dist = distance_in()
                print(dist)
                if dist<min_distance:
                    car_out = True
            if car_out==True:
                time.sleep(5)        
                servo.ChangeDutyCycle(2)
                time.sleep(3)
                servo.ChangeDutyCycle(0)                 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        servo.stop()
        GPIO.cleanup()