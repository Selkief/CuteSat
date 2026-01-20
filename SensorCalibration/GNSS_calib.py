import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import ScalarFormatter

data1 = pd.read_csv("testing and calibration/2509_GNSS_test2.csv", sep=",")
data2 = pd.read_csv("testing and calibration/2609_GNSS_test3.csv", sep=",")

##not done yet:
def degrees_to_meters(latitude, longitude):
    lat_meters = latitude * 111111*np.cos(np.radians(78.2227))
    lon_meters = longitude * 111111
    return lat_meters, lon_meters


lon_mean1, lat_mean1 = np.mean(data1["lon"]), np.mean(data1["lat"])
lon_mean2, lat_mean2 = np.mean(data2["lon"]), np.mean(data2["lat"])
lon_min1, lat_min1, lon_min2, lat_min2 = np.min(data1["lon"]), np.min(data1["lat"]), np.min(data2["lon"]), np.min(data2["lat"])
lon_max1, lat_max1, lon_max2, lat_max2 = np.max(data1["lon"]), np.max(data1["lat"]), np.max(data2["lon"]), np.max(data2["lat"])
std1_lon, std1_lat, std2_lon, std2_lat = np.std(data1["lon"]), np.std(data1["lat"]), np.std(data2["lon"]), np.std(data2["lat"])
std1_lon_m, std1_lat_m = degrees_to_meters(std1_lon, std1_lat)
std2_lon_m, std2_lat_m = degrees_to_meters(std2_lon, std2_lat)

print("Elvesletta:")
print("mean values: lon:", lon_mean1, "lat:", lat_mean1)
print("min values: lon:", lon_min1, "lat:", lat_min1)
print("max values: lon:", lon_max1, "lat:", lat_max1)
print("std lon:", std1_lon, "std lat:", std1_lat)
print("std lon meters:", std1_lon_m, "std lat meters:", std1_lat_m)

print("UNIS:")
print("mean values: lon:", lon_mean2, "lat: ", lat_mean2)
print("min values: lon:", lon_min2, "lat:", lat_min2)
print("max values: lon:", lon_max2, "lat:", lat_max2)
print("std lon:", std2_lon, "std lat:", std2_lat)
print("std lon meters:", std2_lon_m, "std lat meters:", std2_lat_m)

y_formatter = ScalarFormatter(useOffset=False)

fig, axs = plt.subplots(2)
fig.suptitle('Altitude from GNSS')
axs[0].plot(data1["alt"])
axs[0].set_title("2nd floor Elvesletta")
axs[0].set_ylabel("altitude [m]")
axs[1].plot(data2["alt"])
axs[1].set_title("outside Kapp Mitra classroom")
axs[1].set_ylabel("altitude [m]")
plt.tight_layout()
#plt.show()

fig, axs = plt.subplots(2)
fig.suptitle('Longitude measurements')
axs[0].plot(data1["lon"])
axs[0].set_title("2nd floor Elvesletta")
axs[0].set_ylabel("degrees East")
axs[0].yaxis.set_major_formatter(y_formatter)
axs[1].plot(data2["lon"])
axs[1].set_title("outside Kapp Mitra classroom")
axs[1].set_ylabel("degrees East")
axs[1].yaxis.set_major_formatter(y_formatter)
plt.tight_layout()
#plt.show()

fig, axs = plt.subplots(2)
fig.suptitle('Latitude measurements')
axs[0].plot(data1["lat"])
axs[0].set_title("2nd floor Elvesletta")
axs[0].set_ylabel("degrees North")
axs[0].yaxis.set_major_formatter(y_formatter)
axs[1].plot(data2["lat"])
axs[1].set_title("outside Kapp Mitra classroom")
axs[1].set_ylabel("degrees North")
axs[1].yaxis.set_major_formatter(y_formatter)
plt.tight_layout()
#plt.show()