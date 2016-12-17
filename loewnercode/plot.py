from scipy.interpolate import spline
import matplotlib.pyplot as plt
from numpy import linspace 
plt.style.use('ggplot')

results_file = open('result.txt', 'r')

x_values = []
y_values = []

for line in results_file:
    nobrackets = (line.replace("(","")).replace(")","")
    values = nobrackets.split(",")

    x_values.append(float(values[0]))
    y_values.append(float(values[1]))

# xnew = linspace(min(x_values),max(x_values),50)
# y_smooth = spline(x_values,y_values,xnew)

plt.plot(x_values,y_values)
plt.show()

# plt.plot(xnew,y_smooth)
# plt.show()
