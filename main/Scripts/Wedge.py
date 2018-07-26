import sys
sys.path.append('../PythonTools')
from LoewnerRunFactory import LoewnerRunFactory
from Constants import HALF_PI

start_time = 0
final_time = 15

outer_points = 50
inner_points = 10

dont_compile_modules = False
save_plots = True
save_data = True

wedge_factory = LoewnerRunFactory(start_time, final_time, outer_points, inner_points, dont_compile_modules, save_plots, save_data)
wedge_runs = wedge_factory.create_standard_runs()

for run in wedge_runs:
    run.wedge_growth(HALF_PI)
