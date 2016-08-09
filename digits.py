import dlx
import itertools
import sys

def xy(t, pixel):
  return tuple(sorted((p[0], p[1], t) for p in pixel))
def xz(t, pixel):
  return tuple(sorted((p[0], t, p[1]) for p in pixel))
def yz(t, pixel):
  return tuple(sorted((t, p[0], p[1]) for p in pixel))

def shift(d, pixel):
  return [ [i[0]+d,i[1]] for i in pixel]

def rotateR(pixel):
  return [ [i[1], -i[0]] for i in pixel]

def trans(pixel):
  return [ [i[1], i[0]] for i in pixel]

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

name = sorted(digit.keys())
col  = list(itertools.product((-2,-1,0,1,2), repeat=3))

x  = { k : i for i,k in enumerate(name)}
x.update({ k : i + len(name) for i, k in enumerate(col)})

column  = [(x[k],dlx.DLX.PRIMARY) for k in name]
column += [(x[k],dlx.DLX.SECONDARY) for k in col]

d   = dlx.DLX(column)
row = []

for k, v in digit.items():
  color  = v[0]
  pixel  = [v[1], shift(1,v[1]), shift(2,v[1])]
  pixel += [rotateR(i) for i in pixel[-3:]]
  pixel += [rotateR(i) for i in pixel[-3:]]
  pixel += [rotateR(i) for i in pixel[-3:]]
  pixel += [trans(i) for i in pixel]

  j = set()
  for z in pixel:
    for t in (-2,-1,0,1,2):
      j.add(xy(t,z))
      j.add(xz(t,z))
      j.add(yz(t,z))
  for placement in j:
    row += [ [x[k]] + [x[i] for i in placement]]

d.appendRows(row)
path  = sys.argv[1]
count = 0

for sol in d.solve():
  print(count)
  with open( '{}/solution.{:05d}'.format(path,count), 'w') as io:
    io.write(  '{\n' )
    for i in sol:
      r = d.getRowList(i)
      color = digit[name[r[0]]][0]
      place = [col[i-len(name)] for i in r[1:]]
      io.write( '{} : {},\n'.format(color,place))
    io.write( '}\n')
  count += 1
