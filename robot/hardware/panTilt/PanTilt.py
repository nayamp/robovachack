import sys
import pygame
from pygame.locals import *
import time
#import ikpy.chain
import numpy as np
#import ikpy.utils.plot as plot_utils
import matplotlib.pyplot as plt
import time
import board
from adafruit_motor import servo
from adafruit_pca9685 import PCA9685





#my_chain = ikpy.chain.Chain.from_urdf_file("../urdfs/mantisgripikpy.urdf")
i2c = board.I2C()
pca = PCA9685(i2c)
pca.frequency = 50
print("PCA attached")
default_angle=90

pan = servo.Servo(pca.channels[14])
tilt = servo.Servo(pca.channels[15])
uncat = servo.Servo(pca.channels[2])
print("servos SET")


class joystick_handler(object):
    def __init__(self, id):
        self.id = id
        self.joy = pygame.joystick.Joystick(id)
        self.name = self.joy.get_name()
        self.joy.init()
        self.numaxes    = self.joy.get_numaxes()
        self.numballs   = self.joy.get_numballs()
        self.numbuttons = self.joy.get_numbuttons()
        self.numhats    = self.joy.get_numhats()
        

        self.axis = []
        for i in range(self.numaxes):
            self.axis.append(self.joy.get_axis(i))

        self.ball = []
        for i in range(self.numballs):
            self.ball.append(self.joy.get_ball(i))

        self.button = []
        for i in range(self.numbuttons):
            self.button.append(self.joy.get_button(i))

        self.hat = []
        for i in range(self.numhats):
            self.hat.append(self.joy.get_hat(i))


class input_test(object):
    def init(self):
        pygame.init()
        pygame.event.set_blocked((MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN))
  
        self.joycount = pygame.joystick.get_count()
        if self.joycount == 0:
            print("This program only works with at least one joystick plugged in. No joysticks were detected.")
            self.quit(1)
        self.joy = []
        for i in range(self.joycount):
            self.joy.append(joystick_handler(i))
            print('Joystick Attached')


    def run(self):
        # self.screen = pygame.display.set_mode(self.resolution, RESIZABLE)
        # pygame.display.set_caption(self.program.nameversion)
        # self.circle.convert()
        pan_angle=default_angle
        tilt_angle=default_angle
        try:

            x,y,z=0,0,0
            while True:
                

                # time.sleep(.5)
                # for i in range(self.joycount):
                #     self.draw_joy(i)
                # pygame.display.flip()
                # self.clock.tick(30)
                for event in [pygame.event.wait(), ] + pygame.event.get():
                    # QUIT             none
                    # ACTIVEEVENT      gain, state
                    # KEYDOWN          unicode, key, mod
                    # KEYUP            key, mod
                    # MOUSEMOTION      pos, rel, buttons
                    # MOUSEBUTTONUP    pos, button
                    # MOUSEBUTTONDOWN  pos, button
                    # JOYAXISMOTION    joy, axis, value
                    # JOYBALLMOTION    joy, ball, rel
                    # JOYHATMOTION     joy, hat, value
                    # JOYBUTTONUP      joy, button
                    # JOYBUTTONDOWN    joy, button
                    # VIDEORESIZE      size, w, h
                    # VIDEOEXPOSE      none
                    # USEREVENT        code
                    if event.type == QUIT:
                        self.quit()
                    # elif event.type == KEYDOWN and event.key in [K_ESCAPE, K_q]:
                    #     self.quit()
                    # elif event.type == VIDEORESIZE:
                    #     self.screen = pygame.display.set_mode(event.size, RESIZABLE)
                    elif event.type == JOYAXISMOTION:
                        self.joy[event.joy].axis[event.axis] = event.value
                        if event.axis==1 and event.value>=.4:
                                pan_angle=pan_angle-.1
                                pan.angle=pan_angle
                                print('down1',pan_angle)
                        if event.axis==1 and event.value<=-.4:
                                pan_angle=pan_angle+.1
                                pan.angle=pan_angle
                                print('up1',pan_angle)
                                #print('up',x)
                        if event.axis==0 and event.value>=.4:
                                tilt_angle=tilt_angle+.1
                                tilt.angle=tilt_angle
                                print('right0',tilt_angle)
                        if event.axis==0 and event.value<=-.4:
                                tilt_angle=tilt_angle-.1
                                tilt.angle=tilt_angle
                                print('left0',tilt_angle)
                        else:
                            continue

                        # target_position=[x,y,z]
                        # print(target_position)
                        # fig, ax = plot_utils.init_3d_figure()
                        # my_chain.plot(my_chain.inverse_kinematics(target_position), ax, target=target_position)
                        # plt.xlim(-0.3, 0.3)
                        # plt.ylim(-0.3, 0.3)
                        # plt.pause(.1)
                        # plt.close('all')


                        #print('AXIS!  VALUE=',event.axis,event.value)
                    # elif event.type == JOYBALLMOTION:
                    #     self.joy[event.joy].ball[event.ball] = event.rel
                    #     print('BALL!  VALUE=',event.ball,event.rel)
                    # elif event.type == JOYHATMOTION:
                    #     self.joy[event.joy].hat[event.hat] = event.value
                    #     print('HAT!  VALUE=',event.hat,event.value)
                    # elif event.type == JOYBUTTONUP:
                    #     self.joy[event.joy].button[event.button] = 0
                    #     print('BUTTONUP!  VALUE=',event.button)
                    # elif event.type == JOYBUTTONDOWN:
                    #     self.joy[event.joy].button[event.button] = 1
                    #     print('BUTTONDOWN!  VALUE=',event.button)
        except KeyboardInterrupt:
            print('thanks')



    def quit(self, status=0):
        pygame.quit()
        sys.exit(status)

if __name__ == "__main__":
    program = input_test()
    program.init()
    program.run()  # This function should never return