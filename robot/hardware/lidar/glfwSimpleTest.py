import glfw
from OpenGL.GL import *

if not glfw.init():
    raise Exception("GLFW could not be initialized")

window = glfw.create_window(640, 480, "Hello World", None, None)
if not window:
    glfw.terminate()
    raise Exception("GLFW window could not be created")

glfw.make_context_current(window)

while not glfw.window_should_close(window):
    glClear(GL_COLOR_BUFFER_BIT)
    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()