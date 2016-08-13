License
-------

The MIT License (MIT)
Copyright (c) 2016 Vincent Lucarelli

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.



Overview
--------

Code to find solutions to the "Digits in a Box" puzzle by Eric Harshbarger
  http://www.ericharshbarger.org/puzzles/digits_in_a_box/

Use Donald Knuth's Dancing Links algorithm to solve the problem by
finding solutions to an exact cover problem.

Code currently produces "impossible" solutions.  These solutions are valid
configurations of the ten puzzle pieces in a 5x5x5 block, but are impossible to
physically achieve with real puzzle pieces.


Files
-----

  digits.py    -- solver engine that creates exact cover problem
  dlx.c        -- ISO-C11 implementation of Knuth's Dancing Links Algorithm
  ArcBall.py   -- implements 3d rotation used in voxel.py
  voxel.py     -- 3d voxel view used to visualize solutions
  solution.txt -- 128 example solutions
  slice.sh     -- extract a slice of solutions from a solution file


Example
--------
  
  # Get python modules
  $ pip3 install pyglet
  $ pip3 install pyopengl

  # Create exact cover problem
  $ python3 digits.py cover.txt
  
  # Solve exact cover problem (this will take some time)
  $ gcc -O2 -std=gnu11 -o dlx dlx.c
  $ ./dlx cover.txt | tee solutions.txt

  # Count solutions
  $ grep 'zero' solutions.txt | wc
  
  # Solutions 5000 to 6000
  $ ./slice.sh solutions.txt 5000 6000 > slice.txt

  # View solutions start at solution 32
  $ python3 voxel.py --index 32 slice.txt


Voxel Mouse & Keyboard Control
------------------------------

  zoom              : mouse scroll up/down
  expand/contract   : mouse scroll left/right
  rotate            : click-n-drag 
  scroll solutions  : shift + mouse scroll up/down
  next solution     : N
  previous solution : P


Why so many solutions?
----------------------

Eric Harshbarger, the puzzle designer, states

   The instructions on the box read that there are "over 4000
   possible solutions"; there are actually 4239 solutions. That
   is the number of distinct solutions; it does not include
   repetitions due to symmetries or answers in which
   like-shaped pieces are exchanged (the "2" and "5" are
   identical, as are the "6" and "9"). However it does include
   many answers which are almost identical (for example, often
   the "8" piece can simply be swapped with another of the
   pieces -- but these are considered separate configurations).

digits.py uses a fix orientation for "4", which should eliminate the 24
symmetries of the cube.

dlx assumes "2"/"5" and "6"/"9" are distinct, so dlx should produce 4
times as many solutions.

But dlx outputs 226216 solutions!

Some of those solutions are "impossible", but it seems unlikely that
    
    52315 = 226216/4 - 4239

solutions are not feasible.  So there is an open question, "Why so
many solutions?".



--
Vincent Lucarelli
August 2016


