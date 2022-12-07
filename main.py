import pandas as pd


def nearestNeighbor():
    print()


def main():
    print("Welcome to Feature Selection Algorithm.")
    fileName = input("Type in the name of the file to test :")
    searchNum = int(input(
        "Type in the number of the algorithm you want to run.\n     1) Forward Selection\n     2) Backward Elimination\n"))

    data = pd.read_csv(fileName, sep="  ", engine='python', header=None)
    print(data)


if __name__ == '__main__':
    main()
