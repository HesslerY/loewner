import sys
sys.path.append('../PythonTools')
from LoewnerRunFactory import LoewnerRunFactory
from Constants import HALF_PI

start_time = 0
final_time = 10

outer_points = 500
inner_points = 2

dont_compile_modules = False
save_plots = True
save_data = True

wedge_factory = LoewnerRunFactory(start_time, final_time, outer_points, inner_points, dont_compile_modules, save_plots, save_data)
wedge_runs = [wedge_factory.select_single_run(0,constant=1)] + wedge_factory.create_standard_runs()

not_good_ones = [3,4,5,7,8,9,12,13]

for i in not_good_ones:
    run = wedge_factory.select_single_run(index=i,outer_points=5000,inner_points=1)
    run.wedge_growth(4/3)

for run in wedge_runs:
    run.wedge_growth(4/3)
    run.wedge_growth(HALF_PI)
    break
