import sys
sys.path.append('PythonTools')
from Constants import CONST_IDX, LINR_IDX, KAPPA_IDX, CALPHA_IDX, SQRTPLUS_IDX
from LoewnerRunFactory import LoewnerRunFactory

# Declare final time for Loewner runs
start_time = 0
cubic_final_time = 10
outer_points = 1000
inner_points = 10
compile_modules = True
save_plot = True
save_data = True

# Create lists of kappa and alpha values
kappas = [i + 0.5 for i in range(1,10)]
alphas = [i * 0.1 for i in range(1,10)]

# Make a LoewnerRunFactory
cubic_factory = LoewnerRunFactory(start_time, cubic_final_time, outer_points, inner_points, compile_modules, save_plot, save_data)

# Create a list of cubic runs
cubic_runs = cubic_factory.create_standard_runs() + cubic_factory.vary_kappa(kappas) + cubic_factory.vary_alpha(alphas) + [cubic_factory.select_single_run(index=CONST_IDX,constant=1)]

# Solve the cubic runs
for run in cubic_runs:

    print("Starting cubic forward for driving function " + str(run.name))
    run.cubic_forward_loewner()
    print("Finished cubic forward for driving function " + str(run.name))

    if run.index == KAPPA_IDX:
        print("Finished cubic forward for kappa = " + str(run.kappa)[:3])

# Create a list of cubic runs for which there is an exact solution
exact_cubic_runs = cubic_factory.create_exact_cubic()

# Solve for the exact solution
for run in exact_cubic_runs:

    run.exact_cubic_forward_loewner()
    print("Finished exact cubic forward for driving function " + str(run.name))
