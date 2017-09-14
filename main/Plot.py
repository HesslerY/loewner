import Constants
import matplotlib.pyplot as plt
from math import pi, degrees
from numpy import arctan2
from os.path import dirname, exists
from os import mkdir

plt.style.use('bmh')

class Plot:

    def __init__(self, driving_function, resolution_parameters, results):

        # Create list of real and imaginary values (removes last point)
        self.real_values = [result.real for result in results]
        self.imag_values = [result.imag for result in results]

        # Assign the plot title
        self.output_plot_title = Constants.PLOT_TITLE[driving_function]
    
        # Determine the output directory for the plot images
        self.output_plot_directory = "outputimages/" + str(driving_function) + "/"
        
        # Determine the partial filename for the plot images
        self.partial_output_filename = str(driving_function) + " " + "-".join([str(x) for x in resolution_parameters])
        
        # Display or save plot
        self.display = True
        
        # Assign the run paramters
        self.resolution_parameters = resolution_parameters
        
    def create_output_folder(self):
        
        image_directory = dirname(self.output_plot_directory)
        
        if not exists(image_directory):
            mkdir(image_directory)
        
    def generate_plot(self):

        # Set the plot title
        plt.title(self.output_plot_title, fontsize = 19, color = "black", y = 1.02, usetex = True)
        
        # Plot the values
        plt.plot(self.real_values, self.imag_values)

        if self.display:
            plt.show()
            
        else:
            self.create_output_folder()
            plt.savefig(self.output_plot_directory + self.partial_output_filename + ".png")

    def generate_scatter_plot(self):
        pass
