import pandas as pd
import math
import time
import numpy as np


def leaveOneOutEvaluation(data, features):
    # converted from pandas dataframe to numpy because I found out it's much slower https://stackoverflow.com/questions/54549284/convert-dataframe-to-2d-array
    newData = data.values
    numberClassifiedCorrect = 0
    numInstances = len(data.axes[0])  # gets number of rows
    numFeatures = len(data.axes[1])   # gets number of columns

    for i in range(0, numInstances):
        objectToClassify = i
        labelObjectToClassify = newData[objectToClassify][0]
        # https://www.geeksforgeeks.org/python-infinity/
        nearestNeighborDistance = float('inf')
        nearestNeighborLocation = float('inf')
        for j in range(0, numInstances):
            if j != i:
                distance = 0
                # iterate and calucalte the total distance: distance = sqrt(sum((object_to_classify-data(k,2:end)).^2)); from the slides
                for k in range(0, len(features)):
                    distance += pow(newData[objectToClassify]
                                    [features[k]] - newData[j][features[k]], 2)

                # People said that numpy functions would speed up the program but it did not
                # I wanted to try and increase my program because it takes quite a while at the moment but this was a failed attempt
                # distance = np.linalg.norm(
                #     newData[objectToClassify][features] - newData[j][features])
                # temp = newData[objectToClassify][features] - \
                #     newData[j][features]
                # distance = np.sqrt(np.dot(temp.T, temp))
                # distance = np.sqrt(np.sum(np.square(temp)))

                distance = math.sqrt(distance)
                if distance < nearestNeighborDistance:
                    nearestNeighborDistance = distance
                    nearestNeighborLocation = j
                    nearestNeighborLabel = newData[nearestNeighborLocation][0]

        if labelObjectToClassify == nearestNeighborLabel:
            numberClassifiedCorrect += 1

    return (numberClassifiedCorrect/numInstances) * 100


def forwardSelection(data):
    # used https://stackoverflow.com/questions/12444004/how-long-does-my-python-application-take-to-run
    start_time = time.time()
    numInstances = len(data.axes[0])  # gets number of rows
    numFeatures = len(data.axes[1])   # gets number of columns
    currentFeatures = []  # keeps track of the features being used
    bestFeatures = []
    featureToAdd = []
    # keeps track of the very best accuracy, bestAccuracy only keeps track of the bestAccuracy given the next options
    overallBestAccuracy = 0

    for i in range(1, numFeatures):
        bestAccuracy = 0
        flag = 0

        for j in range(1, numFeatures):
            if j not in currentFeatures:
                tempFeatures = currentFeatures.copy()
                tempFeatures.append(j)
                tempAccuracy = leaveOneOutEvaluation(data, tempFeatures)
                print("\tUsing feature(s) {", tempFeatures,
                      "} accuracy is ", tempAccuracy, "%")
                if tempAccuracy > bestAccuracy:  # keeps track of the next best accuracy and not the VERY best one
                    bestAccuracy = tempAccuracy
                    # currentFeatures.append(j)
                    featureToAdd = j
                    # only add to bestFeatures if the calculated accucuracy is the new best accuracy
                    if bestAccuracy > overallBestAccuracy:
                        overallBestAccuracy = bestAccuracy
                        # bestFeatures.append(j)
                        flag = 1
        if flag == 1:
            print("Feature set {", currentFeatures,
                  "} was best, accuracy is ", bestAccuracy, "%\n")
            bestFeatures.append(featureToAdd)
            currentFeatures.append(featureToAdd)
        else:
            currentFeatures.append(featureToAdd)
            print(
                "(Warning, Accuracy has decreased! Continuing search in case of local maxima)\n")
            print("Feature set {", currentFeatures,
                  "} was best, accuracy is ", bestAccuracy, "%\n")

    print("Finishd Search!! The best feature subset is {", bestFeatures,
          "}, which has an accuracy of", overallBestAccuracy, "%\n")
    print("Program took ", time.time() - start_time, "seconds to run")


