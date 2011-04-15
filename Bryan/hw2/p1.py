#!/usr/bin/env python2.6
import string
import pprint
pp = pprint.PrettyPrinter(indent=4)

def labeled_pprint(label, obj):
    '''
    Print labeled structure to stdout.
    '''
    print "%s:" % label
    print "\t" + string.replace(pp.pformat(obj), "\n", "\n\t")

label_space = ['+','-']
instance_space = ['a','b','c']
labeled_pprint("Instance space", instance_space)

print

hyp_prior = {'h1':0.5, 'h2':0.4, 'h3':0.1}
labeled_pprint("Hypothesis prior probabilities", hyp_prior)

print

cond_prob = {
        'a':{'h1':0.8, 'h2':0.25, 'h3':0.5},
        'b':{'h1':0.8, 'h2':0.75, 'h3':0.5},
        'c':{'h1':0.2, 'h2':0.75, 'h3':0.5},
        }
labeled_pprint("Conditional probabilities of '+'", cond_prob)

print

examples=[('a','+'), ('b', '-'), ('c', '+')]
labeled_pprint("Sample", examples)

def plus_prior(point):
    '''
    Compute the prior probability of a point ('a','b', or 'c').
    '''
    if not point in instance_space: return 0
    joint_probs = [hyp_prior[h] * cond_prob[point][h] for h in cond_prob[point].keys()]
    #labeled_pprint("Debug: Prior plus of " + point, joint_probs)
    return sum(joint_probs)

labeled_pprint(
        "(a) Prior probability of '+' for each point",
        [plus_prior(point) for point in instance_space])

print

def cond_example_likelihood(ex, h):
    '''
    Compute the probability of an example (pair of point and label) given a hypothesis.
    '''
    (point, c) = ex
    if not point in instance_space: return 0
    if not c in label_space: return 0
    if c == '+': return cond_prob[point][h]
    return 1 - cond_prob[point][h]


def sample_likelihood(data, h):
    '''
    Calculate the likelihood of a list of examples given a hypothesis.
    '''
    pr = 1
    for ex in data: pr *= cond_example_likelihood(ex, h)
    return pr

ML_hyp=None
hyp_likelihood = dict([(h, sample_likelihood(examples, h)) for h in hyp_prior.keys()])
normalizer = sum(hyp_likelihood.values())
for h in hyp_likelihood.keys():
    hyp_likelihood[h] /= normalizer
    if ML_hyp is None:
        ML_hyp = h
    elif hyp_likelihood[ML_hyp] < hyp_likelihood[h]:
        ML_hyp = h
    else:
        pass

labeled_pprint("(b) Hypothesis likelihoods", hyp_likelihood)
labeled_pprint("    Maximum likelihood hypothesis", ML_hyp)

def _sample_posterior(data, h):
    '''
    Calculate the posterior probability of a list of examples given a hypothesis.
    '''
    return hyp_prior[h] * sample_likelihood(data, h)
def sample_posterior(data, h):
    '''
    Calculate the posterior probability of a list of examples given a hypothesis.
    '''
    return _sample_posterior(data,h) / float(sum([_sample_posterior(data,h1) for h1 in hyp_prior.keys()]))

hyp_posterior = dict( [(h, sample_posterior(examples, h)) for h in hyp_prior.keys()] )
#normalizer = float(sum(hyp_posterior.values()))
#for h in hyp_posterior:
#    hyp_posterior[h] /= normalizer

labeled_pprint("(c) Posterior hypothesis probabilities", hyp_posterior)
MAP_hyp=None
for h in hyp_posterior.keys():
    if MAP_hyp is None:
        MAP_hyp = h
    elif hyp_posterior[MAP_hyp] < hyp_posterior[h]:
        MAP_hyp = h
    else:
        pass
labeled_pprint("    Maximum a posteriori hypothesis", MAP_hyp)

mean_posterior = dict([
        (point, sum([cond_prob[point][h] * hyp_posterior[h] for h in hyp_posterior.keys()]))
        for point in instance_space])
labeled_pprint("(d) Mean posterior probabilities of '+'", mean_posterior)

double_examples = examples + examples

ML_hyp=None
hyp_likelihood = dict([(h, sample_likelihood(double_examples, h)) for h in hyp_prior.keys()])
normalizer = sum(hyp_likelihood.values())
for h in hyp_likelihood.keys():
    hyp_likelihood[h] /= normalizer
    if ML_hyp is None:
        ML_hyp = h
    elif hyp_likelihood[ML_hyp] < hyp_likelihood[h]:
        ML_hyp = h
    else:
        pass
labeled_pprint("(e) Hypothesis likelihoods", hyp_likelihood)
labeled_pprint("    Maximum likelihood hypothesis", ML_hyp)
hyp_posterior = dict( [(h, sample_posterior(double_examples, h)) for h in hyp_prior.keys()] )
labeled_pprint("    Posterior hypothesis probabilities", hyp_posterior)
MAP_hyp=None
for h in hyp_posterior.keys():
    if MAP_hyp is None:
        MAP_hyp = h
    elif hyp_posterior[MAP_hyp] < hyp_posterior[h]:
        MAP_hyp = h
    else:
        pass
labeled_pprint("    Maximum a posteriori hypothesis", MAP_hyp)
mean_posterior = dict([
        (point, sum([cond_prob[point][h] * hyp_posterior[h] for h in hyp_posterior.keys()]))
        for point in instance_space])
labeled_pprint("    Mean posterior probabilities of '+'", mean_posterior)
