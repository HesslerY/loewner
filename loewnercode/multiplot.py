import matplotlib.pyplot as plt
from sys import argv

# List of colour options for each of the different plots
colour_options = ["b", "g", "r", "c", "m", "y", "k"]

iterations_file = open("iterations.txt","r")
labels = []

for line in iterations_file:
    labels.append(line[:-1])

all_titles = ["$\\xi (t) = 0$",
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
              "$\\xi (t) = 2 \ \sqrt{8 \ (1 - t)}$"]

title_index = int(argv[1])

dir_name = "backup/" + str(title_index) + "/"

plt.title(all_titles[title_index],fontsize = 18, color='black', y = 1.03)

# Iterate over the results files
for i in range(len(labels)):

    # Obtain the filename and open the file
    try:
        filename = dir_name + str(labels[i]) + ".txt"
        result_file = open(filename,"r")
        print("Opened a file!")

    except FileNotFoundError:
        print("Unable to open " + filename)
        break
    
    # Create empty lists
    real_values = []
    imag_values = []
    
    # Read the values in the file
    for line in result_file:

        values = line.split()

        real_values.append(float(values[0]))
        imag_values.append(float(values[1]))
        
    # Remove the last value in both lists
    real_values.pop()
    imag_values.pop()

    # Create a plot
    plt.plot(real_values,imag_values,colour_options[i],label=labels[i])

# Show the plot legend
plt.legend()

# Force equal axes
plt.axis('equal')

# Show the plot
plt.show()
