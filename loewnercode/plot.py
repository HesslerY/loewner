from scipy.interpolate import spline
import matplotlib.pyplot as plt
from numpy import linspace, nan_to_num
plt.style.use('ggplot')

results_file = open('result.txt', 'r')

x_values = []
y_values = []

smooth_curve = False

for line in results_file:

    values = line.split()

    x_values.append(float(values[0]))
    y_values.append(float(values[1]))

# x_values = nan_to_num(x_values)
# y_values = nan_to_num(y_values)

# Don't smooth curve in case of a straight line
if smooth_curve:
    xnew = linspace(min(x_values),max(x_values),50)
    y_smooth = spline(x_values,y_values,xnew)

    plt.plot(xnew,y_smooth)
    plt.show()

plt.plot(x_values,y_values)
plt.show()

plt.scatter(x_values,y_values)
plt.show()


