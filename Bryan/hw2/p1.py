#!/usr/bin/env python2.6
# Authors: Bryan Matsuo (bmatsuo@soe.ucsc.edu)
#       & John St. John (jstjohn@soe.ucsc.edu)
# Filename: p1.py
# Associated Assignment: CMPS 242 Spring '11 - HW2
# Due: 4/15/2011

# Produces output like the following (long lines/floats are trimmed):
#
# Label space:
#	     ['+', '-']
# Instance space:
#	     ['a', 'b', 'c']
# Hypothesis prior probabilities:
#	     {   'h1': 0.5, 'h2': 0.4000, 'h3': 0.1000}
# Conditional probabilities of '+':
#	     {   'a': {   'h1': 0.8000, 'h2': 0.25, 'h3': 0.5},
#	         'b': {   'h1': 0.8000, 'h2': 0.75, 'h3': 0.5},
#	         'c': {   'h1': 0.2000, 'h2': 0.75, 'h3': 0.5}}
#
# Sample:
#	     [('a', '+'), ('b', '-'), ('c', '+')]
# (a) Prior probability of '+' for each point:
#	     {   'a': 0.5500, 'b': 0.7500, 'c': 0.4500}
# (b) Hypothesis likelihoods:
#	     {   'h1': 0.031999999999999994, 'h2': 0.046875, 'h3': 0.125}
#     Maximum likelihood hypothesis:
#	     'h3'
# (c) Posterior hypothesis probabilities:
#	     {   'h1': 0.33862433862433855,
#	         'h2': 0.39682539682539686,
#	         'h3': 0.26455026455026454}
#     Maximum a posteriori hypothesis:
#	     'h2'
# (d) Mean posterior probabilities of '+':
#	     {   'a': 0.5024, 'b': 0.7008, 'c': 0.4976}
# (e) Larger sample:
#	     [('a', '+'), ('b', '-'), ('c', '+'), ('a', '+'), ('b', '-'), ('c', '+')]
#     Hypothesis likelihoods:
#	     {   'h1': 0.0010, 'h2': 0.0021, 'h3': 0.0156}
#     Maximum likelihood hypothesis:
#	     'h3'
#     Posterior hypothesis probabilities:
#	     {   'h1': 0.1733591,
#	         'h2': 0.2975907,
#	         'h3': 0.5290501}
#     Maximum a posteriori hypothesis:
#	    'h3'
#     Mean posterior probabilities of '+':
#	     {   'a': 0.47761, 'b': 0.62640, 'c': 0.52238}
import string
import pprint

# CONSTANTS
label_space     = ['+','-']
instance_space  = ['a','b','c']
(h1,h2,h3)  = ( 'h1',   'h2',       'h3')
hypotheses  = [ h1,     h2,         h3]
hyp_prior   = { h1:0.5, h2:0.4,     h3:0.1}
cond_prob = {
        'a':{   h1:0.8, h2:0.25,    h3:0.5},
        'b':{   h1:0.8, h2:0.75,    h3:0.5},
        'c':{   h1:0.2, h2:0.75,    h3:0.5}, }

class LabelError(ValueError): pass
class InstanceError(ValueError): pass
class HypothesisError(ValueError): pass

pp = pprint.PrettyPrinter(indent=4)
def labeled_pprint(label, obj):
    'Print labeled structure to stdout.'
    print "%s:\n\t%s" % (
            label,
            string.replace(pp.pformat(obj), "\n", "\n\t"))

def arg_max(d):
    'Return the key of the maximum value in dictionary d.'
    return reduce(lambda k1, k2: k1 if d[k1] > d[k2] else k2, d.keys())

def prior(point):
    'The prior probability of point ("a","b", or "c") being a "+" instance.'
    if not point in instance_space:
        InstanceError("Unknown point %s" % str(point))
    return sum([hyp_prior[h] * cond_prob[point][h] for h in hypotheses])
def prior_hyp():
    'Return a dict mapping instances to their prior probabilities.'
    return dict( [ (point, prior(point)) for point in instance_space ] )

def cond_ex_likelihood(ex, h):
    'The probability of an example (point-label pair) given a hypothesis.'
    (point, c) = ex
    if not point in instance_space:
        InstanceError("Unknown point %s" % str(point))
    if not c in label_space:
        LabelError("Unknown label %s" % str(c))
    if not h in hypotheses:
        HypothesisError("Unknown hypothesis %s" % str(h))
    return cond_prob[point][h] if c == '+' else 1 - cond_prob[point][h]
def sample_likelihood(data, h):
    'The likelihood of a list of examples given a hypothesis.'
    return reduce(
            lambda x,y: x*y,
            [1] + [cond_ex_likelihood(ex, h) for ex in data])
def _sample_likelihood_dict(data):
    return dict( [ (h, sample_likelihood(data, h)) for h in hypotheses ] )
def max_likelihood_hyp(data):
    'The maximum likelihood hypothesis given a list of examples.'
    return arg_max(_sample_likelihood_dict(data))

def _h_posterior(h,data):
    'The unnormalized posterior probability of a hypothesis.'
    if not h in hypotheses:
        HypothesisError("Unknown hypothesis %s" % str(h))
    return hyp_prior[h] * sample_likelihood(data, h)
def h_posterior(h,data):
    'The full posterior probability of hypothesis.'
    norm = float( sum( [ _h_posterior(g, data) for g in hypotheses ] ) )
    return _h_posterior(h,data) / norm
def _hyp_posterior_dist(data):
    'The full Bayes posterior distribution over hypotheses.'
    return dict( [ (h, h_posterior(h,data)) for h in hypotheses ] )
def max_ap_hyp(data):
    'The maximum a posteriori hypothesis given a list of examples.'
    return arg_max(_hyp_posterior_dist(data))

def _mean_posterior(point, data):
    'The mean posterior probability of a point being labeled "+"'
    if not point in instance_space:
        InstanceError("Unknown point %s" % str(point))
    return sum([cond_prob[point][h] * h_posterior(h,data) for h in hypotheses])
def mean_posterior_hyp(data):
    'The mean over hypothesis of posterior probabilities for each instance.'
    means = [(point, _mean_posterior(point, data)) for point in instance_space]
    return dict( means )


labeled_pprint("Label space", label_space)
labeled_pprint("Instance space", instance_space)
labeled_pprint("Hypothesis prior probabilities", hyp_prior)
labeled_pprint("Conditional probabilities of '+'", cond_prob); print

S=[('a','+'), ('b', '-'), ('c', '+')]
labeled_pprint("Sample", S)

labeled_pprint("(a) Prior probability of '+' for each point", prior_hyp())
labeled_pprint("(b) Hypothesis likelihoods", _sample_likelihood_dict(S))
labeled_pprint("    Maximum likelihood hypothesis", max_likelihood_hyp(S))
labeled_pprint("(c) Posterior hypothesis probabilities", _hyp_posterior_dist(S))
labeled_pprint("    Maximum a posteriori hypothesis", max_ap_hyp(S))
labeled_pprint("(d) Mean posterior probabilities of '+'", mean_posterior_hyp(S))

SS = S + S
labeled_pprint("(e) Larger sample", SS)

labeled_pprint("    Hypothesis likelihoods", _sample_likelihood_dict(SS))
labeled_pprint("    Maximum likelihood hypothesis", max_likelihood_hyp(SS))
labeled_pprint("    Posterior hypothesis probabilities", _hyp_posterior_dist(SS))
labeled_pprint("    Maximum a posteriori hypothesis", max_ap_hyp(SS))
labeled_pprint("    Mean posterior probabilities of '+'", mean_posterior_hyp(SS))
