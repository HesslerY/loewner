import sys
sys.path.append('../PythonTools')
from Constants import CONST_IDX, LINR_IDX, KAPPA_IDX, CALPHA_IDX, SQRTPLUS_IDX
from LoewnerRunFactory import LoewnerRunFactory

# Declare final time for Loewner runs
start_time = 0
final_time = 25
outer_points = 1000
inner_points = 10
compile_modules = True
save_plot = True
save_data = True

kappas = [i + 0.5 for i in range(1,10)]
alphas = [i * 0.1 for i in range(1,10)]

# Make a LoewnerRunFactory
loewner_factory = LoewnerRunFactory(start_time, final_time, outer_points, inner_points, compile_modules, save_plot, save_data)

# Create three lists of LoewnerRuns
standard_runs = loewner_factory.create_standard_runs()

# Observing how xi(t) = 0 relates to sqrt(final_time)
constantdf_time_runs = loewner_factory.vary_final_time(index=CONST_IDX,constant=0,times=[1,4,9,16])

# Exact solution for xi(t) = t
exact_quadratic_runs = loewner_factory.create_exact_quadratic_forward()

# Change resolution to compare xi(t) = t to exact solution
linear_exact_solution_comp = loewner_factory.vary_inner_res(index=LINR_IDX,points=[5,50,100,200,300,400,500])

# Kappa and calpha
kappa_runs = loewner_factory.vary_kappa(kappas,inner_points=2000)
calpha_runs = loewner_factory.vary_alpha(alphas)

for run in standard_runs:

    run.quadratic_forward_loewner()
    print("Finished quadratic forward for driving function " + str(run.name))

    run.quadratic_inverse_loewner()
    print("Finished quadratic inverse for driving function " + str(run.name))

for run in constantdf_time_runs:
    run.quadratic_forward_loewner()
    print("Finished quadratic forward for driving function " + str(run.name) + " with final time " + str(run.final_time))

for run in linear_exact_solution_comp:
    run.quadratic_forward_loewner()
    print("Finished quadratic forward for driving function " + str(run.name) + " with inner res of " + str(run.inner_points))

for run in kappa_runs:

    run.quadratic_forward_loewner()
    print("Finished quadratic forward for kappa = " + str(run.kappa)[:3])

    run.quadratic_inverse_loewner()
    print("Finished quadratic inverse for kappa = " + str(run.kappa)[:3])

for run in calpha_runs:

    run.quadratic_forward_loewner()
    print("Finished quadratic forward for alpha = " + str(run.alpha)[:3])

    run.quadratic_inverse_loewner()
    print("Finished quadratic inverse for alpha = " + str(run.alpha)[:3])

exact_quadratic_runs = loewner_factory.create_exact_quadratic_forward()

for run in exact_quadratic_runs:

    run.exact_quadratic_forward_loewner()
    print("Finished exact quadratic forward for driving function = " + str(run.name))


# Make a LoewnerRunFactory
cubic_final_time = 10
cubic_factory = LoewnerRunFactory(start_time, cubic_final_time, outer_points, inner_points, compile_modules, save_plot, save_data)

cubic_runs = cubic_factory.create_standard_runs() + cubic_factory.vary_kappa(kappas) + cubic_factory.vary_alpha(alphas) + [cubic_factory.select_single_run(index=CONST_IDX,constant=1)]

for run in cubic_runs:

    print("Starting cubic forward for driving function " + str(run.name))
    run.cubic_forward_loewner()
    print("Finished cubic forward for driving function " + str(run.name))

    if run.index == KAPPA_IDX:
        print("Finished cubic forward for kappa = " + str(run.kappa)[:3])

exact_cubic_runs = cubic_factory.create_exact_cubic()

for run in exact_cubic_runs:

    run.exact_cubic_forward_loewner()
    print("Finished exact cubic forward for driving function " + str(run.name))

