import Constants
import matplotlib.pyplot as plt
from math import pi, degrees
from numpy import arctan2,array
from os.path import dirname, exists
from os import mkdir
import matplotlib.ticker as ticker
from matplotlib import rc

plt.style.use('seaborn')
rc('lines', linewidth=1.0)

class Plot:

    def __init__(self, driving_function, resolution_parameters, results, plot_dir = None):

        self.results = results
        self.driving_function = driving_function

        # Assign the plot title
        self.output_plot_title = Constants.PLOT_TITLE[driving_function]

        self.plot_dir = plot_dir

        if bool(self.plot_dir):

            # Determine the partial filename for the plot images
            self.partial_output_filename = str(driving_function) + "-" + "-".join([str(x) for x in resolution_parameters])

        # Assign the run paramters
        self.resolution_parameters = resolution_parameters

    def generate_plot(self):

        # Plot the values
        plt.plot(self.results.real, self.results.imag, color='crimson')

        periodic_driving = [i for i in range(2,10)]

        ax = plt.axes()

        if bool(self.plot_dir):

            plt.ylim(bottom=0)

            if self.driving_function not in periodic_driving:

                plt.title(self.output_plot_title, fontsize = 19, color = "black", y = 1.02, usetex = True)

                plt.xlabel('Re($g$)')
                plt.ylabel('Im($g$)')

                if self.driving_function == 0:
                    plt.xticks([-2,0,2])

                    if self.resolution_parameters[1] is not 25:
                        plt.title("")

                if self.driving_function == 12:
                    ax.xaxis.set_major_locator(ticker.MultipleLocator(5))

            else:
                plt.xticks([])
                plt.yticks([])

            plt.savefig(self.plot_dir + self.partial_output_filename + ".pdf", bbox_inches='tight')
            plt.cla()

        else:

            # Set the plot title
            plt.title(self.output_plot_title, fontsize = 19, color = "black", y = 1.02, usetex = True)
            # plt.show()
            from matplotlib2tikz import save as tikz_save
            tikz_save('test.tex')

    def generate_scatter_plot(self):
        pass

class MiniPlot(Plot):

    def __init__(self, driving_function, resolution_parameters, results, plot_dir = None):

        self.results = results
        self.driving_function = driving_function

        # Assign the plot title
        self.output_plot_title = Constants.PLOT_TITLE[driving_function]

        self.plot_dir = plot_dir

        if bool(self.plot_dir):

            # Determine the partial filename for the plot images
            self.partial_output_filename = str(driving_function) + "-" + "-".join([str(x) for x in resolution_parameters]) + "-mini"

        # Assign the run paramters
        self.resolution_parameters = resolution_parameters

    def generate_plot(self):

        # Plot the values
        plt.plot(self.results.real, self.results.imag, color='crimson')

        if bool(self.plot_dir):

            plt.ylim(bottom=0)

            plt.xticks([])
            plt.yticks([])

            plt.savefig(self.plot_dir + self.partial_output_filename + ".pdf", bbox_inches='tight')
            plt.cla()

        else:

            # Set the plot title
            plt.title(self.output_plot_title, fontsize = 19, color = "black", y = 1.02, usetex = True)
            plt.show()

    def generate_scatter_plot(self):
        pass

class MultiPlot(Plot):

    def __init__(self, driving_function, resolution_parameters, results_arr, plot_dir = None, labels = None):

        self.multi_result = results_arr

        Plot.__init__(self,driving_function,resolution_parameters,[],plot_dir)

        if driving_function == 10:
            self.output_plot_title = "$\\xi (t) = 2 \ \sqrt{ \kappa \ (1 - t)}$"
            self.shift_results()

        elif driving_function == 11:
            self.output_plot_title = "$\\xi (t) = c_{\\alpha} \sqrt{t}$"

        self.labels = labels

        if bool(self.labels):

            self.partial_output_filename += "-exact"

    def shift_results(self):

        for result in self.multi_result:

            offset = result[0].real

            for i in range(len(result)):

                result[i] = result[i] - offset

    def generate_plot(self):

        if bool(self.labels):

            for result,label in zip(self.multi_result,self.labels):

                print(result.imag[-2])
                plt.plot(result.real, result.imag, label=label)

            plt.legend(loc=0)

        else:

            for result in self.multi_result:

                plt.plot(result.real, result.imag)

        if bool(self.plot_dir):

            plt.ylim(bottom=0)

            plt.title(self.output_plot_title, fontsize = 19, color = "black", y = 1.02, usetex = True)

            plt.xlabel('Re($g$)')
            plt.ylabel('Im($g$)')

            plt.savefig(self.plot_dir + self.partial_output_filename + ".pdf", bbox_inches='tight')
            plt.cla()

        else:

            # Set the plot title
            plt.title(self.output_plot_title, fontsize = 19, color = "black", y = 1.02, usetex = True)
            plt.show()

class InverseMultiPlot(Plot):

    def __init__(self, driving_function, resolution_parameters, results_arr, plot_dir = None):

        self.multi_inverse = results_arr
        Plot.__init__(self,driving_function,resolution_parameters,[],plot_dir)

        if driving_function == 10:
            self.output_plot_title = "$\\xi (t) = 2 \ \sqrt{ \kappa \ (1 - t)}$"

        elif driving_function == 11:
            self.output_plot_title = "$\\xi (t) = c_{\\alpha} \sqrt{t}$"

        self.partial_output_filename += "-inv"

    def generate_plot(self):

        for result in self.multi_inverse:
            plt.plot(result[0], result[1])

        if bool(self.plot_dir):

            plt.xlim(xmin=0)

            if self.driving_function == 10:
                plt.ylim(bottom=0)

            plt.title(self.output_plot_title, fontsize = 19, color = "black", y = 1.02, usetex = True)

            plt.xlabel('$t$')
            plt.ylabel(r'$\xi(t)$')

            plt.savefig(self.plot_dir + self.partial_output_filename + ".pdf", bbox_inches='tight')
            plt.cla()

        else:

            # Set the plot title
            plt.title(self.output_plot_title, fontsize = 19, color = "black", y = 1.02, usetex = True)
            plt.show()

class InversePlot(Plot):

    def __init__(self, driving_function, resolution_parameters, time_arr, driving_arr, plot_dir = None):

        Plot.__init__(self,driving_function,resolution_parameters,[],plot_dir)

        self.partial_output_filename = self.partial_output_filename + "-inv"

        self.time_arr = time_arr
        self.driving_arr = driving_arr

    def generate_plot(self):

        plt.plot(self.time_arr, self.driving_arr)

        if bool(self.plot_dir):

            plt.xlim(xmin=0)

            if self.driving_function is 1:
                plt.ylim(ymin=0)

            # plt.title(self.output_plot_title, fontsize = 19, color = "black", y = 1.02, usetex = True)

            plt.xticks([])
            plt.yticks([])

            plt.savefig(self.plot_dir + self.partial_output_filename + ".pdf", bbox_inches='tight')
            plt.cla()

        else:

            # Set the plot title
            plt.title(self.output_plot_title, fontsize = 19, color = "black", y = 1.02, usetex = True)
            plt.show()
