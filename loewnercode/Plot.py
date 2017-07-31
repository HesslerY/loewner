from sys import argv
import matplotlib.pyplot as plt
from math import pi, degrees
from numpy import arctan2

plt.style.use('ggplot')

label_index = int(argv[1])
remove_last = int(argv[2])
square_root_value = argv[3]

all_labels = ["$\\xi (t) = 0$",
              "$\\xi (t) = t$",
              "$\\xi (t) = \cos(t)$",
              "$\\xi (t) = t \ \cos(t)$",
              "$\\xi (t) = \cos(\pi t)$",
              "$\\xi (t) = t \ \cos(\pi t)$",
              "$\\xi (t) = \sin(t)$",
              "$\\xi (t) = t \ \sin(t)$",
              "$\\xi (t) = \sin(\pi t)$",
              "$\\xi (t) = t \ \sin(\pi t)$",
              "$\\xi (t) = 2 \ \sqrt{" + square_root_value + " \ (1 - t)}$",
              "$\\xi (t) = c_{" + square_root_value + "} \sqrt{t}$"]

all_filenames = ["zero",
                 "t",
                 "cos(t)",
                 "t * cos(t)",
                 "cos(pi * t)",
                 "t * cos(pi * t)",
                 "sin(t)",
                 "t * sin(t)",
                 "sin(pi * t)",
                 "t * sin(pi * t)",
                 "2 * sqrt(" + square_root_value + " * (1 - t))",
                 "c" + square_root_value + "-sqrt(t)"]

results_file = open('result.txt', 'r')

real_values = []
imag_values = []

for line in results_file:

    values = line.split()

    real_values.append(float(values[0]))
    imag_values.append(float(values[1]))

if remove_last == 1:

    real_values = real_values[1:-1]
    imag_values = imag_values[1:-1]

if label_index == 11:

    max_x = real_values[-1]
    max_y = real_values[-1]
    angle = arctan2(max_y , max_x) / pi
    alpha_data = [square_root_value, str(angle)]
    print(alpha_data)
    plt.axis((-5,5,0,6))

partial_filename = "output/" + all_filenames[label_index]

# plt.figure(figsize=(4.5, 3))

plt.title(all_labels[label_index],fontsize = 12, color='black', y = 1.02)
plt.plot(real_values,imag_values)
# plt.axis('equal')
plt.savefig(partial_filename + ".png")

## Test!

exit()

plt.cla()
plt.title(all_labels[label_index],fontsize = 14, color='black', y = 1.03)
plt.scatter(real_values,imag_values)
plt.savefig(partial_filename + " [scatter].png")
# plt.axis('equal')
