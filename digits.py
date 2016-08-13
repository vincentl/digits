import itertools
import sys

if len(sys.argv) != 2:
  print( '{} cover.txt'.format(sys.argv[0]) )
  sys.exit(1)

# Maps from 2d -> 3d with 1 fixed coordinate
# Returns voxels in canonical order to allow for deduplication
def xy(t, pixel):
  return tuple(sorted((p[0], p[1], t) for p in pixel))
def xz(t, pixel):
  return tuple(sorted((p[0], t, p[1]) for p in pixel))
def yz(t, pixel):
  return tuple(sorted((t, p[0], p[1]) for p in pixel))

# 2d map to right d pixels right
def shift(d, pixel):
  return [ [i[0]+d,i[1]] for i in pixel]

# 2d map that rotates 5x5 array 90 degrees to the right
def rotateR(pixel):
  return [ [i[1], -i[0]] for i in pixel]

# 2d map that flips 5x5 array across main diagonal
def trans(pixel):
  return [ [i[1], i[0]] for i in pixel]

# Name, color, base pixels for each digit
digits = {
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

# Fix an order for digits and 125 voxels
name  = [ 'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine' ]
voxel = list(itertools.product((-2,-1,0,1,2), repeat=3))

# x maps {digit name, voxel} -> [0,10+125)
x  = { k : i for i,k in enumerate(name)}
x.update({ k : i + len(name) for i, k in enumerate(voxel)})

# All columns
column = name + voxel 

# Create matrix of constraints
matrix = []
for digit in name:                                                     # for each digit
  shape  = digits[digit][1]                                            # look up its shape as a list of 2d pixels 
  pixel  = [shape, shift(1,shape), shift(2,shape)]                     # add 2 valid shifts to the right
  pixel += [rotateR(i) for i in pixel[-3:]] if digit != 'four' else [] # except for 'four', consider all rotations and flips
  pixel += [rotateR(i) for i in pixel[-3:]] if digit != 'four' else [] # we use 'four' to eliminate the 24 symmetries of the cube by
  pixel += [rotateR(i) for i in pixel[-3:]] if digit != 'four' else [] # requiring the 'four' to be upright, correctly oriented 
  pixel += [trans(i) for i in pixel]        if digit != 'four' else [] # in one of the 5 xy planes

  unique = set()                                                       # many rotations/flips of a digit are equivalent
  for z in pixel:                                                      # go through the list of all posibilities
    for t in (-2,-1,0,1,2):                                            # for each of the 5 planes the digit can occupy
      unique.add(xy(t,z))                                              # add a canocical list of voxels to the set
      if digit != 'four':
        unique.add(xz(t,z)) 
        unique.add(yz(t,z))
  for placement in sorted(unique):                                     # write each unique digit placement into the constraint matrix
    matrix += [ [x[digit]] + [x[i] for i in placement]]

  print( 'Digit {} has {} placements'.format(digit, len(unique)) )

with open(sys.argv[1], 'w') as io:
  io.write( 'column:\n' )
  for i in name:
    io.write( '+ {}\n'.format(i) )
  for i in voxel:
    io.write( '- {}\n'.format(i) )

  io.write( 'matrix:\n' )
  for i in matrix:
    io.write( '- {}\n'.format(i) )

print( 'Wrote a {} x {} constraint matrix'.format(len(matrix),len(x)) )


