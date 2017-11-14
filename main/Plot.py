import Constants
import matplotlib.pyplot as plt
from math import pi, degrees
from numpy import arctan2
from os.path import dirname, exists
from os import mkdir

plt.style.use('seaborn')

class Plot:

    def __init__(self, driving_function, resolution_parameters, results, plot_dir = None):

        self.results = results
        self.driving_function = driving_function
        # Assign the plot title
        self.output_plot_title = Constants.PLOT_TITLE[driving_function]

        if plot_dir is None:
            self.display == True

        else:
            # Determine the output directory for the plot images
            self.output_plot_directory = plot_dir

            # Determine the partial filename for the plot images
            self.partial_output_filename = str(driving_function) + " " + "-".join([str(x) for x in resolution_parameters])

            # Display or save plot
            self.display = False

        # Assign the run paramters
        self.resolution_parameters = resolution_parameters

    def generate_plot(self):

        # Plot the values
        plt.plot(self.results.real, self.results.imag, color='crimson')

        sqrtdr = [i for i in range(2,9)]

        if not self.display:

            plt.ylim(bottom=0)

            if self.driving_function not in sqrtdr:

                plt.title(self.output_plot_title, fontsize = 19, color = "black", y = 1.02, usetex = True)

                if self.driving_function == 0:
                    plt.xticks(self.results.real, ["","","0","",""])

                plt.xlabel('Re(g)')
                plt.ylabel('Im(g)')

            else:
                plt.xticks([])
                plt.yticks([])

            plt.savefig(self.output_plot_directory + self.partial_output_filename + ".pdf")
            plt.cla()

        else:

            # Set the plot title
            plt.title(self.output_plot_title, fontsize = 19, color = "black", y = 1.02, usetex = True)
            plt.show()

    def generate_scatter_plot(self):
        pass
