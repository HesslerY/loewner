import sys
sys.path.append('PythonTools')
from LoewnerRunFactory import LoewnerRunFactory

start_time = 0
final_time = 5

outer_points = 1000
inner_points = 1

dont_compile_modules = False
save_plots = True
save_data = True

finger_factory = LoewnerRunFactory(start_time, final_time, outer_points, inner_points, dont_compile_modules, save_plots, save_data)
finger_runs = finger_factory.create_standard_runs()

for run in finger_runs:
    run.finger_growth()

