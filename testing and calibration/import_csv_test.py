import csv
import pandas as pd
import matplotlib.pyplot as plt

def read_csv(filepath):
    data_array = []
    with open(filepath, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data_array.append(row)
    return data_array



#data = read_csv("2409_1.csv")
data = pd.read_csv("2409_1.csv", sep=";")
data = data.dropna()
print(data["pressure"]*1e-2)

plt.plot(data["pressure"]*1e-2)
plt.show()


