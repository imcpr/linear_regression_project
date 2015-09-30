import csv
import numpy
import numpy as np
from numpy import matrix
from progress.bar import Bar


def list_to_float(list):
    # converts all elements in list into float and return a list of floats
    return [float(i) for i in list]

# function that reads a CSV file into to matrices - X, and Y
# where X is the example with features, and Y is the output
# feature_col_start denotes the index of the first feature column
# output_col denotes the index of the output column in the csv
# return: a tuple of (X,Y) each in numpy matrix form
def read_csv_into_matrices(filename, feature_col_start, output_col):
    # open csv file
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        inputs = []
        outputs = []
        i = 0
        for row in reader:
            if (i == 0): # strip out first row because its column header
                i = i+1
                continue
            # append row to input matrix
            input = list_to_float([1.0]+row[feature_col_start:output_col])
            inputs.append(input)
            # append output to output vector
            outputs.append(float(row[output_col]))
        # transform into numpy matrix
        X = matrix(inputs)
        Y = matrix(outputs).T
    return (X,Y)

# function that runs the closed form regression using matrix inversion
# X is the data matrix, where Y is the output
# lamb is an optional parameter denoting the lambda to be used in ridge regression
# return: the optimal weight vector
def closed_form_regression(X, Y, lamb=0):
    Xt = X.T
    XtX = Xt.dot(X)
    XtXI = XtX + numpy.identity(len(XtX))*lamb
    XtXi = numpy.linalg.inv(XtXI)
    XtXiXt = XtXi.dot(Xt)
    w = XtXiXt.dot(Y)
    return w

# function that runs the gradient descent algorithm
# X is the data matrix, where Y is the output
# iter: the number of iterations to run before terminating, if difference > epsilon
# alpha: the learning rate parameter
# lamb: the lambda parameter for ridge regression
# return: the optimal weight vector
def gradient_descent(X, Y, iter, alpha, lamb=0):
    (rows, cols) = X.shape
    Xt = X.T
    w = numpy.zeros((len(Xt), 1))
    print w.shape
    bar = Bar('iterations', max=iter)
    for i in range(0, iter):
        pw = w
        dw =  2 * (matrix.dot(matrix.dot(Xt,X), w) - matrix.dot(Xt, Y)) + 2*lamb*w
        # print w
        w = w - alpha*dw/rows
        diff =numpy.absolute(w-pw).sum()
        # print "Diff is %f " % diff
        if (diff < 0.000001):
            bar.finish()
            return w

        bar.next()
    bar.finish()
    return w
    
# computes the sum squared error
# X: the dataset
# Y: expected output
# w: weight vector
# return: integer representing the sum squared error using the weights in w
def computeSSE(X, Y, w):
    e = (Y-X.dot(w)).transpose().dot(Y-X.dot(w)).sum()
    print e
    return e

# computes the percent squared error
# X: the dataset
# Y: expected output
# w: weight vector
# return: integer representing the squared percentage error per sample using the weights in w
def computePError(X, output, w) :
    errorTotal = 0
    for i in range(len(X)):
        guess = np.dot(X[i, :], w)
        if (output[i] == 0):
            output[i] = 1
        errorTotal+= np.power((guess - output[i])/(output[i]), 2)
    error = errorTotal / len(X)
    print(error)
    return error

# computes the mean squared error
# X: the dataset
# Y: expected output
# w: weight vector
# return: integer representing the sum squared error using the weights in w
def computeMSE(X, output, w) :
    errorTotal = 0
    for i in range(len(X)):
        guess = np.dot(X[i, :], w)
        if (output[i] == 0):
            output[i] = 1
        errorTotal+= np.power((guess - output[i]), 2)
    error = errorTotal / len(X)
    print(error)

