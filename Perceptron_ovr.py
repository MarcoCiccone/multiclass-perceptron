from numpy import *
import scipy as Sci
import scipy.linalg
import matplotlib.pyplot as plt

#i vettori sono di tipo numpy.array per ottimizzare il prodotto scalare
class Perceptron(object):

    def __init__(self, w=None, b=None, R=None ):
        self.R = R
        self.b = b
        self.w = w
        self.wlist = []
        self.blist = []
        self.clist = []

    def calculate_R(self, input_vector) :
        R = 0
        for x in input_vector :
            r = linalg.norm(x)
            if (r > R):
               R = r
        return R

    def train(self, training_set, learning_rate=0.1, limit=100):
        if self.w is None:
            lenX = len(training_set[training_set.keys()[0]][0][0]) # training_set.keys()[0] prendo la prima chiave (da 0 a 9), poi prendo il primo elemento della lista che contiene il vettore x e il valore 1 o -1 a seconda se e un esempio positivo o no per la classe della chiave
            self.w = dict((el,array([0.0 for _ in range(lenX)])) for el in training_set)
            self.b = dict((el,0.0) for el in training_set)
            # ho creato un dizionario per i pesi inizializzati a 0 per ogni classe


        c = 1
        for key,d in training_set.items() :  #per ogni classe
            #for count in range(0,limit): #fino a che non ci sono errori
            updated = True
            iterations = 0
            while(updated):
                iterations += 1
                updated = False
                #print key
                for x,y in d:

                    #self._total(key,x)
                    h = dot(self.w[key], x) - self.b[key]
                    #print h
                    if(h*y <= 0):
                        #self._store(c)
                        self._update_w(key,learning_rate, y, x)
                        self._update_b(key,learning_rate, y, self.R)
                        updated = True
                    else :
                        c = c + 1
                #print
                #print
                #print
                if limit is not None and iterations >= limit:
                    break
            print key, iterations
        #self._store(c)
        return 1

    def testBinary(self, training_set):

        result = dict()
        for key,d in training_set.items() :  #per ogni classe
            result[key] = 0
            for x, y in d:
                d = dot(self.w[key], x) - self.b[key]
                if(d*y <= 0):
                    result[key] += 1
        return result

    def test(self, training_set):

        pos = dict()
        for x, y in training_set:

            h = -99999
            keymax = ''
            for key, w in self.w.items():

                d = dot(w, x) - self.b[key]
                print d, "   ",key
                if d >= h:
                    h = d
                    keymax = key
            print keymax, y
            print
            print
            if keymax == y :
                if keymax in pos:
                    pos[keymax] += 1
                else:
                    pos[keymax] = 1

        return pos

    def _store(self, c):
        self.wlist.append(self.w)
        self.blist.append(self.b)
        self.clist.append(c)

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


if __name__ == '__main__':
    Data = dict()
    file = open("zip.train")

    R = 0
    for line in file:
        #y = map(float, line.split(" "))
        x =line.split(" ")
        y = x.pop(0);   #recupero il valore della carattere. Cifra da 0 a 9
        if x[len(x)-1] == "\n" :
            x.pop(len(x)-1) #si toglie il /n in fondo alla riga

        x = map(float, x) #converto in float i campi stringa
        if y in Data:
            # append the new number to the existing array at this slot
            Data[y].append(x)
        else:
            # create a new array in this slot
            Data[y] = []
            Data[y].append(x)

        r = linalg.norm(x)
        if (r > R):
            R = r


    print "R : ", R
    #-----------------------------------------------------------------------------
    #Decompongo in problemi binari
    #creare un dataset per ogni elemento chiave,
    # valore +1 per quelli che sono la chiave, -1 per tutti gli altri

    Dataset = dict()
    for x, y in Data.items():
        Dataset[x] = []
        for k, v in Data.items():
            for V in v:
                if (k != x) :
                    Dataset[x].append([array(V),-1.0])
                else :
                    Dataset[x].append([array(V),1.0])


    #----------------------------------------------------------------------------



    Data = dict()
    file = open("zip.test")

    R = 0
    for line in file:
        #y = map(float, line.split(" "))
        x =line.split(" ")
        y = x.pop(0);   #recupero il valore della carattere. Cifra da 0 a 9
        y = y + '.0000'
        if x[len(x)-1] == "\n" :
            x.pop(len(x)-1) #si toglie il /n in fondo alla riga

        x = map(float, x) #converto in float i campi stringa
        if y in Data:
            # append the new number to the existing array at this slot
            Data[y].append(x)
        else:
            # create a new array in this slot
            Data[y] = []
            Data[y].append(x)

    #-----------------------------------------------------------------------------
    #Decompongo in problemi binari
    #creare un dataset per ogni elemento chiave,
    # valore +1 per quelli che sono la chiave, -1 per tutti gli altri

    Dataset = dict()
    for x, y in Data.items():
        Dataset[x] = []
        for k, v in Data.items():
            for V in v:
                if (k != x) :
                    Dataset[x].append([array(V),-1.0])
                else :
                    Dataset[x].append([array(V),1.0])


    #----------------------------------------------------------------------------

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


    nn = Perceptron(None,None,R)
    iterations = nn.train(Dataset, 0.2) # learning_rate is the learning rate

    pos = nn.test(DataTest)
    #res = nn.testBinary(DataTest)

    print "RESULT OF TEST: "

    tot = 0
    for key,value in pos.items():
        print key
        percentage = float(value)*100/float(count[key])
        print value, " on " , count[key] , "\t --> ", percentage, "%"
        tot += value


    print tot, " on ", len(DataTest)


    #for key,d in DataTest.items() :  #per ogni classe
     #   print key
      #  print (len(d)-res[key])*100/len(d)
    # print




    #print res[0]*100/len(DataTest)

    #print nn.w


    #print Xdata
    #print Ydata


    #Yset = list(set(Ydata))

    #for yset in Yset


    #print Yset
    #dataset = zip(Xdata,Ydata)
    #print dataset[0]
