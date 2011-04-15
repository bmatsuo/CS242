#!/usr/bin/env python2.6
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
    print "%s:\n\t%s" % (label, string.replace(pp.pformat(obj), "\n", "\n\t"))

def arg_max(d):
    'Return the key of the maximum value in dictionary d.'
    return reduce(lambda k1, k2: k1 if d[k1] > d[k2] else k2, d.keys())

def prior(point):
    'The prior probability of point ("a","b", or "c") being a "+" instance.'
    if not point in instance_space: InstanceError("Unknown point %s" % str(point))
    return sum([hyp_prior[h] * cond_prob[point][h] for h in hypotheses])
def prior_hyp():
    'Return a dict mapping instances to their prior probabilities.'
    return dict( [ (point, prior(point)) for point in instance_space ] )

def cond_ex_likelihood(ex, h):
    'The probability of an example (point-label pair) given a hypothesis.'
    (point, c) = ex
    if not point in instance_space: InstanceError("Unknown point %s" % str(point))
    if not c in label_space: LabelError("Unknown label %s" % str(c))
    if not h in hypotheses: HypothesisError("Unknown hypothesis %s" % str(h))
    return cond_prob[point][h] if c == '+' else 1 - cond_prob[point][h]
def sample_likelihood(data, h):
    'The likelihood of a list of examples given a hypothesis.'
    return reduce(lambda x,y: x*y, [1] + [cond_ex_likelihood(ex, h) for ex in data])
def _sample_likelihood_dict(data):
    return dict( [ (h, sample_likelihood(data, h)) for h in hypotheses ] )
def max_likelihood_hyp(data):
    'The maximum likelihood hypothesis given a list of examples.'
    return arg_max(_sample_likelihood_dict(data))

def _h_posterior(h,data):
    'The unnormalized posterior probability of a hypothesis given a list of examples.'
    if not h in hypotheses: HypothesisError("Unknown hypothesis %s" % str(h))
    return hyp_prior[h] * sample_likelihood(data, h)
def h_posterior(h,data):
    'Calculate the full posterior probability of hypothesis given a list of examples.'
    norm = float( sum( [ _h_posterior(g, data) for g in hypotheses ] ) )
    return _h_posterior(h,data) / norm
def _hyp_posterior_dist(data):
    'The full Bayes posterior distribution over hypotheses given a list of examples.'
    return dict( [ (h, h_posterior(h,data)) for h in hypotheses ] )
def max_ap_hyp(data):
    'The maximum a posteriori hypothesis given a list of examples.'
    return arg_max(_hyp_posterior_dist(data))

def _mean_posterior(point, data):
    'The mean posterior probability of a point being labeled "+"'
    if not point in instance_space: InstanceError("Unknown point %s" % str(point))
    return sum([cond_prob[point][h] * h_posterior(h,data) for h in hypotheses])
def mean_posterior_hyp(data):
    'The mean over hypothesis of posterior probabilities for each instance.'
    means = [ (point, _mean_posterior(point, data)) for point in instance_space ]
    return dict( means )


labeled_pprint("Label space", label_space)
labeled_pprint("Instance space", instance_space)
labeled_pprint("Hypothesis prior probabilities", hyp_prior)
labeled_pprint("Conditional probabilities of '+'", cond_prob); print

examples=[('a','+'), ('b', '-'), ('c', '+')]
labeled_pprint("Sample", examples)

labeled_pprint("(a) Prior probability of '+' for each point", prior_hyp())
labeled_pprint("(b) Hypothesis likelihoods", _sample_likelihood_dict(examples))
labeled_pprint("    Maximum likelihood hypothesis", max_likelihood_hyp(examples))
labeled_pprint("(c) Posterior hypothesis probabilities", _hyp_posterior_dist(examples))
labeled_pprint("    Maximum a posteriori hypothesis", max_ap_hyp(examples))
labeled_pprint("(d) Mean posterior probabilities of '+'", mean_posterior_hyp(examples))

double_examples = examples + examples
labeled_pprint("(e) Larger sample", double_examples)

labeled_pprint("    Hypothesis likelihoods", _sample_likelihood_dict(double_examples))
labeled_pprint("    Maximum likelihood hypothesis", max_likelihood_hyp(double_examples))
labeled_pprint("    Posterior hypothesis probabilities", _hyp_posterior_dist(double_examples))
labeled_pprint("    Maximum a posteriori hypothesis", max_ap_hyp(double_examples))
labeled_pprint("    Mean posterior probabilities of '+'", mean_posterior_hyp(double_examples))