# writes predicted Y and actual Y side by side into a csv file
# fname: filename to save to
# X: data
# Y: actual output
# w: weight used to calculate predicted Y
def write_output(fname, X, Y, w):
    with open(fname, 'wb') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        yp = X.dot(w)
        for i in range(0, len(yp)):
            # print str(yp[i].sum()) + " vs " + str(Y[i].sum())
            writer.writerow([yp[i].sum()]+[Y[i].sum()])

# normalizes the dataset, divides each item in col by largest value in that column
# data: the dataset, (X), mutates the value in X
def normalize_data(data):
    (rows, cols) = data.shape
    for i in range(0, cols):
        max = 0.0
        for j in range(0,rows):
            if (numpy.abs(data[j,i]) > max):
                max = numpy.abs(data[j,i])
        # print "Max is %f" % max
        if (max > 0):
            for j in range(0, rows):
                # print "Div %f by %f" % (data[j,i], max)
                data[j,i] = data[j,i]/max

# function to perform k fold cross validation
# X: dataset to train on
# Y: output
# k: k value in k cross validation
# iter: how many iterations per dataset to run
# alpha: learning rate
# lamb: lambda for ridge regression
def k_cross_validation(X, Y, k, iter, alpha, lamb=0):
    (rows,_) = X.shape
    size = rows/k
    total_error = 0
    for i in range(0, k):
        print "K = " + str(k)
        if (i == k-1):
            print "Train from %d to %d " % (0, i*size)
            print "Val from %d to %d" %(i*size, rows)
            train = X[:i*size,] # get first k-1 sets
            val = X[i*size:,] # if last set, get til end
            val_output = Y[i*size:,]
            output = Y[:i*size,]
        else:
            print "Train from %d to %d and %d to %d" % (0, i*size, i*size+size, rows)
            print "Val from %d to %d" %(i*size, i*size+size)
            val = X[i*size:i*size+size,] # get kth set
            val_output = Y[i*size:i*size+size,]
            train = numpy.vstack((X[:i*size,], X[i*size+size:,])) #get first k-1 sets and k+1 til end
            output = numpy.vstack((Y[:i*size,], Y[i*size+size:,]))
        w = gradient_descent(train, output, iter, alpha, lamb)
        total_error += computeSSE(val, val_output, w)
    return total_error

# a few examples of the calculations we ran
def test():
    (X,Y) = read_csv_into_matrices('data/OnlineNewsPopularity.csv', 2, 60)
    print X
    normalize_data(X)
    print X
    print X.shape
    # raw_input()
    # (X,Y) = read_csv_into_matrices('data/quiz.csv', 0, 1)
    # (X,Y) = read_csv_into_matrices('data/example.csv', 0, 1)
    # w = closed_form_regression(X,Y)
    # e = computeSSE(X,Y,w)
    # write_output('output.csv', X, Y, w)
    #w2 = gradient_descent(X, Y, 5000, 0.00000000000005)   #NOT BAD
    #w2 = gradient_descent(X, Y, 5000, 0.0000000000001) #5.35452175848e+12
    #w2 = gradient_descent(X, Y, 5000, 0.0000000000007) #5.34348578427
    #w2 = gradient_descent(X, Y, 15000, 0.0000000000007) 5.33360677181e+12
    # w2 = gradient_descent(X, Y, 10000000, 0.000000000001)
    # w2 = gradient_descent(X, Y, 10000, 0.04)
    w2 = gradient_descent(X[:30000,], Y[:30000,], 200000, 0.1)

    print "On test set error"
    e2 = computeSSE(X[30000:,],Y[30000:,],w2)
    write_output('output.csv', X[30000:,],Y[30000:,],w2)
    return w2

# min_error = 10000000000000
# best = 0
# d = {}
# for r in [0, 0.01, 0.1, 1, 10, 100]:
#     err = k_cross_validation(X[:30000,], Y[:30000,], 5, 1000, 0.1, r)
#     d[r] = err
#     if( err < min_error ):
#         print "using "+str(r)+" as lambda produced lowest error so far " + str(err)
#         min_error = err
#         best = r

# print "best r is " + str(best)