def backwardElimination(data):
    # used https://stackoverflow.com/questions/12444004/how-long-does-my-python-application-take-to-run
    start_time = time.time()
    numInstances = len(data.axes[0])  # gets number of rows
    numFeatures = len(data.axes[1])   # gets number of columns
    currentFeatures = []  # keeps track of the features being used
    bestFeatures = []
    featureToRemove = []

    for i in range(1, numFeatures):  # fills the arrays so we can eliminate
        currentFeatures.append(i)
        bestFeatures.append(i)
    # keeps track of the very best accuracy, bestAccuracy only keeps track of the bestAccuracy given the next options
    overallBestAccuracy = 0

    for i in range(1, numFeatures):
        bestAccuracy = 0
        flag = 0

        for j in range(1, numFeatures):
            if j in currentFeatures:
                # print("currentFeatures:", currentFeatures)
                # used https://stackoverflow.com/questions/11362232/python-variables-changing-when-they-shouldnt to learn that in python you need to make a copy or else temp array will be changed too
                tempFeatures = currentFeatures.copy()
                tempFeatures.remove(j)
                tempAccuracy = leaveOneOutEvaluation(data, tempFeatures)
                print("\tUsing feature(s) {", tempFeatures,
                      "} accuracy is ", tempAccuracy, "%")
                if tempAccuracy > bestAccuracy:  # keeps track of the next best accuracy and not the VERY best one
                    bestAccuracy = tempAccuracy
                    featureToRemove = j
                    # currentFeatures.remove(j)
                    # only add to bestFeatures if the calculated accucuracy is the new best accuracy
                    if bestAccuracy > overallBestAccuracy:
                        overallBestAccuracy = bestAccuracy
                        # bestFeatures.remove(j)
                        flag = 1
        if flag == 1:
            print("Feature set {", currentFeatures,
                  "} was best, accuracy is ", bestAccuracy, "%\n")
            currentFeatures.remove(featureToRemove)
            bestFeatures.remove(featureToRemove)
        else:
            currentFeatures.remove(featureToRemove)
            print(
                "(Warning, Accuracy has decreased! Continuing search in case of local maxima)\n")
            print("Feature set {", currentFeatures,
                  "} was best, accuracy is ", bestAccuracy, "%\n")

    print("Finishd Search!! The best feature subset is {", bestFeatures,
          "}, which has an accuracy of", overallBestAccuracy, "%\n")
    print("Program took ", time.time() - start_time, "seconds to run")


def main():
    print("Welcome to Feature Selection Algorithm.")
    fileName = input("Type in the name of the file to test :")
    searchNum = int(input(
        "Type in the number of the algorithm you want to run.\n\t1) Forward Selection\n\t2) Backward Elimination\n"))

    data = pd.read_csv(fileName, sep="  ", engine='python', header=None)
    numInstances = len(data.axes[0])  # gets number of rows
    numFeatures = len(data.axes[1]) - 1  # gets number of columns

    print("This dataset has ", numFeatures,
          " features (not including the class attribute), with ", numInstances, " instances.\n")

    currentFeatures = []
    for i in range(1, numFeatures+1):
        currentFeatures.append(i)
    tempAccuracy = leaveOneOutEvaluation(data, currentFeatures)
    print("Running nearest neighbor with all ", numFeatures,
          " features, using \"leaving-one-out\" evaluation, I get an accuracy of ", tempAccuracy, "%\n")

#
    # print(data)
    # values = data.values
    # print("help", type(currentFeatures))
    # print("values type: ", type(values))
    # print("data type: ", type(data))
    # # print(values)
    # row1 = values[0][0]
    # print("row1: ", row1)

    print("Beginning Search.\n")
    if searchNum == 1:
        forwardSelection(data)
    if searchNum == 2:
        backwardElimination(data)


if __name__ == '__main__':
    main()
