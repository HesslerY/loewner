import sys
sys.path.append('../PythonTools')
from Constants import CONST_IDX, LINR_IDX, KAPPA_IDX, CALPHA_IDX, SQRTPLUS_IDX
from LoewnerRunFactory import LoewnerRunFactory

# Declare final time for Loewner runs
start_time = 0
final_time = 25
outer_points = 1000
inner_points = 10
compile_modules = False
save_plot = True
save_data = True

kappas = [i + 0.5 for i in range(1,10)]
alphas = [i * 0.1 for i in range(1,10)]

# Make a LoewnerRunFactory
loewner_factory = LoewnerRunFactory(start_time, final_time, outer_points, inner_points, compile_modules, save_plot, save_data)

# Create three lists of LoewnerRuns
standard_runs = loewner_factory.create_standard_runs()

# Kappa and calpha
kappa_runs = loewner_factory.vary_kappa(kappas,inner_points=2000)
calpha_runs = loewner_factory.vary_alpha(alphas)

# Carry out the 'standard' runs (drving functions for which there are no extra parameters)
for run in standard_runs:

    run.quadratic_forward_loewner()
    print("Finished quadratic forward for driving function " + str(run.name))

    run.quadratic_inverse_loewner()
    print("Finished quadratic inverse for driving function " + str(run.name))

    run.exact_quadratic_inverse()
    print("Finished exact quadratic inverse for driving function " + str(run.name))

# Carry out the kappa runs
for run in kappa_runs:

    run.quadratic_forward_loewner()
    print("Finished quadratic forward for kappa = " + str(run.kappa)[:3])

    run.quadratic_inverse_loewner()
    print("Finished quadratic inverse for kappa = " + str(run.kappa)[:3])

    run.exact_quadratic_inverse()
    print("Finished exact quadratic inverse for kappa = " + str(run.kappa)[:3])

# Carry out the calpha runs
for run in calpha_runs:

    run.quadratic_forward_loewner()
    print("Finished quadratic forward for alpha = " + str(run.alpha)[:3])

    run.quadratic_inverse_loewner()
    print("Finished quadratic inverse for alpha = " + str(run.alpha)[:3])

    run.exact_quadratic_inverse()
    print("Finished exact quadratic inverse for alpha = " + str(run.alpha)[:3])

