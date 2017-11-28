import Constants
import matplotlib.pyplot as plt
from math import pi, degrees
from numpy import arctan2,array
from os.path import dirname, exists
from os import mkdir
import matplotlib.ticker as ticker

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

        periodic_driving = [i for i in range(2,10)]

        ax = plt.axes()

        if not self.display:

            plt.ylim(bottom=0)

            if self.driving_function not in periodic_driving:

                plt.title(self.output_plot_title, fontsize = 19, color = "black", y = 1.02, usetex = True)

                plt.xlabel('Re(g)')
                plt.ylabel('Im(g)')

                if self.driving_function == 0:
                    plt.xticks([-2,0,2])

                if self.driving_function == 12:
                    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))

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

class MultiPlot(Plot):

    def __init__(self, driving_function, resolution_parameters, results_arr, plot_dir = None):

        self.multi_result = results_arr

        Plot.__init__(self,driving_function,resolution_parameters,[],plot_dir)

        if driving_function == 10:
            self.output_plot_title = "$\\xi (t) = 2 \ \sqrt{ \kappa \ (1 - t)}$"
            self.shift_results()

        elif driving_function == 11:
            self.output_plot_title = "$\\xi (t) = c_{\\alpha} \sqrt{t}$",

    def shift_results(self):

        for result in self.multi_result:

            offset = result[0].real

            for i in range(len(result)):

                result[i] = result[i] - offset

            plt.plot(result.real, result.imag)

    def generate_plot(self):

        ax = plt.axes()

        if not self.display:

            plt.ylim(bottom=0)

            plt.title(self.output_plot_title, fontsize = 19, color = "black", y = 1.02, usetex = True)

            plt.xlabel('Re(g)')
            plt.ylabel('Im(g)')

            plt.savefig(self.output_plot_directory + self.partial_output_filename + ".pdf")
            plt.cla()

        else:

            # Set the plot title
            plt.title(self.output_plot_title, fontsize = 19, color = "black", y = 1.02, usetex = True)
            plt.show()

