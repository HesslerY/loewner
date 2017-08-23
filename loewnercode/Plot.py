import matplotlib.pyplot as plt
from math import pi, degrees
from numpy import arctan2
from os.path import dirname, exists
from os import mkdir
import Constants

plt.style.use('ggplot')

class Plot:

    def __init__(self, driving_func_index, run_params, results, sqrt_param = None, remove_last_point = True):

        # Create empty lists for plot points
        self.real_values = [result.real for result in results]
        self.imag_values = [result.imag for result in results]
        
        # Assign the plot title
        self.output_plot_title = self.generate_plot_title(driving_func_index, sqrt_param)
    
        # Determine the output directory for the plot images
        self.output_plot_directory = "outputimages/" + str(driving_func_index) + "/"
        
        # Determine the partial filename for the plot images
        self.partial_output_filename = str(driving_func_index) + " " + "-".join([str(x) for x in run_params])
        
        # Display or save plot
        self.display = True
        
        # Remove last point before plotting
        self.remove_last_point = True
        
        # Assign the run paramters
        self.run_params = run_params
        
    def generate_plot_title(self, driving_func_index, sqrt_param):
    
        if driving_func_index not in [Constants.KAPPA_IDX, Constants.C_ALPHA_IDX]:
            return Constants.DRIVING_INFO[driving_func_index][1]
            
        return Constants.DRIVING_INFO[driving_func_index][1].replace("SQRT_PARAM", sqrt_param)

    def create_output_folder(self):
        
        image_directory = dirname(self.output_plot_directory)
        
        if not exists(image_directory):
            mkdir(image_directory)
        
    def generate_plot(self):

        # Set the plot title
        plt.title(self.output_plot_title, fontsize = 14, color = "black", y = 1.02, usetex = True)
        
        # Plot the values
        plt.plot(self.real_values, self.imag_values)

        if self.display:
            plt.show()
            
        else:
            self.create_output_folder()
            plt.savefig(self.output_plot_directory + self.partial_output_filename + ".png")

    def generate_scatter_plot(self):
        pass
