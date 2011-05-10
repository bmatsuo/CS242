#!/usr/bin/env python

# To view the plot immediately run in pylab
#   ipython -pylab binplot.py
# To simply save the plot to 'binplot.eps', run in regular python
#   python2.6 binplot.py

import sys
from numpy import arange
from scipy import comb
import matplotlib.pyplot as pyplot

def bin_pdf(n,p,k): return comb(n,k) * p**k * (1-p)**(n-k)
def bin_cdf(n,p,m): return sum( (bin_pdf(n,p,k) for k in range(m+1)) )
def pr_correct(n,p): 
    if isinstance(n,int): return 1 - bin_cdf(n,p,n//2)
    try:
        return map(lambda m: pr_correct(m,p),n)
    except:
        raise Exception('pr_correct requires integer or a list of integers')

t = arange(1,50)
pyplot.plot(t, pr_correct(t,0.5), 'g.', label='$p = 0.5$')
#pyplot.plot(t, pr_correct(t,0.5), 'g.')

pyplot.plot(t, pr_correct(t,0.6), 'b.', label='$p = 0.6$')
#pyplot.plot(t, pr_correct(t,0.6), 'b.')

pyplot.plot(t, pr_correct(t,0.8), 'r.', label='$p = 0.7$')
#pyplot.plot(t, pr_correct(t,0.8), 'r.')

pyplot.ylabel('Pr(Correct Majority)')
pyplot.xlabel('Number of base learners $T$')

pyplot.legend(loc='best')

# Save the plot if desired.
try:
    filename = sys.argv[1]
    pyplot.savefig(filename)
except Exception as e:
    if isinstance(e,IndexError):
        sys.stderr.write("\nNo filename given, didn't write to file.\n\n")
    else:
        sys.stderr.write("\nCan not write image file '%s'\n\n" % filename)
