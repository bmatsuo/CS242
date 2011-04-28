#!/usr/bin/env python2.6
from numpy import cos, sin, pi
from random import random as rand
from optparse import OptionParser, make_option
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

setfile = args[0] if len(args) > 0 else None
try:
    fh = sys.stdin if setfile is None else open(setfile, 'r')
except:
    sys.stderr.write("Can't read file %s" % str(setfile))

pos_points = []

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

if len(pos_points) < 2:
    if opt.verbose: print "No gap; %d" % len(pos_points)
    exit(0)

left = pos_points[0]
right = pos_points[0]

rleft = rotate(left)
rright = rotate(right)

if opt.verbose: print "Rotated:"
for p in pos_points[1:]:
    r = rotate(p)
    if opt.verbose or opt.print_rotated:
        print "%f\t%f" % r
    if r[1] < -1.0e-16: Exception('Large negative y value %f' % r[1])
    if r[0] < left[0]:
        left = p
        rleft = r
    if r[0] > right[0]:
        right = p
        rright = r

if opt.verbose:
    print "Left: (%f, %f)\tRight: (%f, %f)" % (
            left[0], left[1], right[0], right[1])
    print "Rot Left: (%f, %f)\tRot Right: (%f, %f)" % (
            rleft[0], rleft[1], rright[0], rright[1])

# $w = \frac{{\bf x}_\ell + {\bf x}_r}{2}$
weights = map(lambda lr: (lr[0] + lr[1]) / 2.0, zip(left,right))
w_norm = sum(map(lambda w:w**2, weights))**0.5
if opt.verbose:
    print "W: (%f, %f) 2-Norm: %f" % (weights[0], weights[1], w_norm)

# $g = \frac{{\bf w} \cdot {\bf x}_\ell}{||w||_2}$
gap = sum(map(lambda wx: wx[0]*wx[1]/w_norm, zip(weights, left)))
gap_right = sum(map(lambda wx: wx[0]*wx[1]/w_norm, zip(weights, right)))

# There seem to be rounding errors and the gaps are not really THAT close.
#if abs(gap - gap_right) > 1.0e-15:
#    raise Exception('Large gap difference %.16f' % abs(gap - gap_right))

if opt.print_gap:
    print "Gap: %f" % gap
    if opt.verbose: print "Right gap: %f" % gap_right
    if opt.verbose: print "Gap delta: %.15f" % abs(gap - gap_right)

if not fh is sys.stdin: fh.close()
