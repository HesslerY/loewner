import sys
sys.path.append('PythonTools')
from Constants import CONST_IDX, LINR_IDX, KAPPA_IDX, CALPHA_IDX, SQRTPLUS_IDX
from LoewnerRunFactory import LoewnerRunFactory
from math import pi

# Declare final time for Loewner runs
start_time = 0
final_time = 25
outer_points = 1000
inner_points = 10
compile_modules = False
save_plot = True
save_data = True

# Make a LoewnerRunFactory
loewner_factory = LoewnerRunFactory(start_time, final_time, outer_points, inner_points, compile_modules, save_plot, save_data)

# Create list of single-trace runs for which there is a known exact solution
exact_quadratic_runs = loewner_factory.create_exact_quadratic_forward()

# Change resolution to compare xi(t) = t to exact solution
linear_exact_solution_comp = loewner_factory.vary_inner_res(index=LINR_IDX,points=[5,50,100,200,300,400,500])

# Find the exact solutions for the single-traces
for run in exact_quadratic_runs:
    run.exact_quadratic_forward_loewner()
    print("Finished exact quadratic forward for driving function = " + str(run.name))

exact_quadratic_runs[0].phi_quadratic_exact(0,pi)

# Vary the resolution for xi(t) = t (in order to compare to exact solution)
for run in linear_exact_solution_comp:
    run.quadratic_forward_loewner()
    print("Finished quadratic forward for driving function " + str(run.name) + " with inner res of " + str(run.inner_points))

