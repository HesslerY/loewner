import matplotlib.pyplot as plt
from math import pi, degrees
from numpy import arctan2
from time import gmtime, strftime
from os.path import dirname, exists
from os import mkdir
import Constants

plt.style.use('ggplot')

class Plot:

    def __init__(self, driving_func_index, remove_last_point = True, input_filename = "result.txt"):

        # Create empty lists for plot points
        self.real_values = []
        self.imag_values = []
        
        # Assign the results data filename
        self.input_filename = input_filename
        
        # Assign figsize
        # self.fig_size = fig_size
        
        # Assign the plot title
        self.output_plot_title = Constants.DRIVING_INFO[driving_func_index][1]
    
        # Determine the output directory for the plot images
        self.output_plot_directory = "output/" + strftime("%m-%d-%y", gmtime())
        
        # Determine the partial filename for the plot images
        self.partial_output_filename = str(driving_func_index)
        
        # Save rather than display plot
        self.display = True
        
        # Remove last point before plotting
        self.remove_last_point = True

    def read_file(self):

        # Open the data file
        data_file = open(self.input_filename, 'r')

        # Convert the values to float
        for line in data_file:

            values = line.split()

            self.real_values.append(float(values[0]))
            self.imag_values.append(float(values[1]))

        # Deletes last point from the results
        if self.remove_last_point:

            self.real_values.pop()
            self.imag_values.pop()
            
    def create_output_folder(self):
        
        image_directory = dirname(self.output_plot_directory)
        
        if not exists(image_directory):
            mkdr(image_directory)
        
    def generate_plot(self):
    
        # Clear the plot
        plt.cla()

        # Set the plot title
        plt.title(self.output_plot_title, fontsize = 12, color="black", y = 1.02)
        
        # Plot the values
        plt.plot(self.real_values, self.imag_values)
        
        # if self.equal_axes:
            # plt.axis("equal")
            
        # elif fig_size is not None:
            # plt.figsize(self.fig_size)

        if self.display:
            plt.show()
            
        else:
            self.create_output_folder()
            plt.savefig(self.output_plot_directory + self.partial_output_filename + ".png")

    def generate_scatter_plot(self):
        pass
        
        # Clear the plot
        # plt.cla()
        # plt.title(all_labels[label_index],fontsize = 14, color='black', y = 1.03)
        # plt.scatter(real_values,imag_values)
        # plt.savefig(partial_filename + " [scatter].png")
        # plt.axis('equal')
