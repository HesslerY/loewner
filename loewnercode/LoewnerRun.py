from numpy import empty
from Plot import Plot
from importlib import import_module

class LoewnerRun:

    def __init__(self, loewner_config):

        # Assign the LoewnerConfig object
        self.loewner_config = loewner_config

        self.driving_function = self.loewner_config.driving_function
        self.run_params = self.loewner_config.run_params
        self.sqrt_param = loewner_config.sqrt_param

        self.results = self.perform_loewner(*self.run_params)
        self.create_plot()

    def import_loewner(self):

        # Try to import the corresponding module
        return import_module("modules.NumericalLoewner_" + str(self.driving_function))

    def perform_loewner(self, start_point, end_point, n_points):

        try:

            # Check if the module can be imported successfully
            NumericalLoewner = self.import_loewner()

        except ModuleNotFoundError:

            self.loewner_config.compile_loewner()
            NumericalLoewner = self.import_loewner()


        g_arr = empty(n_points, dtype=complex)

        if not self.loewner_config.exact_mode:
            if not self.sqrt_param:
                NumericalLoewner.loewners_equation(start_point, end_point, g_arr)
            else:
                NumericalLoewner.loewners_equation(start_point, end_point, g_arr, self.sqrt_param)
        else:
            NumericalLoewner.linear_driving(start_point, n_points, g_arr)

        return g_arr

    def create_plot(self):

        if not self.sqrt_param:
            plot = Plot(self.driving_function, self.run_params, self.results)

        else:
            plot = Plot(self.driving_function, self.run_params, self.results, self.sqrt_param)

        plot.generate_plot()
