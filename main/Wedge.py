import sys
sys.path.append('PythonTools')
from LoewnerRunFactory import LoewnerRunFactory
from Constants import HALF_PI

# Set time parameters
start_time = 0
final_time = 10

# Set resolution parameters
outer_points = 500
inner_points = 10

# Set compilation and saving parameters
dont_compile_modules = False
save_plots = True
save_data = True

# Create a LoewnerRunFactory object
wedge_factory = LoewnerRunFactory(start_time, final_time, outer_points, inner_points, dont_compile_modules, save_plots, save_data)

# Instruct the factory to create LoewnerRun objects for the wedge evolution
wedge_runs = wedge_factory.create_wedge_runs()

# Run the wedge program for different values of alpha
for run in wedge_runs:
    run.wedge_growth(4/3)
    run.wedge_growth(HALF_PI)
    break
