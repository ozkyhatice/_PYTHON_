import pandas as pd
from knn_operations import knn_algo
from d_tree import decisiontree

def main():
    # Diabetes veri setini oku
    df = pd.read_csv("./diabetes.csv")

    # KNN algoritmasını uygula
    knn_algo(df)


if __name__ == "__main__":
    main()
