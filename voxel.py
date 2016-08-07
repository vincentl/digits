import pyglet
import math
import copy

from pyglet.gl import *
from pyglet.window import key

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import ArcBall


class World(pyglet.window.Window):
  def __init__(self):
    width  = 1280
    height =  960
    
    config = Config(sample_buffers=1, samples=4,
                depth_size=16, double_buffer=True,)
    super(World, self).__init__(width, height, resizable=True, config=config)

    self.z      = 16.0
    self.width  = width
    self.heigth = height
    self.lastR  = ArcBall.Matrix3fT()
    self.thisR  = ArcBall.Matrix3fT()
    self.trans  = ArcBall.Matrix4fT()
    self.setup()
  
  def setup(self):
    self.InitGL(self.width, self.height)
    self.arcball = ArcBall.ArcBallT(self.width, self.height)
    self.lastR = ArcBall.Matrix3fSetIdentity()
    self.thisR = ArcBall.Matrix3fSetIdentity()
    self.trans = ArcBall.Matrix4fSetRotationFromMatrix3f(self.trans, self.thisR)

  def on_draw(self):
    self.DrawGLScene()

  def on_resize(self,w,h):
    self.ReSizeGLScene(w,h)
    self.arcball.setBounds(w,h)
  
  def InitGL(self,Width, Height):
    glClearColor(0.0, 0.0, 0.0, 0,0)
    glClearDepth(1.0)	   
    glDepthFunc(GL_LESS)	   
    glEnable(GL_DEPTH_TEST)	   
    glShadeModel(GL_SMOOTH)	   
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()	   
    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_LINE_SMOOTH)

  def ReSizeGLScene(self,Width, Height):
    if Height == 0:
            Height = 1
    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

  def cubeVertex(self):
    glBegin(GL_QUADS)
    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f( 1.0, 1.0, 1.0)

    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f( 1.0,-1.0,-1.0)

    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)

    glVertex3f( 1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0,-1.0)

    glVertex3f(-1.0, 1.0, 1.0)
    glVertex3f(-1.0, 1.0,-1.0)
    glVertex3f(-1.0,-1.0,-1.0)
    glVertex3f(-1.0,-1.0, 1.0)

    glVertex3f( 1.0, 1.0,-1.0)
    glVertex3f( 1.0, 1.0, 1.0)
    glVertex3f( 1.0,-1.0, 1.0)
    glVertex3f( 1.0,-1.0,-1.0)
    glEnd()

  def placeCube(self,x,y,z):
    glPushMatrix()
    glTranslatef(x,y,z)
    glColor3f(0.5,  0.0,  0.0 );
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    self.cubeVertex()
    glColor3f(1.0, 0, 0)
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    self.cubeVertex()
    glPopMatrix()

  def DrawGLScene(self):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(0,0,self.z,0,0,0,0,1,0)
    glLineWidth( 2.0 + 8.0/max(self.z,0.1))
    glPushMatrix()
    glMultMatrixf(self.trans)
    self.placeCube(0,0,0)
    self.placeCube(3,0,0)
    glPopMatrix()

  def on_key_press(self, symbol, modifiers):
    if symbol == key.ESCAPE:
      self.dispatch_event('on_close')

  def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
    self.z += scroll_y/4.0

  def on_mouse_press(self, x, y, button, modifiers):
    self.lastR = copy.copy(self.thisR)
    pt = ArcBall.Point2fT(x,y)
    self.arcball.click(pt)

  def on_mouse_release(self, x, y, button, modifiers):
    self.lastR = copy.copy(self.thisR)

  def on_mouse_drag(self, x, y, dx, dy, button, modifiers ):
    pt = ArcBall.Point2fT(x,y)
    q  = self.arcball.drag(pt)
    self.thisR = ArcBall.Matrix3fSetRotationFromQuat4f(q)
    self.thisR = ArcBall.Matrix3fMulMatrix3f(self.lastR, self.thisR)
    self.trans = ArcBall.Matrix4fSetRotationFromMatrix3f(self.trans, self.thisR)
    

if __name__ == "__main__":
  window = World()
  pyglet.app.run()

