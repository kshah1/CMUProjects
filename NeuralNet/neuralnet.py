import numpy as np
import sys
import math

#read data in
def readData(file):
    with open(file, 'r') as f:
        data = f.readlines()

    examples = []
    for line in data:
        splitLine = line.strip().split(',')
        splitLine = list(map(lambda x: int(x), splitLine))
        examples.append(splitLine)
    examples = np.array(examples)
    return examples


#creates one hot vector 
def oneHotVector(value):
    vector = np.zeros(10)
    vector[value] = 1
    vector.reshape(len(vector), 1)
    return vector
    
#applies sigmoid fn
def sigmoid(a):
    x = a.copy()
    denominator = 1 + math.exp(-1 * x)
    result = 1/denominator
    return result

#alpha dot product x results in a
def linearForward(x, alpha):
    xV = x.copy()
    alphaMat = alpha.copy()
    a = np.dot(alphaMat,xV)
    a = a.reshape((len(a), 1))
    return a

#sigmoid of a results in z
def sigmoidForward(firstLayerVector):
    a = firstLayerVector.copy()
    z = np.apply_along_axis(sigmoid, 1, a)
    z = np.insert(z, 0, 1)
    z = z.reshape((len(z)), 1)
    return z

#softmax of b results in yhat
def softMaxForward(secondLayerVector):
    b = secondLayerVector.copy()
    denominator = sum(np.apply_along_axis(math.exp, 1, b))
    numerator = np.apply_along_axis(math.exp, 1, b)
    yHatVector = numerator/denominator
    yHatVector = yHatVector.reshape((len(yHatVector), 1))
    return yHatVector

#objective function resulting in J
def crossEntropyForward(yHat, yStar):
    y_hat = yHat.copy()
    y_star = yStar.copy()
    result = -1 * np.sum(y_star * np.log(y_hat))
    return result

#feed forward process
def NNForward(x,y,alpha,beta):
    xV = x.copy()
    yV = y.copy()
    alphaMat = alpha.copy()
    betaMat = beta.copy()
    a = linearForward(xV, alphaMat) 
    z = sigmoidForward(a)
    b = linearForward(z, betaMat)
    y_hat = softMaxForward(b)
    J = crossEntropyForward(y_hat, y)
    return xV, a, z, b, y_hat, J 

#gradient of J with respect to y
def crossEntropyBackward(yV, yHatV, J, gj):
    y = yV.copy()
    yHat = yHatV.copy()
    gyHat = yHat - y
    return gyHat

#gradient of J with respect to vector b
def softMaxBackward(bV, yHatV, gyHat):
    gb = gyHat
    return gb

#gradient of J with respect to Matrix B and vector z
def linearFirstBackward(zV, bV, gb, betaM):
    z = zV.copy()
    b = bV.copy()
    beta = betaM.copy()
    gB = np.dot(gb, np.transpose(z))
    gz = np.transpose(np.dot(np.transpose(gb), beta[:, 1:]))
    return gB, gz

#gradient of J with respect to vector a (elemental approach)
def sigmoidBackward(aV, zV, gz):
    ga = gz * zV[1:,:] * (1-zV[1:,:])
    return ga

#gradient of J with respect to Matrix alpha
def linearSecondBackward(xV, aV, ga):
    x = xV.copy()
    a = aV.copy()
    galpha = np.dot(ga, np.transpose(x))
    return galpha

#backpropagation
def NNBackward(xVector, yVector, alphaMat, betaMat, aVector, zVector, bVector, yHatVector, J):
    gj = 1
    gyHat = crossEntropyBackward(yVector, yHatVector, J, gj)
    gb = softMaxBackward(bVector, yHatVector, gyHat)
    gBeta, gz = linearFirstBackward(zVector, bVector, gb, betaMat)
    ga =  sigmoidBackward(aVector, zVector, gz)
    galpha = linearSecondBackward(xVector,aVector,ga)
    return galpha, gBeta

