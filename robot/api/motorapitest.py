from flask import Flask
from flask import render_template, request
import RPi.GPIO as gpio
import time
app = Flask(__name__)

gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(27, gpio.OUT)
gpio.setup(22, gpio.OUT)
gpio.setup(23, gpio.OUT)
gpio.setup(24, gpio.OUT)
a=1

@app.route("/")

def index():

    return render_template('robot.html')

@app.route('/left')

def left():
    gpio.output(27, True)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)
    stop()
    return "left"

@app.route('/right')

def right():
    gpio.output(27, False)
    gpio.output(22, True)
    gpio.output(23, False)
    gpio.output(24, True)
    stop()
    return "right"

@app.route('/forward')

def forward():
    gpio.output(27, False)
    gpio.output(22, True)
    gpio.output(23, False)
    gpio.output(24, True)
    stop()
    return "forward"

@app.route('/reverse')

def reverse():
    gpio.output(27, True)
    gpio.output(22, False)
    gpio.output(23, True)
    gpio.output(24, False)
    stop()
    return "reverse"

@app.route('/stop')
def stop():
    gpio.output(27, False)
    gpio.output(22, False)
    gpio.output(23, False)
    gpio.output(24, False)
    return "stop"

if __name__ == "__main__":

 print("start")
 app.run(host='0.0.0.0',port=5010)

