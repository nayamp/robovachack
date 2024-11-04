import sys
import pygame
from pygame.locals import *
import requests

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

    def run(self):
        # self.screen = pygame.display.set_mode(self.resolution, RESIZABLE)
        # pygame.display.set_caption(self.program.nameversion)
        # self.circle.convert()

        while True:
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
                while event.type == JOYAXISMOTION:
                    self.joy[event.joy].axis[event.axis] = event.value
                    if event.value>.06 or event.value<-.06:
                        if event.axis==1 and event.value>0:
                            response=requests.get(url="http://10.0.0.161:5010/forward")
                            print(response)
                        print('AXIS!  VALUE=',event.axis,event.value)
                while event.type == JOYBALLMOTION:
                    self.joy[event.joy].ball[event.ball] = event.rel
                    print('BALL!  VALUE=',event.ball,event.rel)
                while event.type == JOYHATMOTION:
                    self.joy[event.joy].hat[event.hat] = event.value
                    print('HAT!  VALUE=',event.hat,event.value)
                while event.type == JOYBUTTONUP:
                    self.joy[event.joy].button[event.button] = 0
                    print('BUTTONUP!  VALUE=',event.button)
                while event.type == JOYBUTTONDOWN:
                    self.joy[event.joy].button[event.button] = 1
                    print('BUTTONDOWN!  VALUE=',event.button)


    def quit(self, status=0):
        pygame.quit()
        sys.exit(status)

if __name__ == "__main__":
    program = input_test()
    program.init()
    program.run()  # This function should never return