from numpy import empty
from Plot import Plot
import importlib

class LoewnerRun:

    def __init__(self, loewner_config):
    
        self.loewner_config = loewner_config
        
        self.driving_func_index = self.loewner_config.driving_func_index
        self.run_params = self.loewner_config.run_params
        self.sqrt_param = loewner_config.sqrt_param
        
        self.loewner_config.compile_loewner()
        
        self.results = self.perform_loewner(*self.run_params)
        self.create_plot()
        
    def perform_loewner(self, start_point, end_point, n_points):
    
        import NumericalLoewner
        NumericalLoewner = importlib.reload(NumericalLoewner)
    
        g_arr = empty(n_points, dtype=complex)
        NumericalLoewner.loewners_equation(start_point, end_point, g_arr)

        return g_arr
    
    def create_plot(self):
    
        if self.sqrt_param is None:
            plot = Plot(self.driving_func_index, self.run_params, self.results)

        else:
            plot = Plot(self.driving_func_index, self.run_params, self.results, self.sqrt_param)

        plot.generate_plot()
