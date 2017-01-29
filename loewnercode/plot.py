# from scipy.interpolate import spline
import matplotlib.pyplot as plt
import numpy as np
import cmath
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
                 "2 * sqrt(1 * (1 - T))",
                 "2 * sqrt(3.5 * (1 - T))",
                 "2 * sqrt(4 * (1 - T))",
                 "2 * sqrt(6 * (1 - T))",
                 "2 * sqrt(8 * (1 - T))"]
              
label_index = int(sys.argv[1])

results_file = open('result.txt', 'r')

# x_values = []
# y_values = []

g_zero_array = np.empty((0))

smooth_curve = False

for line in results_file:

    values = line.split()
    
    g_zero = complex(float(values[0]),float(values[1]))
    g_zero_array = np.append(g_zero_array,g_zero)
    
partial_filename = "output/" + all_filenames[label_index]
    
plt.title(all_labels[label_index],fontsize = 18, color='black', y = 1.03)
plt.plot(g_zero_array.real,g_zero_array.imag)
plt.savefig(partial_filename + ".png")
plt.cla()

plt.title(all_labels[label_index],fontsize = 18, color='black', y = 1.03)
plt.scatter(g_zero_array.real,g_zero_array.imag)
plt.savefig(partial_filename + " [scatter].png")
plt.cla()

plt.title(all_labels[label_index],fontsize = 18, color='black', y = 1.03)
for complex_num in g_zero_array:
    
    plt.polar([0,cmath.polar(complex_num)[1]],[0,cmath.polar(complex_num)[0]],marker='o')

plt.savefig(partial_filename + " [polar].png")

print("Saved plots for " + partial_filename[7:])


