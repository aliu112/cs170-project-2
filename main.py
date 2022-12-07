import pandas as pd


def nearestNeighbor():
    print()


def leaveOneOutEvaluation(data, features):
    return 1


def forwardSelection(data):
    numInstances = len(data.axes[0])  # gets number of rows
    numFeatures = len(data.axes[1]) - 1  # gets number of columns
    currentFeatures = []  # keeps track of the features being used
    bestFeatures = []
    # keeps track of the very best accuracy, bestAccuracy only keeps track of the bestAccuracy given the next options
    overallBestAccuracy = 0

    for i in range(1, numFeatures):
        bestAccuracy = 0
        flag = 0

        for j in range(1, numFeatures):
            if j not in currentFeatures:
                tempFeatures = currentFeatures
                tempFeatures.append(j)
                tempAccuracy = leaveOneOutEvaluation(data, tempFeatures)
                print("\tUsing feature(s) {", tempFeatures,
                      "} accuracy is ", tempAccuracy, "%")
                if tempAccuracy > bestAccuracy:  # keeps track of the next best accuracy and not the VERY best one
                    bestAccuracy = tempAccuracy
                    currentFeatures.append(j)
                    # only add to bestFeatures if the calculated accucuracy is the new best accuracy
                    if bestAccuracy > overallBestAccuracy:
                        overallBestAccuracy = bestAccuracy
                        bestFeatures.append(j)
                        flag = 1
        if flag == 1:
            print("Feature set {", currentFeatures,
                  "} was best, accuracy is ", bestAccuracy, "%\n")
        else:
            print(
                "(Warning, Accuracy has decreased! Continuing search in case of local maxima)\n")
            print("Feature set {", currentFeatures,
                  "} was best, accuracy is ", bestAccuracy, "%\n")

    print("Finishd Search!! The best feature subset is {", bestFeatures,
          "}, which has an accuracy of", overallBestAccuracy, "%\n")


def backwardElimination(data):
    print("backward")


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
    tempAccuracy = leaveOneOutEvaluation(data)
    print("Running nearest neighbor with all ", numFeatures,
          " features, using \"leaving-one-out\" evaluation, I get an accuracy of ", tempAccuracy, "%\n")
    print(numFeatures)
    print(numInstances)
    print(data)

    print("Beginning Search.\n")
    if searchNum == 1:
        forwardSelection(data)
    if searchNum == 2:
        backwardElimination(data)


if __name__ == '__main__':
    main()
