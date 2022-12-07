import pandas as pd


def nearestNeighbor():
    print()


def leaveOneOutEvaluation(data, features):
    return 1


def forwardSelection(data):
    numInstances = len(data.axes[0])  # gets number of rows
    numFeatures = len(data.axes[1])   # gets number of columns
    currentFeatures = []  # keeps track of the features being used
    bestFeatures = []
    featureToAdd = []
    # keeps track of the very best accuracy, bestAccuracy only keeps track of the bestAccuracy given the next options
    overallBestAccuracy = 0

    for i in range(1, numFeatures):  # +1 because pandas reads columns 0-6
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


def backwardElimination(data):
    numInstances = len(data.axes[0])  # gets number of rows
    numFeatures = len(data.axes[1])   # gets number of columns
    currentFeatures = []  # keeps track of the features being used
    bestFeatures = []
    featureToRemove = []

    for i in range(1, numFeatures):
        currentFeatures.append(i)
        bestFeatures.append(i)
    # keeps track of the very best accuracy, bestAccuracy only keeps track of the bestAccuracy given the next options
    overallBestAccuracy = 0

    for i in range(1, numFeatures):
        bestAccuracy = 0
        flag = 0

        for j in range(1, numFeatures):
            if j in currentFeatures:
                #print("currentFeatures:", currentFeatures)
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

    print(data)

    print("Beginning Search.\n")
    if searchNum == 1:
        forwardSelection(data)
    if searchNum == 2:
        backwardElimination(data)


if __name__ == '__main__':
    main()
