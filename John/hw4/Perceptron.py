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
    
    
    if len(sys.argv) < 3:
        sys.stderr.write("\nUsage:%s REQUIRED: train.txt test.txt OPTIONAL: [Test Function(one of:'last','longest','voted','last50') default: 'last'] [# training iterations, default: 1]\n\n"%(sys.argv[0]))
        sys.exit(1)
    
    train = open(sys.argv[1],'r')
    test = open(sys.argv[2],'r')
    
    perceptron = Perceptron()
    
    #defaults:
    testFunction = perceptron.lastHypothesisClassify
    trainItter = 1
    
    if len(sys.argv) > 3:
        arg = sys.argv[3]
        if arg == 'last':
            testFunction = perceptron.lastHypothesisClassify
        elif arg == 'longest':
            testFunction = perceptron.longestSurvivorClassify
        elif arg == 'voted':
            testFunction = perceptron.votedHypothesisClassify
        elif arg == 'last50':
            testFunction = perceptron.last50VotesClassify
        else:
            sys.stderr.write("\nError: Do not recognize test function: %s, run again with no args for help.\n\n"%arg)
            sys.exit(1)
    if len(sys.argv) > 4:
        trainItter = int(sys.argv[4])

    trainData = []
    testData = []
    
    for line in train:
        #each line should be "x_1    x_2    class"
        #where x_n is a float and class is either +1(or 1) or -1
        #(python can handle unary +)
        line = line.split()
        if line:
            x1 = float(line[0])
            x2 = float(line[1])
            label = int(line[2])
            trainData.append((x1,x2,label))
            
    for line in test:
        line = line.split()
        if line:
            x1 = float(line[0])
            x2 = float(line[1])
            label = int(line[2])
            testData.append((x1,x2,label))
    
    #train the perceptron on the set of data
    for i in range(trainItter):
        if i > 0: #shuffle after first iteration through the data
            random.shuffle(trainData)
        
        for (x1,x2,label) in trainData:
            perceptron.train(x1, x2, label)
    
    #run tests, to standard out write the following
    print("#x1\tx2\tlabel\tpred")
    for (x1,x2,label) in testData:
        print("%.3f\t%.3f\t%d\t%d"%(x1,x2,label,testFunction(x1,x2)))
            
        
        
        
        