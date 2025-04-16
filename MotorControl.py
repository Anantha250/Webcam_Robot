import RPi.GPIO as GPIO
import time

# ตั้งค่า GPIO
in1 = 17
in2 = 18
ena = 22

try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    from fake_rpi.RPi import GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(ena, GPIO.OUT)

pwm = GPIO.PWM(ena, 1000)
pwm.start(0)

def move_forward(speed=50):
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    pwm.ChangeDutyCycle(speed)

def move_backward(speed=50):
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    pwm.ChangeDutyCycle(speed)

def stop():
    pwm.ChangeDutyCycle(0)

try:
    move_forward(70)
    time.sleep(2)
    move_backward(70)
    time.sleep(2)
    stop()

except KeyboardInterrupt:
    pass

GPIO.cleanup()
