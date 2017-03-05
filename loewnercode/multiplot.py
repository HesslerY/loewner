import matplotlib.pyplot as plt
from sys import argv

# List of colour options for each of the different plots
colour_options = ["b","g","r","k","m"]

# Label of number of iterations for each of the different plots
labels = ["100","1000","10000","100000","200000"]

# Iterate over the results files
for i in range(5):

    # Obtain the filename and open the file
    filename = "multiple/" + str(i) + ".txt"
    result_file = open(filename,"r")
    
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
    
    # Remove the first value in both lists
    real_values.pop(0)
    imag_values.pop(0)

    # Create a plot
    plt.plot(real_values,imag_values,colour_options[i],label=labels[i])

# Show the plot legend
plt.legend()

# Force equal axes
plt.axis('equal')

# Show the plot
plt.show()
