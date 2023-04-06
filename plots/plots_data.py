import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt("adxl.csv",delimiter=",", dtype=float,encoding="utf-8")
data_T = np.transpose(data)

x_data = data_T[0]
y_data = data_T[1]
z_data = data_T[2]
'''
x_data_1 = x_data[0:10201]
x_data_2 = x_data[10201:21307]
x_data_3 = x_data[21307:32208]
x_data_4 = x_data[32208:43814]
x_data_5 = x_data[43814:55136]
x_data_6 = x_data[55136:66342]
x_data_7 = x_data[66342:77563]

y_data_1 = y_data[0:10201]
y_data_2 = y_data[10201:21307]
y_data_3 = y_data[21307:32208]
y_data_4 = y_data[32208:43814]
y_data_5 = y_data[43814:55136]
y_data_6 = y_data[55136:66342]
y_data_7 = y_data[66342:77563]

z_data_1 = z_data[0:10201]
z_data_2 = z_data[10201:21307]
z_data_3 = z_data[21307:32208]
z_data_4 = z_data[32208:43814]
z_data_5 = z_data[43814:55136]
z_data_6 = z_data[55136:66342]
z_data_7 = z_data[66342:77563]

x = []
x_1 = [1 for i in range(10201)]
x_2 = [2 for i in range(11106)]
x_3 = [3 for i in range(10901)]
x_4 = [4 for i in range(11606)]
x_5 = [5 for i in range(11322)]
x_6 = [6 for i in range(11206)]
x_7 = [7 for i in range(11221)]
x = np.concatenate([x_1,x_2,x_3,x_4,x_5,x_6,x_7])
'''

x = [i for i in range(77563)]
#x = [i for i in range(10201)]

plt.plot(x, x_data, label="x-axis") #row_data
plt.plot(x, y_data, label="y-axis") #row_data
plt.plot(x, z_data, label="z-axis") #row_data
plt.xlabel("earthquake",fontsize=13)
plt.ylabel("acceleration",fontsize=13)

plt.legend(loc="upper right", prop={'size': 6})
plt.savefig('data_plots.png', dpi=199)
print('figure save')
plt.show()
