import sys
sys.path.append('PythonTools')
from Constants import CONST_IDX, LINR_IDX, KAPPA_IDX, CALPHA_IDX, SQRTPLUS_IDX
from LoewnerRunFactory import LoewnerRunFactory

# Declare final time for Loewner runs
start_time = 0
final_time = 25
outer_points = 1000
inner_points = 10
compile_modules = True
save_plot = False
save_data = True

# Make a LoewnerRunFactory
loewner_factory = LoewnerRunFactory(start_time, final_time, outer_points, inner_points, compile_modules, save_plot, save_data)

# Observing how xi(t) = 0 relates to sqrt(final_time)
constantdf_time_runs = loewner_factory.vary_final_time(index=CONST_IDX,constant=0,times=[1,4,9,16])

# Run xi(t) = 0 with different final time values
for run in constantdf_time_runs:
    run.quadratic_forward_loewner()
    print("Finished quadratic forward for driving function " + str(run.name) + " with final time " + str(run.final_time))
