import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

#reading the data for all the flights from drop to landing (determined from pressure meassurements)
rows_toskip_1 = np.arange(1,141)
rows_toskip_2 = np.arange(1,149)
rows_toskip_3 = np.arange(1,85)
rows_toskip_4 = np.arange(1,144)
rows_toskip_5 = np.arange(1,93)
rows_toskip_6 = np.arange(1,93)
rows_toskip_7 = np.arange(1,87)
rows_toskip_8 = np.arange(1,111)
rows_toskip_9 = np.arange(1,73)
rows_toskip_10 = np.arange(1,82)
rows_toskip_11 = np.arange(1,199)
rows_toskip_13 = np.arange(1,87)

data1 = pd.read_csv("flightdata/3009_cutesat1.csv", sep=",", skiprows=rows_toskip_1)
data2 = pd.read_csv("flightdata/3009_cutesat2.csv", sep=",", skiprows=rows_toskip_2)
data3 = pd.read_csv("flightdata/3009_cutesat3.csv", sep=",", skiprows=rows_toskip_3)
data4 = pd.read_csv("flightdata/3009_cutesat4.csv", sep=",", skiprows=rows_toskip_4)
data5 = pd.read_csv("flightdata/3009_cutesat5.csv", sep=",", skiprows=rows_toskip_5)
data6 = pd.read_csv("flightdata/3009_cutesat6.csv", sep=",", skiprows=rows_toskip_6)
data7 = pd.read_csv("flightdata/3009_cutesat7.csv", sep=",", skiprows=rows_toskip_7)
data8 = pd.read_csv("flightdata/3009_cutesat8.csv", sep=",", skiprows=rows_toskip_8)
data9 = pd.read_csv("flightdata/3009_cutesat9.csv", sep=",", skiprows=rows_toskip_9)
data10 = pd.read_csv("flightdata/3009_cutesat10.csv", sep=",", skiprows=rows_toskip_10)
data11 = pd.read_csv("flightdata/210_cutesat11.csv", sep=",", skiprows=rows_toskip_11)
data13 = pd.read_csv("flightdata/210_cutesat13.csv", sep=",", skiprows=rows_toskip_13)
data = [data1, data2, data3, data4, data5, data6, data7, data8, data9, data10, data11, data13]

#parameters from ntc calibration
alpha = -2.21782344e-02
beta = 3.98125194e+01

def get_param(data_name, variable):
    return data_name[variable]

#calculate the temperature from the ntc value
def calc_temp(data):
    ntc_values = data["ntc"]
    return alpha * ntc_values + beta

#calculate a new time from the GPS time for each flight starting at the drop
def calc_interval(data):
    time_s = data["hh"]*3600 + data["mm"]*60 + data["ss"]
    interval_length = np.max(time_s) - np.min(time_s)
    interval = np.linspace(0, interval_length, len(data["hh"]))
    return interval

t = []
for i in range(len(data)):
    time = calc_interval(data[i])
    t.append(time)

t_short = []
for i in range(len(data)):
    shortened = np.delete(t[i],-1)
    t_short.append(shortened)



ntc_temp = []
for i in range(len(data)):
    ntc = calc_temp(data[i])
    ntc_temp.append(ntc)

pressure = []
for i in range(len(data)):
    pressure.append(get_param(data[i], "p"))

humidity = []
for i in range(len(data)):
    humidity.append(get_param(data[i], "H"))

v_lon = [[] for _ in range(12)] #east_west
v_lat = [[] for _ in range(12)] #north-south
v_lat_m = [[] for _ in range(12)] #north-south
v_lon_m = [[] for _ in range(12)] #east-west

#converting latitude and longitude coordinates(decimals) at about 78 degrees N into meters
# (makes mostly sense for distances)
def degrees_to_meters(latitude, longitude, lat_list, lon_list):
    for i in range(len(latitude)):
        lat_meters = latitude[i] * 111111
        lon_meters = longitude[i] * 111111.0*np.cos(np.radians(78.2227))
        lat_list.append(lat_meters)
        lon_list.append(lon_meters)

#calculating velocity from position coordinates (discrete derivative)
def calc_velocity(data, t_list, v_lat_list, v_lon_list):
    for i in range(len(t_list)-1):
        v_longitude = float((data.iloc[i+1, 3] - data.iloc[i, 3])/(t_list[i+1] - t_list[i]))
        v_latitude = float((data.iloc[i+1, 2] - data.iloc[i, 2])/(t_list[i+1] - t_list[i]))
        v_lat_list.append(v_latitude)
        v_lon_list.append(v_longitude)


for k in range(len(data)):
    calc_velocity(data[k], t[k], v_lat[k], v_lon[k])
for k in range(len(data)):
    degrees_to_meters(v_lat[k], v_lon[k], v_lat_m[k], v_lon_m[k])

#get wind average speed and direction for flights 3 and 5
v_lat_mean3 = np.mean(v_lat_m[2])
v_lat_mean5 = np.mean(v_lat_m[4])
v_lon_mean3 = np.mean(v_lon_m[2])
v_lon_mean5 = np.mean(v_lon_m[4])


#calculate the height from pressure --> hydrostatic equilibrium and scaleheight

