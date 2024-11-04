import RPi.GPIO as gpio
import time
def init():    
    gpio.setmode(gpio.BCM)
    gpio.setup(27, gpio.OUT)
    gpio.setup(22, gpio.OUT)
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)
def forward(sec):
    gpio.output(27, True)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)
    time.sleep(sec)
def reverse(sec):
    gpio.output(27, False)
    gpio.output(22, True)
    gpio.output(23, False)
    gpio.output(24, True)
    time.sleep(sec)
def left_turn(sec):
    gpio.output(27, False)
    gpio.output(22, True)
    gpio.output(23, True)
    gpio.output(24, False)
    time.sleep(sec)
def right_turn(sec):
    gpio.output(27, True)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, True)
    time.sleep(sec)
def stop():
    gpio.output(27, False)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, False)

