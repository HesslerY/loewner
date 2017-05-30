from sys import argv
import matplotlib.pyplot as plt
from math import pi, degrees
from numpy import arctan2

plt.style.use('ggplot')

label_index = int(argv[1])
remove_last = int(argv[2])
alpha_value = argv[3]

all_labels = ["$\\xi (t) = 0$",
              "$\\xi (t) = t$",
              "$\\xi (t) = \cos(t)$",
              "$\\xi (t) = \cos(\pi t)$",
              "$\\xi (t) = t \ \cos(t)$",
              "$\\xi (t) = t \ \cos(\pi t)$",
              "$\\xi (t) = \sin(t)$",
              "$\\xi (t) = \sin(\pi t)$",
              "$\\xi (t) = t \ \sin(t)$",
              "$\\xi (t) = t \ \sin(\pi t)$",
              "$\\xi (t) = 2 \ \sqrt{1 \ (1 - t)}$",
              "$\\xi (t) = 2 \ \sqrt{2.5 \ (1 - t)}$",
              "$\\xi (t) = 2 \ \sqrt{3.5 \ (1 - t)}$",
              "$\\xi (t) = 2 \ \sqrt{4 \ (1 - t)}$",
              "$\\xi (t) = 2 \ \sqrt{4.5 \ (1 - t)}$",
              "$\\xi (t) = 2 \ \sqrt{6 \ (1 - t)}$",
              "$\\xi (t) = 2 \ \sqrt{8 \ (1 - t)}$",
              "$\\xi (t) = c_{" + alpha_value + "} \sqrt{t}$"]

all_filenames = ["zero",
                 "t",
                 "cos(t)",
                 "cos(pi * t)",
                 "t * cos(t)",
                 "t * cos(pi * t)",
                 "sin(t)",
                 "sin(pi * t)",
                 "t * sin(t)",
                 "t * sin(pi * t)",
                 "2 * sqrt(1 * (1 - t))",
                 "2 * sqrt(2.5 * (1 - t))",
                 "2 * sqrt(3.5 * (1 - t))",
                 "2 * sqrt(4 * (1 - t))",
                 "2 * sqrt(4.5 * (1 - t))",
                 "2 * sqrt(6 * (1 - t))",
                 "2 * sqrt(8 * (1 - t))",
                 "c" + alpha_value + "-sqrt(t)"]

results_file = open('result.txt', 'r')

real_values = []
imag_values = []

for line in results_file:

    values = line.split()

    real_values.append(float(values[0]))
    imag_values.append(float(values[1]))

if remove_last == 1:

    real_values.pop()
    imag_values.pop()

if label_index >= 17:
    max_x = real_values[-1]
    max_y = real_values[-1]
    angle = arctan2(max_y , max_x) / pi
    alpha_data = [alpha_value, str(angle)]
    plt.axis((-5,5,0,6))

partial_filename = "output/" + all_filenames[label_index]

# plt.figure(figsize=(4.5, 3))

plt.title(all_labels[label_index],fontsize = 12, color='black', y = 1.02)
plt.plot(real_values,imag_values)
# plt.axis('equal')
plt.savefig(partial_filename + ".png")

exit()

plt.cla()
plt.title(all_labels[label_index],fontsize = 14, color='black', y = 1.03)
plt.scatter(real_values,imag_values)
plt.savefig(partial_filename + " [scatter].png")
# plt.axis('equal')
