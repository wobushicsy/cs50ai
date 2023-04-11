import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # sys.argv.append("shopping.csv")       this code is for test

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    month = {
        "Feb": 1, "Mar": 2, "Apr": 3, "May": 4, "June": 5,
        "Jul": 6, "Aug":7, "Sep": 8, "Oct": 9, "Nov": 11, 
        "Dec": 12, "Jan": 0
    }
    label = {
        "FALSE": 0, "TRUE": 1
    }
    evidences = []
    labels = []
    with open(filename) as file:
        reader = csv.reader(file)
        next(reader)
        for data in reader:
            evidence = []
            for _ in range(3):
                evidence.append(int(data[0]))
                evidence.append(float(data[1]))
                data = data[2:]
            for _ in range(4):
                evidence.append(float(data[0]))
                data = data[1:]
            evidence.append(month[data[0]])
            data = data[1:]
            for _ in range(4):
                evidence.append(int(data[0]))
                data = data[1:]
            evidence.append(1 if data[0] == "Returning_Visitor" else 0)
            evidence.append(label[data[1]])
            labels.append(label[data[-1]])
            evidences.append(evidence)
    return (evidences, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence, labels)
    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    true_labels = 0
    false_labels = 0
    true_predictions = 0
    false_predictions = 0
    for i in range(len(labels)):
        if labels[i] == 1:
            true_labels += 1
            if predictions[i] == 1:
                true_predictions += 1
        elif labels[i] == 0:
            false_labels += 1
            if predictions[i] == 0:
                false_predictions += 1
    return (true_predictions/true_labels, false_predictions/false_labels)


if __name__ == "__main__":
    main()
