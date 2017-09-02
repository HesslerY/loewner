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
        self.module_code = loewner_config.module_code

        self.results = self.perform_loewner(*self.run_params)
        self.create_plot()

    def import_loewner(self):

        # Try to import the corresponding module
        return import_module("modules.NumericalLoewner_" + self.module_code)

    def perform_loewner(self, start_point, end_point, n_points):

        try:

            # Check if the module can be imported successfully
            NumericalLoewner = self.import_loewner()

        except ModuleNotFoundError:

            self.loewner_config.compile_loewner()
            NumericalLoewner = self.import_loewner()

        g_arr = empty(n_points, dtype=complex)

        if not self.sqrt_param:
            NumericalLoewner.loewners_equation(start_point, end_point, g_arr)

        else:
            NumericalLoewner.loewners_equation(start_point, end_point, g_arr, self.sqrt_param)

        return g_arr

    def create_plot(self):

        if not self.sqrt_param:
            plot = Plot(self.driving_function, self.run_params, self.results)

        else:
            plot = Plot(self.driving_function, self.run_params, self.results, self.sqrt_param)

        plot.generate_plot()
