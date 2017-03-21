import matplotlib.pyplot as plt

data_dir = ""
counter = 0
all_colours = ["b", "g", "r", "c", "m", "y", "k"]

def set_data_dir(directory):
    global data_dir
    data_dir = directory

def file_to_plot(filename, label, remove_last = False):

    global counter
    global data_dir
    full_filename = data_dir + filename

    try:
        data_file = open(full_filename, "r")
    except FileNotFoundError:
        print("This file " + full_filename + " does not exist.")
        return

    real_values = []
    imag_values = []
    
    for line in data_file:

        loewner_data = line.split()

        real_values.append(float(loewner_data[0]))
        imag_values.append(float(loewner_data[1]))

    if remove_last:
        real_values.pop()
        imag_values.pop()

    plt.plot(real_values, imag_values, label=label, color=all_colours[counter])
    counter += 1

def show_plot():
    plt.legend(loc = 0)
    plt.show()
    reset_counter()

def reset_counter():
    global counter
    counter = 0
