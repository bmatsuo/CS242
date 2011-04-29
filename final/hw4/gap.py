#!/usr/bin/env python2.6
from numpy import cos, sin, pi, sqrt
from random import random as rand
from optparse import OptionParser, make_option
from operator import itemgetter
import sys

def rotate(x,theta=pi/4):
    return (cos(theta)* x[0] - sin(theta)*x[1], sin(theta)*x[0] + cos(theta)*x[1])

options = [
        make_option('--points', '-p', action='store_true', dest='print_points',
            help='Print all known positive points (w/ negative points *-1).'),
        make_option('--rotated', '-r', action='store_true', dest='print_rotated',
            help='Print rotated positive points (for debugging).'),
        make_option('--no-gap', '-g', action='store_false', default=True,
            dest='print_gap', help='Do not print the gap of the input set.'),
        make_option('--verbose', '-v', action='store_true', dest='verbose'),]
p = OptionParser(
        description="Compute the maximum gap for a labeled example set for CMPS242 hw3 problem 3",
        option_list=options)
(opt, args) = p.parse_args()

pos_points = []

setfile = args[0] if len(args) > 0 else None
try:
    fh = sys.stdin if setfile is None else open(setfile, 'r')
except:
    sys.stderr.write("Can't read file %s" % str(setfile))
    exit(1)

if opt.verbose: print "Positive:"
for ln in fh.readlines():
    (x1,x2,y) = ln.rstrip().split()
    x1 = float(x1)
    x2 = float(x2)
    y = int(y)
    if y < 0:
        x1 = -x1
        x2 = -x2
    pos_points.append((x1,x2))
    if opt.verbose or opt.print_points:
        print "%f\t%f" % (x1,x2)

if not fh is sys.stdin: fh.close()

if len(pos_points) < 2:
    if opt.verbose: print "No gap; %d" % len(pos_points)
    exit(0)

#grab 4 pairs (with replacement) with minx, maxx, miny, maxy
#if max x >= 0, min y else max y gives bottom
#if max y >= 0, min x, else max x gives top


minx = min(pos_points,key=itemgetter(0))
maxx = max(pos_points,key=itemgetter(0))
miny = min(pos_points,key=itemgetter(1))
maxy = max(pos_points,key=itemgetter(1))


#get point closest to bottom:
if maxx[0] >= 0:
    bottom = miny
else:
    bottom = maxy

#get point closest to top:
if maxy[1] >= 0:
    top = minx
else:
    top = maxx

#now compute distance from bottom to y=-x
#and from top to y=-x
#in this case (after lots of simplification,
#and using the knowlege that we have unit circles
# and are just finding the distance to the y=-x line:
#we get dist = x+y/sqrt(2)
r2 = sqrt(2)
dtop = sum(top)/r2
dbottom = sum(bottom)/r2

#the gap is the mean of the two distances
gap = (dtop+dbottom)/2.0

print("%f"%gap)
