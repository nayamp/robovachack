from flask import Flask
from flask import render_template, request
import RPi.GPIO as GPIO
import time
from hardware import motortest
app = Flask(__name__)

motortest.init()

a=1

@app.route("/")

def index():

    return render_template('robot.html')

@app.route('/left_side')

def left_side():
    motortest.left_turn(3)
    return 200

@app.route('/right_side')

def right_side():
    motortest.right_turn(3)
    return 200

@app.route('/up_side')

def up_side():
    motortest.forward(3)
    return 200

@app.route('/down_side')

def down_side():
    motortest.reverse()
    return 200

@app.route('/stop')

def stop():
   motortest.stop()


if __name__ == "__main__":

 print("start")
 app.run(host='0.0.0.0',port=5010)

