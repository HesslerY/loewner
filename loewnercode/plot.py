from scipy.interpolate import spline
import matplotlib.pyplot as plt
from numpy import linspace, nan_to_num
import sys

plt.style.use('ggplot')

all_labels = ["$\\xi (T) = 0$",
              "$\\xi (T) = T$",
              "$\\xi (T) = \cos(T)$",
              "$\\xi (T) = \cos(\pi T)$",
              "$\\xi (T) = T \ \cos(T)$",
              "$\\xi (T) = T \ \cos(\pi T)$",
              "$\\xi (T) = \sin(T)$",
              "$\\xi (T) = \sin(\pi T)$",
              "$\\xi (T) = T \ \sin(T)$",
              "$\\xi (T) = T \ \sin(\pi T)$",
              "$\\xi (T) = 2 \ \sqrt{K \ (1 - T)}$",
              "$\\xi (T) = 2 \ \sqrt{1 \ (1 - T)}$",
              "$\\xi (T) = 2 \ \sqrt{3.5 \ (1 - T)}$",
              "$\\xi (T) = 2 \ \sqrt{4 \ (1 - T)}$",
              "$\\xi (T) = 2 \ \sqrt{6 \ (1 - T)}$",
              "$\\xi (T) = 2 \ \sqrt{8 \ (1 - T)}$"]
              
all_filenames = ["zero",
                 "T",
                 "cos(T)",
                 "cos(pi * T)",
                 "T * cos(T)",
                 "T * cos(pi * T)",
                 "sin(T)",
                 "sin(pi * T)",
                 "T * sin(T)",
                 "T * sin(pi * T)",
                 "2 * sqrt(K * (1 - T))",
                 "2 * sqrt(1 * (1 - T))",
                 "2 * sqrt(3.5 * (1 - T))",
                 "2 * sqrt(4 * (1 - T))",
                 "2 * sqrt(6 * (1 - T))",
                 "2 * sqrt(8 * (1 - T))"]
              
label_index = int(sys.argv[1])

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
    
plt.title(all_labels[label_index],fontsize=18, color='black', y=1.03)

plt.plot(x_values,y_values)
plt.savefig("output/" + all_filenames[label_index] + ".png")
# plt.show()

plt.scatter(x_values,y_values)
plt.savefig("output/" + all_filenames[label_index] + " [scatter].png")
# plt.show()