R_a = 287 #gas constant air in [J/(kg*K)]
T_a = 273
T = [272, 272, 272, 273, 273, 273, 273, 271, 271, 271, 278, 279] #assumed constant temperature at location [K]
g = 9.81 #grav. acceleration [m/s2]
height_KHO = 518 #startingpoint for flights - height above sealevel [m]

heights = [[]for i in range(len(data))]
def calc_height(p_data, height_list):
    p0 = p_data[0]
    p1 = p_data
    height = (R_a*T_a)/g*np.log(p0/p1)
    height_list.append(height)

for k in range(len(data)):
    calc_height(pressure[k],heights[k])

GNSS_altitude = []
for m in range(len(data)):
    set = data[m]
    GNSS_altitude.append(set["alt"])

pitch = []
for i in range(len(data)):
    pitch.append(get_param(data[i], "pitch"))

roll = []
for i in range(len(data)):
    roll.append(get_param(data[i], "roll"))

yaw = []
for i in range(len(data)):
    yaw.append(get_param(data[i], "yaw"))



cmap = mpl.colormaps['plasma']
colors = cmap(np.linspace(0, 1, 12))
plt.rcParams.update({'font.size': 14})

fig, axs = plt.subplots(3,1)
axs[0].plot(t[2], pitch[2], label= f"flight {2+1}", color=colors[2])
axs[0].plot(t[4], pitch[4], label= f"flight {4+1}", color=colors[4])
axs[0].set_ylabel("pitch")
axs[0].set_xlabel("time after drop (s)")
axs[0].grid(True)
axs[0].legend()
axs[1].plot(t[2], roll[2], label= f"flight {2+1}", color=colors[2])
axs[1].plot(t[4], roll[4], label= f"flight {4+1}", color=colors[4])
axs[1].set_ylabel("roll")
axs[1].set_xlabel("time after drop (s)")
axs[1].grid(True)
axs[1].legend()
axs[2].plot(t[2], yaw[2], label= f"flight {2+1}", color=colors[2])
axs[2].plot(t[4], yaw[4], label= f"flight {4+1}", color=colors[4])
axs[2].set_ylabel("yaw")
axs[2].set_xlabel("time after drop (s)")
axs[2].grid(True)
axs[2].legend()
plt.tight_layout()
plt.show()

for i in range(len(data)):
    plt.scatter(t[i], GNSS_altitude[i], label= f"flight {i+1}", color=colors[i], s=20)
plt.ylabel("height from drop (m) from GNSS")
plt.xlabel("time after drop (s)")
plt.grid(True)
plt.legend()
plt.show()

for i in range(len(data)):
    plt.scatter(t[i], heights[i], label= f"flight {i+1}", color=colors[i], s=20)
plt.ylabel("height from drop (m)")
plt.xlabel("time after drop (s)")
plt.grid(True)
plt.legend()
plt.show()

for i in range(len(data)):
    plt.scatter(t[i], pressure[i], label= f"flight {i+1}", color=colors[i], s=20)
plt.xlabel("time after drop (s)")
plt.ylabel("pressure (hPa)")
plt.grid(True)
plt.legend()
plt.show()

for i in range(len(data)):
    plt.scatter(t[i], ntc_temp[i], label= f"flight {i+1}", color=colors[i], s=20)
plt.xlabel("time after drop (s)")
plt.ylabel("temperature(C) from ntc")
plt.grid(True)
plt.legend()
plt.show()

for i in range(len(data)):
    plt.scatter(t[i], humidity[i], label= f"flight {i+1}", color=colors[i], s=20)
plt.xlabel("time after drop (s)")
plt.ylabel("humidity (%)")
plt.grid(True)
plt.legend()
plt.show()

fig, axs = plt.subplots(1,4)
axs[0].scatter(v_lat_m[2], t_short[2], label= f"flight {3}", color=colors[2], s=20)
axs[0].axvline(x=v_lat_mean3, color='red', linestyle=':', label='mean speed')
axs[0].set_xlabel("horizontal velocity N-S (m/s)")
axs[0].set_ylabel("time after drop (s)")
axs[0].legend(loc="upper left")
axs[0].grid(True)
axs[1].scatter(v_lat_m[4],t_short[4], label= f"flight {5}", color=colors[4], s=20)
axs[1].axvline(x=v_lat_mean5, color='red', linestyle=':', label='mean speed')
axs[1].set_xlabel("horizontal velocity N-S (m/s)")
axs[1].set_ylabel("time after drop (s)")
axs[1].legend(loc="upper left")
axs[1].grid(True)
axs[2].scatter(v_lon_m[2], t_short[2], label= f"flight {3}", color=colors[2], s=20)
axs[2].axvline(x=v_lon_mean3, color='red', linestyle=':', label='mean speed')
axs[2].set_xlabel("horizontal velocity E-W (m/s)")
axs[2].set_ylabel("time after drop (s)")
axs[2].legend(loc="upper left")
axs[2].grid(True)
axs[3].scatter(v_lon_m[4], t_short[4], label= f"flight {5}", color=colors[4], s=20)
axs[3].axvline(x=v_lon_mean5, color='red', linestyle=':', label='mean speed')
axs[3].set_xlabel("horizontal velocity E-W (m/s)")
axs[3].set_ylabel("time after drop (s)")
axs[3].legend(loc="upper left")
axs[3].grid(True)
plt.tight_layout()
plt.show()