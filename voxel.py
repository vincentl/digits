# The MIT License (MIT)
# Copyright (c) 2016 Vincent Lucarelli
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# This code was heavily inspired by NeHe tutorials in 
# https://pypi.python.org/packages/source/P/PyOpenGL-Demo/PyOpenGL-Demo-3.0.1b1.tar.gz
 
import argparse
import ast
import copy
import itertools
import math
import pyglet
import sys

from pyglet.gl import *
from pyglet.window import key

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import ArcBall

class World(pyglet.window.Window):
  def __init__(self, cubes, index, kind):
    width  = 1280
    height =  960
    
    config = Config(sample_buffers=1, samples=4,
                depth_size=16, double_buffer=True,)
    super(World, self).__init__(width, height, resizable=True, config=config)

    self.cubes  = cubes
    self.index  = index % len(cubes)
    self.kind   = kind
    self.shift  = False
    self.e      = 1.0
    self.z      = 16.0
    self.width  = width
    self.heigth = height
    self.lastR  = ArcBall.Matrix3fT()
    self.thisR  = ArcBall.Matrix3fT()
    self.trans  = ArcBall.Matrix4fT()
    self.setup()
    self.set_caption('{} {}'.format(self.kind, self.index))
  
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
    glClearColor(0.125, 0.125, 0.125, 0,0)
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
    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f( 0.5, 0.5, 0.5)

    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f( 0.5,-0.5,-0.5)

    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)

    glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5)

    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5,-0.5)
    glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5,-0.5, 0.5)

    glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5, 0.5)
    glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5)
    glEnd()

  def scaleS(self,x,y,z):
    r = math.sqrt(x**2 + y**2 + z**2)
    t = math.acos(z/r) if r else 0
    p = math.atan2(y,x)
    r = r * (self.e**r)

    return (r * math.sin(t) * math.cos(p), r * math.sin(t) * math.sin(p), r * math.cos(t) )

  def scaleC(self,x,y,z):
    return (i * self.e for i in (x,y,z))

  def placeCube(self,c,x,y,z):
    glPushMatrix()
    glTranslatef(x,y,z)
    glColor3f(*(min(1.0,0.875 * i) for i in c))
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    self.cubeVertex()
    glColor3f(*c);
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
    for k,v in self.cubes[self.index].items():
      color = [i/255.0 for i in k]
      for c in v:
        self.placeCube(color, *self.scaleC(*c))
    glPopMatrix()

  def on_key_press(self, symbol, modifiers):
    if symbol == key.ESCAPE:
      self.dispatch_event('on_close')
    elif symbol == key.N:
      self.index = (self.index + 1) % len(self.cubes)
    elif symbol == key.P:
      self.index = (self.index - 1) % len(self.cubes)
    elif symbol in (key.RSHIFT, key.LSHIFT):
      self.shift = True
    self.set_caption('{} {}'.format(self.kind, self.index))

  def on_key_release(self, symbol, modifiers):
    if symbol in (key.RSHIFT, key.LSHIFT):
      self.shift = False
    self.set_caption('{} {}'.format(self.kind, self.index))

  def on_mouse_scroll(self, x, y, scroll_x, scroll_y):
    if self.shift:
      self.index = (self.index - scroll_y) % len(self.cubes)
      self.set_caption('{} {}'.format(self.kind, self.index))
    else:
      self.z += scroll_y/4.0
      self.e = max(1.0, self.e + scroll_x/64.0)

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
    

def to3d(sigma, pixel):
  f = {k:v for k,v in enumerate(sigma)}
  return [[p[f[i]] if f[i] < 2 else 0 for i in range(3)] for p in pixel]

digit = {
  'zero' : ((252,150,167), [[-2,-2],[-2,-1],[-2,0],[-2,1],[-2,2],[-1,-2],[-1,2],[0,-2],[0,-1],[0,0],[0,1],[0,2]]),
  'one'  : ((  1,120, 80), [[-2,-2],[-1,-2],[0,-2],[-1,-1],[-1,0],[-1,1],[-1,2],[-2,2]]),
  'two'  : ((178,  0,111), [[-2,2],[-1,2],[0,2],[0,1],[0,0],[-1,0],[-2,0],[-2,-1],[-2,-2],[-1,-2],[0,-2]]),
  'three': ((  1, 45,169), [[-2,2],[-1,2],[0,2],[0,1],[-2,0],[-1,0],[0,0],[0,-1],[-2,-2],[-1,-2],[0,-2]]),
  'four' : ((  2,148,201), [[-2,2],[0,2],[-2,1],[0,1],[-2,0],[-1,0],[0,0],[0,-1],[0,-2]]),
  'five' : ((255,210, 69), [[-2,2],[-1,2],[0,2],[-2,1],[-2,0],[-1,0],[0,0],[0,-1],[-2,-2],[-1,-2],[0,-2]]),
  'six'  : ((255,130, 19), [[-2,2],[-1,2],[0,2],[-2,1],[-2,0],[-1,0],[0,0],[-2,-1],[0,-1],[-2,-2],[-1,-2],[0,-2]]),
  'seven': ((  7,  8, 11), [[-2,2],[-1,2],[0,2],[-2,1],[0,1],[0,0],[0,-1],[0,-2]]),
  'eight': ((149, 80,177), [[-2,2],[-1,2],[0,2],[-2,1],[0,1],[-2,0],[-1,0],[0,0],[-2,-1],[0,-1],[-2,-2],[-1,-2],[0,-2]]),
  'nine' : ((213, 20, 40), [[-2,2],[-1,2],[0,2],[-2,1],[0,1],[-2,0],[-1,0],[0,0],[0,-1],[-2,-2],[-1,-2],[0,-2]])
}

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Voxel Viewer')
  parser.add_argument('--index', type=int, help='initial solution to view', default=0)
  parser.add_argument('path', metavar='solutions', type=str, nargs='?', help='path to solutions file')
  option = parser.parse_args()

  if option.path:
    with open(option.path) as io:
      cubes = ast.literal_eval(io.read())
      cubes = [ {k if type(k) is tuple else digit[k][0] : v for k,v in cube.items()} for cube in cubes ]
  else:
    name  = [ 'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine' ]
    cubes = [ {digit[n][0] : to3d([0,1,2],digit[n][1])} for n in name ]

  kind = 'solutions' if option.path else 'digits' 
  print("Loaded {} {}".format(len(cubes), kind))

  window = World(cubes, option.index, kind)
  pyglet.app.run()

