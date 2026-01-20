import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import interpolate

room = pd.read_csv("testing and calibration/2609_t2.csv", sep=",")
outside = pd.read_csv("testing and calibration/2609_t3.csv", sep=",")
outside_cropped = outside.drop(outside.index[1355:1384])
freezer = pd.read_csv("testing and calibration/2709_freezer.csv", sep=",")
fridge = pd.read_csv("testing and calibration/2709_fridge.csv", sep=",")
freezer2 = pd.read_csv("testing and calibration/2709_freezer2.csv", sep=",")
fridge2 = pd.read_csv("testing and calibration/2709_fridge2.csv", sep=",")
icewater = pd.read_csv("testing and calibration/2709_icewater.csv", sep=",")

ntc_room = np.max(room["ntc"])
ntc_outside = np.max(outside_cropped["ntc"])
ntc_freezer = np.max(freezer["ntc"])
ntc_fridge = np.max(fridge["ntc"])
ntc_freezer2 = np.max(freezer2["ntc"])
ntc_fridge2 = np.max(fridge2["ntc"])
ntc_icewater = np.max(icewater["ntc"])

#print(ntc_room, ntc_outside, ntc_freezer, ntc_fridge, ntc_freezer2, ntc_fridge2, ntc_icewater)

T = [21, 5, -16, 3, -23, 5, 0, -17, 22.8, -0.7, -0.8, 0.18, -2.4, -2.30]
NTC = [ntc_room, ntc_outside, ntc_freezer, ntc_fridge, ntc_freezer2, ntc_fridge2, ntc_icewater, 2643, 835, 1780, 1865, 1800, 1825, 1843]

#f = interpolate.interp1d(np.array(T), np.array(NTC))
f, cov_matrix = np.polyfit(NTC, T, 1, cov=True)
alpha = f[0]
beta = f[1]
standard_errors = np.sqrt(np.diag(cov_matrix))
usik_T = np.sqrt( 1/(len(NTC)-2)*np.sum(np.power(T-alpha*np.array(NTC)-beta,2)) )

print("[alpha, beta]",f, "alpha*x + beta")
print("standard errors: alpha, beta, T", standard_errors, usik_T)
new_x = np.arange(750, 2800)

plt.scatter(NTC, T)
plt.plot(new_x, alpha * new_x + beta )
plt.xlabel("NTC")
plt.ylabel("T(°C)")
plt.grid(True)
plt.show()