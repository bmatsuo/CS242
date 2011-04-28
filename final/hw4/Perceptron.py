#!/usr/bin/env python
'''
Created on Apr 26, 2011

@author: John St. John & Bryan Matsuo
'''


class Perceptron:
    """
    Perceptron class
    Feed in ____ get out _____
    
    The weight vectors are stored as
    an array of tuples where each tuple
    is the weight vector at time i
    
    
    """
    def __init__(self, learningRate = 1):
        self.w = [(0,0)] #w_0 initialized as a 0 vector
        self.i = 0
        self.lr = learningRate
        
    def train(self, x1, x2, label):
        """
        Train and update weight vectors, return the
        classification so far since it is an online learning
        method
        """
        (w1,w2) = self.w[self.i]
        lpred = cmp((w1*x1+w2*x2),0) #returns -1 or 1
        if lpred == 0: lpred = -1
        if lpred != label: #need to update weights
            w1 = w1 + (self.lr * label * x1)
            w2 = w2 + (self.lr * label * x2)
        #append our possibly modified weight vectors to the list
        self.w.append((w1,w2))
        self.i += 1
        return lpred
    
    def lastHypothesisClassify(self,x1,x2):
        """
        Simply use the latest weight vector to classify
        a new instance (and freeze training)
        """
        (w1,w2) = self.w[self.i] 
        return cmp((w1*x1+w2*x2),0)
    
    def longestSurvivorClassify(self,x1,x2):
        """
        Identify the longest surviving weight vector,
        use it to train new instances
        """
        
        #identify the longest surviving classifier
        try: #see if we have already done this, and can just classify
            self.longestSurviving
        except NameError: #nope: need to find the longest surviving classifier
            (wp1,wp2) = self.w[0]
        
            #initialize longest weight vector
            wl1 = wp1
            wl2 = wp2
        
            #find a longer one?
            longest = 0
            current = 0
            for (w1,w2) in self.w[1:]:
                if w1 == wp1 and w2 == wp2:
                    current += 1
                    if current > longest:
                        wl1 = w1
                        wl2 = w2
                        longest = current
                else:
                    current = 0
            self.longestSurviving = (wl1,wl2)
        #classify using our longest surviving classifier from training
        (w1,w2) = self.longestSurviving
        return cmp((w1*x1+w2*x2),0)
    
    def votedHypothesisClassify(self, x1, x2):
        """
        return the hypothesis with the most votes in our weight vector
        """
        return ord(sum([ord((w1*x1+w2*x2),0) for (w1,w2) in self.w]),0)
    
    def last50VotesClassify(self, x1, x2):
        """
        Optional method:
        lets just trim the first 450 weights (untrained) and use
        the last 50 to get a majority vote.
        """
        try:
            self.last50
        except NameError:
            self.last50 = self.w[-50:]
        return ord(sum([ord((w1*x1+w2*x2),0) for (w1,w2) in self.last50]),0)


if __name__ == '__main__':
    import sys
    import random
    from optparse import OptionParser, make_option

    options = [
        make_option("--no-shuffle", "-s", action="store_false", default=True, dest="should_shuffle",
            help="Don't shuffle data between successive training loops."),
        make_option("--log", "-L", dest="log_file", default='pa.log',
            help="Log filename (default: 'pa.log')"),
        make_option("--rule", '-r', dest="rule", default='last',
            help="Prediction rule ('last' (default),'longest','voted','last50')."),
        make_option('--consistent', '-c', action='store_true', dest='want_consistent',
            help='Loop over the training set until a consistent weight vector is found'),
        make_option("--iterations", "-T", type='int', dest='iterations', default=1,
            help="Number of training iterations (default: 1).")]
    p = OptionParser(
        description="Train perceptron algorithm and verify against a test set.",
        usage='Perception.py [options] TRAIN TEST',
        option_list=options,)
    (opt, args) = p.parse_args()
    
    if len(args) < 1:
        sys.stderr.write("%s\nUse the -h option for more info." % p.usage)
        sys.exit(1)

    perceptron = Perceptron()

    rule_named = {
            'last':perceptron.lastHypothesisClassify,
            'longest':perceptron.longestSurvivorClassify,
            'voted':perceptron.votedHypothesisClassify,
            'last50':perceptron.last50VotesClassify,}

    if not opt.rule.lower() in rule_named:
        raise Exception("Unrecognized rule %s" % opt.rule)

    testFunction = rule_named[opt.rule.lower()]
    trainItter = opt.iterations

    def _parse_line(line):
        #each line should be "x_1    x_2    class"
        #where x_n is a float and class is either +1(or 1) or -1
        #(python can handle unary +)
        line = line.split()
        if line:
            return (float(line[0]), float(line[1]), int(line[2]))
        return

    trainData = []
    train = open(args[1],'r')
    for line in train:
        example = _parse_line(line)
        if not example is None: trainData.append(example)
    train.close()

    testData = []
    test = open(args[1],'r')
    for line in test:
        example = _parse_line(line)
        if not example is None: testData.append(example)
    test.close()
    
    #train the perceptron on the set of data
    trainLog = open(opt.log_file, 'w')
    trainLog.write("#x1\tx2\tlabel\tpred\n")
    mistakes = 0
    made_mistake = False
    i = 0
    if not opt.want_consistent:
        for i in range(trainItter):
            made_mistake = False
            if opt.should_shuffle and i > 0: #shuffle after first iteration through the data
                random.shuffle(trainData)
            for (x1,x2,label) in trainData:
                pred = perceptron.train(x1, x2, label)
                if label != pred:
                    mistakes += 1
                    made_mistake = True
                trainLog.write("%.3f\t%.3f\t%d\t%d\n" % (x1,x2,label,pred))
            if not made_mistake:
                break
    else:
        while(1):
            made_mistake = False
            if opt.should_shuffle and i > 1: #shuffle after first iteration through the data
                random.shuffle(trainData)
            for (x1,x2,label) in trainData:
                pred = perceptron.train(x1, x2, label)
                if label != pred:
                    mistakes += 1
                    made_mistake = True
                trainLog.write("%.3f\t%.3f\t%d\t%d\n" % (x1,x2,label,pred))
            if not made_mistake:
                break
            i += 1

    print("TRAINING SUMMARY:")
    print("Iterations: %d." % (i + 1))
    print("Total mistakes: %d" % mistakes)
    print("Total predictions: %d" % ((i + 1)*len(trainData)))
    print("Consistent hypothesis: %s" % ('YES' if not made_mistake else 'NO'))
            
    
    #run tests, to standard out write the following
    print("#x1\tx2\tlabel\tpred")
    for (x1,x2,label) in testData:
        print("%.3f\t%.3f\t%d\t%d" % (x1,x2,label,testFunction(x1,x2)))
