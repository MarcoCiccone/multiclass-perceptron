from numpy import *
import scipy as Sci
import scipy.linalg
import matplotlib.pyplot as plt
import operator


#i vettori sono di tipo numpy.array per ottimizzare il prodotto scalare
class Perceptron(object):

    def __init__(self, w=None, b=None):
        self.R = R
        self.b = b
        self.w = w

    def _total(self, key, input_vector):
        total = 0
        for w,x in zip(self.w[key], input_vector):
            total += (w * x)
        return total

    def _update_w(self, key, learning_rate, y, x):
        for i in range(len(self.w[key])):
            self.w[key][i] = self.w[key][i] + (learning_rate * y * x[i])

    def _update_b(self, key, learning_rate, y, R):
        self.b[key] = self.b[key] - (learning_rate * y * R*R)


    def train(self, training_set, R, learning_rate=0.1, limit=100):

        self. R = R
        Keys = training_set.keys()
        perm = []
        for i in range(0,len(Keys)):
            for j in range(i+1,len(Keys)):
                perm.append(Keys[i]+"_"+Keys[j])

        if self.w is None:
            lenX = len(training_set[Keys[0]][0])
            self.w = dict((el,array([0.0 for _ in range(lenX)])) for el in perm)
            self.b = dict((el,0.0) for el in perm)
            # creo un dizionario per i pesi inizializzati a 0 per ogni classe


        #creo k(k-1)/2 perceptron


        for i in range(0,len(Keys)):
            for j in range(i+1,len(Keys)):
                P = training_set[Keys[i]] #positivi
                N = training_set[Keys[j]] #negativi
                key = Keys[i]+"_"+Keys[j]

                for f in range(0,limit):
                    #POSITIVI ---------------------
                    y = 1.0
                    for x in P:
                        h = dot(self.w[key], x) - self.b[key]
                        if(h*y <= 0):
                            self._update_w(key,learning_rate, y, x)
                            self._update_b(key,learning_rate, y, self.R)

                    #NEGATIVI ---------------------
                    y = -1.0
                    for x in N:
                        h = dot(self.w[key], x) - self.b[key]
                        if(h*y <= 0):
                            self._update_w(key,learning_rate, y, x)
                            self._update_b(key,learning_rate, y, self.R)
                print "Trained Perceptron : ", key
        return True

    def test(self, training_set):

        Keys = self.w.keys()
        pos = dict()
        neg = dict()

        rank =  dict()


        for x, y in training_set:
            rank = {}
            for k in Keys:
                k1 = k.split("_")[0]
                k2 = k.split("_")[1]

                h = dot(self.w[k], x) - self.b[k]
                #print k1, " ", k2, " ", h
                if(h <= 0):
                    if k2 in rank:
                        rank[k2] += 1
                    else:
                        rank[k2] = 1
                else:
                    if k1 in rank:
                        rank[k1] += 1
                    else:
                        rank[k1] = 1
            maxkey = max(rank.iteritems(), key=operator.itemgetter(1))[0]
            test = "KO"
            if maxkey == y :
                test = "OK"
                if maxkey in pos:
                    pos[maxkey] += 1
                else:
                    pos[maxkey] = 1

            print "Real Value : ", y, "    Result of Test : ", maxkey, "    --> ", test
            print

        print pos
        return pos




if __name__ == '__main__':
    Data = dict()
    file = open("zip.train")

    R = 0
    for line in file:
        x =line.split(" ")
        y = x.pop(0);   #recupero il valore della carattere. Cifra da 0 a 9
        if x[len(x)-1] == "\n" :
            x.pop(len(x)-1) #si toglie il /n in fondo alla riga

        x = array(map(float, x)) #converto in float i campi stringa
        if y in Data:
            Data[y].append(x)
        else:
            Data[y] = []
            Data[y].append(x)

        r = linalg.norm(x)
        if (r > R):
            R = r


    #carico il file di Test
    DataTest = []
    count = dict()
    file = open("zip.test")
    for line in file:
        #y = map(float, line.split(" "))
        x =line.split(" ")
        y = x.pop(0);   #recupero il valore della carattere. Cifra da 0 a 9
        if x[len(x)-1] == "\n" :
            x.pop(len(x)-1) #si toglie il /n in fondo alla riga
        y = y + '.0000'
        x = map(float, x) #converto in float i campi stringa
        DataTest.append([array(x),y])
        if y in count:
            count[y] += 1
        else:
            count[y] = 1

    #----------------------------------------------------------------------------

    nn = Perceptron()

    iterations = nn.train(Data,R, 0.6)
    pos = nn.test(DataTest)
    print "RESULT OF TEST: "

    tot = 0
    for key,value in pos.items():
        print key
        percentage = float(value)*100/float(count[key])
        print value, " on " , count[key] , "\t --> ", percentage, "%"
        tot += value


    print tot, " on ", len(DataTest)
    percentage = float(tot)*100/float(len(DataTest))
    print "Perceptron has been successful in ", percentage,"%"
