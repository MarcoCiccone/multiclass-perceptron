from numpy import *
import scipy as Sci
import scipy.linalg
import matplotlib.pyplot as plt
import sys


class Perceptron(object):

    def __init__(self, w=None, b=0):
        self.b = b
        self.w = w
        self.wlist = []
        self.blist = []
        self.clist = []

    def calculate_R(self, input_vector) :
        R = 0
        for x,y in input_vector :
            r = linalg.norm(x)
            if (r > R):
               R = r
        return R

    def train(self, training_set, learning_rate=0.1, limit=100):
        if self.w is None:
            self.w = [0 for _ in range(len(training_set[0][0]))]
        c = 1
        R = self.calculate_R(training_set)
        for count in range(0,limit):
            for x, y in training_set:
                d = dot(self.w, x) - self.b
                if(d*y <= 0):
                    self._store(c)
                    self._update_w(learning_rate, y, x)
                    self._update_b(learning_rate, y, R)
                    c = 1
                else :
                    c = c + 1
        self._store(c)
        return self.wlist,self.blist,self.clist

    def test(self, training_set):
        for x, y in training_set:
            d = 0
            t = 0
            for j in range(0,len(self.wlist)):
                t = dot(self.wlist[j], x) - self.blist[j]
                if t>=0:
                    t = 1.0
                else:
                    t = -1.0
                d += self.clist[j] * t

            if(d*y <= 0):
                return False
        return True

    def _store(self, c):
        self.wlist.append(self.w)
        self.blist.append(self.b)
        self.clist.append(c)

    def _total(self, input_vector):
        return dot(self.w, input_vector)

    def _update_w(self, learning_rate, y, x):
        for i in range(len(self.w)):
            self.w[i] = self.w[i] + (learning_rate * y * x[i])

    def _update_b(self, learning_rate, y, R):
        self.b = self.b - (learning_rate * y * R*R)



def generateData(n):
    xb = (random.rand(n)*2-1)/2-0.5
    yb = (random.rand(n)*2-1)/2+0.5
    xr = (random.rand(n)*2-1)/2+0.5
    yr = (random.rand(n)*2-1)/2-0.5

    inputs = []

    for i in range(len(xb)):
        inputs.append([[xb[i],yb[i]],1])
        inputs.append([[xr[i],yr[i]],-1])
    return inputs


if __name__ == '__main__':
    if len(sys.argv)>2 :
        print "too much arguments"
        exit()
    elif len(sys.argv) == 2:
        if sys.argv[1] == "AND" :
            training_set = []
            training_set.append([[0,0],-1])
            training_set.append([[0,1],-1])
            training_set.append([[1,0],-1])
            training_set.append([[1,1],1])
            test_set = training_set
        elif sys.argv[1] == "NAND" :

            training_set = []
            training_set.append([[0,0],1])
            training_set.append([[0,1],1])
            training_set.append([[1,0],1])
            training_set.append([[1,1],-1])
            test_set = training_set
        elif sys.argv[1] == "OR" :
            training_set = []
            training_set.append([[0,0],-1])
            training_set.append([[0,1],1])
            training_set.append([[1,0],1])
            training_set.append([[1,1],1])
            test_set = training_set
        elif sys.argv[1] == "NOR" :
            training_set = []
            training_set.append([[0,0],1])
            training_set.append([[0,1],-1])
            training_set.append([[1,0],-1])
            training_set.append([[1,1],-1])
            test_set = training_set
        elif sys.argv[1] == "XOR" :
            training_set = []
            training_set.append([[0,0],1])
            training_set.append([[0,1],-1])
            training_set.append([[1,0],-1])
            training_set.append([[1,1],1])
            test_set = training_set
        else :
            training_set = generateData(100)
            test_set = generateData(50)
    else :
            training_set = generateData(100)
            test_set = generateData(50)

    nn = Perceptron()
    iterations = nn.train(training_set, 1.0) # learning_rate is the learning rate


    maxc = nn.clist.index(max(nn.clist))
    testresult = nn.test(test_set)
    print "Correct?", testresult

    if testresult == False:
        exit()

    for j in range(0,len(nn.wlist)):
        print "W : ", nn.wlist[j]
        print "b : ", nn.blist[j]
        print "c : ", nn.clist[j]
        print



    w1 = nn.wlist[maxc][0]
    w2 = nn.wlist[maxc][1]
    b = nn.blist[maxc]


    def f(t,w1,w2,b):
        return (-w1*t + b)/(w2)

    t1 = arange(-1.0, 5.0, 0.1)

    for x, y in test_set:
        if (y > 0) :
            plt.plot (x[0],x[1],"ro")
        else :
            plt.plot (x[0],x[1],"bs")

    plt.plot(t1, f(t1,w1,w2,b))


    plt.show()
