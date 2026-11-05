import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

try:
    data = pd.read_csv("results.csv")
except FileNotFoundError:
    print("File results.csv not found")
    exit()

marks = []
for i in range(len(data)):
    roll = data["RollNo"][i]
    m = pd.to_numeric(data["Marks"][i], errors="coerce")
    if pd.isna(m):
        print("Warning: Row", roll, "skipped - marks missing")
    elif m < 0 or m > 100:
        print("Warning: Row", roll, "skipped - marks must be between 0 and 100.")
    else:
        marks.append(m)

if len(marks) == 0:
    print("No valid marks found. Nothing to analyse.")
    exit()

marks = pd.Series(marks, dtype=float)

while True:
    print("\n1. Show statistics")
    print("2. Pass percentage and distribution")
    print("3. Exit")
    choice = input("Enter choice: ")

    if choice == "1":
        print("Students:", len(marks))
        print("Mean: %.2f" % marks.mean())
        print("Median: %.2f" % marks.median())
        print("Mode: %g" % marks.mode().min())
        print("Highest: %g | Lowest: %g" % (marks.max(), marks.min()))
        print("Standard deviation: %.2f" % np.std(marks))

    elif choice == "2":
        passed = int((marks >= 40).sum())
        failed = len(marks) - passed
        percent = passed / len(marks) * 100
        print("Passed:", passed, "| Failed:", failed, "| Pass percentage: %.2f%%" % percent)

        labels = ["0-39", "40-59", "60-79", "80-100"]
        bands = pd.cut(marks, bins=[0, 40, 60, 80, 101], labels=labels, right=False)
        counts = bands.value_counts().reindex(labels)

        for label in labels:
            print(label, ":", counts[label])

        plt.bar(labels, counts.values, color="steelblue")
        plt.title("Students per mark band")
        plt.xlabel("Marks band")
        plt.ylabel("Number of students")
        plt.show()

    elif choice == "3":
        break
    else:
        print("Wrong choice, try again")