#predict technique for neural networks using train data and test data
def predict(trainData, testData, trainLabelsFile, testLabelsFile, alpha, beta):
    with open(trainLabelsFile, 'w') as wTrain: 
        trainCount = 0
        for ex in trainData:
            y, xV = ex[0], ex[1:]
            yoneHot = oneHotVector(y)
            xV = np.insert(xV, 0, 1)
            xV = xV.reshape((len(xV), 1))
            yoneHot = yoneHot.reshape((len(yoneHot), 1))
            xV, a, z, b, yHat, j = NNForward(xV, yoneHot, alpha, beta)
            labels = np.argmax(yHat)
            if labels != y:
                trainCount +=  1 
            wTrain.write(str(labels) + '\n')
        trainError = trainCount/len(trainData)

    with open(testLabelsFile, 'w') as wTest: 
        testCount = 0
        for ex in testData:
            y, xV = ex[0], ex[1:]
            yoneHot = oneHotVector(y)
            xV = np.insert(xV, 0, 1)
            xV = xV.reshape((len(xV), 1))
            yoneHot = yoneHot.reshape((len(yoneHot), 1))
            xV, a, z, b, yHat, j = NNForward(xV, yoneHot, alpha, beta)
            labels = np.argmax(yHat)
            if labels != y:
                testCount += 1
            wTest.write(str(labels) + '\n')
        testError = testCount/len(testData)
    
    return trainError, testError

if __name__ == "__main__":
    trainFile = sys.argv[1]
    testFile = sys.argv[2]
    trainLabelsFile = sys.argv[3]
    testLabelsFile = sys.argv[4]
    metricsFile = sys.argv[5]
    numEpochs = int(sys.argv[6]) #number of epochs to pass 
    hiddenUnits = int(sys.argv[7]) 
    initFlag = int(sys.argv[8]) #initialization with 0's or initilization using uniform distribution
    stepSize = float(sys.argv[9]) #step size for stochastic gradient descent

    exs = readData(trainFile)
    testexs = readData(testFile)
    if initFlag == 1: #uniform distribution initilization
        alpha = np.random.uniform(-0.1,0.1,(hiddenUnits,128))
        alpha = np.hstack((np.array([0] * len(alpha)).reshape(len(alpha),1), alpha))
        beta = np.random.uniform(-0.1,0.1, (10,hiddenUnits))
        beta = np.hstack((np.array([0] * len(beta)).reshape(len(beta),1), beta))
    else: #zeroes initilization
        alpha = np.zeros((hiddenUnits,129)) #initialize w/ zeros (can also be random)
        beta = np.zeros((10, hiddenUnits+1)) 

    with open(metricsFile, 'w') as wMetrics:
        idx = 1
        #loop through number of epochs
        for epochs in range(numEpochs):
            traintotal = 0
            testtotal = 0
            #loop through training examples
            for ex in exs:
                y, xV = ex[0], ex[1:]
                y = oneHotVector(y)
                xV = np.insert(xV, 0, 1)
                xV = xV.reshape((len(xV), 1))
                y = y.reshape((len(y), 1))
                xV, a, z, b, yHat, j = NNForward(xV, y, alpha, beta) #calculate values for feed forward
                galpha, gBeta = NNBackward(xV, y, alpha, beta, a, z, b, yHat, j) #apply back propagation 
                alpha = alpha - (stepSize * galpha) #use stochastic gradient descent to update alpha matrix per training example
                beta = beta - (stepSize * gBeta) #use stochastic gradient descent to update beta matrix per training example
            for ex in exs:
                y, xV = ex[0], ex[1:]
                y = oneHotVector(y)
                xV = np.insert(xV, 0, 1)
                xV = xV.reshape((len(xV), 1))
                y = y.reshape((len(y), 1))
                xV, a, z, b, yHat, j = NNForward(xV, y, alpha, beta)
                traintotal += crossEntropyForward(yHat, y) 
            meanTrainCrossEntropy = traintotal/len(exs) #calculate mean train cross entropy once alpha and beta are updated for all training examples
            print("trainCrossE:", meanTrainCrossEntropy) 
            wMetrics.write("epoch={} crossentropy(train): {}\n".format(idx, meanTrainCrossEntropy))
            for ex in testexs:
                y, xV = ex[0], ex[1:]
                y = oneHotVector(y)
                xV = np.insert(xV, 0, 1)
                xV = xV.reshape((len(xV), 1))
                y = y.reshape((len(y), 1))
                xV, a, z, b, yHat, j = NNForward(xV, y, alpha, beta)
                testtotal += crossEntropyForward(yHat, y)
            meanTestCrossEntropy = testtotal/len(testexs) #calculate mean train cross entropy once alpha and beta are updated for all training examples
            print("testCrossE:", meanTestCrossEntropy)
            wMetrics.write("epoch={} crossentropy(test): {}\n".format(idx, meanTestCrossEntropy))
            idx += 1
            trainE, testE = predict(exs, testexs, trainLabelsFile, testLabelsFile, alpha, beta)
            wMetrics.write("error(train): {}\n".format(trainE)) #calculate training error for each epoch
            wMetrics.write("error(test): {}\n".format(testE))  #calculate test error for each epoch