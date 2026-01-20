import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data1 = pd.read_csv("2509_p1.csv")
data2 = pd.read_csv("2509_p2.csv")
data3 = pd.read_csv("2509_p3.csv")
data4 = pd.read_csv("2509_p4.csv")

data_outside = pd.read_csv("2509_t.csv")

#print(data1)

avg1 = np.mean(data1)
avg2 = np.mean(data2)
avg3 = np.mean(data3)
avg4 = np.mean(data4)

print("mean pressure: reception: ", avg1, "first floor: ", avg2, "second floor: ", avg3, "rooftop: ", avg4)

outside_cropped = data_outside.iloc[40:75]
avg_ADC = np.mean(outside_cropped)

print("ADC outside classroom: ", avg_ADC)
