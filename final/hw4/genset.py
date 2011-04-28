#!/usr/bin/env python2.6
from numpy import cos, sin, pi
from random import random as rand
from optparse import OptionParser, make_option

two_pi = 2 * pi
def circle_point(x): return (cos(x * two_pi), sin(x * two_pi))
def rand_circle_point(): return circle_point(rand())

def label(x): return 1 if x[0] + x[1] > 0 else -1
def noisy_label(x): return 1 if x[0] + x[1] + 2*rand() - 1 > 0 else -1

options = [
        make_option("--noisy", action="store_true", dest="noisy",
            help="Generate noisy labels for instances."),
        make_option("--num", "-n", type='int', dest='set_size', default=50,
            help="Generate a training/test with SET_SIZE instances.")]
p = OptionParser(
        description="Generate training/test sets for CMPS242 hw3 problem 3",
        option_list=options,)
(opt, args) = p.parse_args()

labeler = noisy_label if opt.noisy else label

for i in range(opt.set_size):
    x = rand_circle_point()
    y = labeler(x)
    print "%f\t%f\t%d" % (x[0], x[1], y)
