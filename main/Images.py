from LoewnerRun import LoewnerRun, SqrtLoewnerRun, ExactLoewnerRun
from InverseRun import InverseRun
import Constants
from Plot import Plot, MultiPlot, InversePlot, MiniPlot, InverseMultiPlot
from numpy import savetxt, column_stack, full_like

output_dir = "/home/dolica/Documents/writeuploewner/finalreport/data/"

def create_loewner_runs():

    loewner_runs = []

    for driving_function in range(Constants.TOTAL_DRIVING_FUNCTIONS):

        if not Constants.squareroot_driving(driving_function):
            loewner_runs.append(LoewnerRun(driving_function))
            loewner_runs[-1].final_time = 25
            loewner_runs[-1].start_time = 0
            loewner_runs[-1].total_points = 1000

    return loewner_runs

def create_kappa_runs():

    loewner_runs = []
    kappas = [i + 0.5 for i in range(1,10)]

    for kappa in kappas:
        loewner_runs.append(SqrtLoewnerRun(10))
        loewner_runs[-1].final_time = 1
        loewner_runs[-1].start_time = 0
        loewner_runs[-1].total_points = 1000
        loewner_runs[-1].sqrt_param = kappa

    return loewner_runs

def create_calpha_runs():

    loewner_runs = []
    alphas = [i * 0.1 for i in range(1,10)]

    for alpha in alphas:
        loewner_runs.append(SqrtLoewnerRun(11))
        loewner_runs[-1].final_time = 25
        loewner_runs[-1].start_time = 0
        loewner_runs[-1].total_points = 1000
        loewner_runs[-1].sqrt_param = alpha

    return loewner_runs

loewner_runs = create_loewner_runs()
kappa_runs = create_kappa_runs()
calpha_runs = create_calpha_runs()

filename_end = ".csv"

def sqrt_to_string(sqrt):

    return str(sqrt)[:3].replace(".","point")

def generate_properties(loewner):

    return [loewner.driving_function, loewner.start_time, loewner.final_time, loewner.total_points]

def properties_string(properties):

    desc = [str(attr) for attr in properties]
    return "-".join(desc)

def create_csv(loewner_run):

    data = loewner_run.results
    filename = output_dir + properties_string(generate_properties(loewner_run)) + filename_end

    real_vals = data.real
    imag_vals = data.imag

    combined = column_stack((real_vals,imag_vals))
    savetxt(filename, combined, fmt="%.18f")

def shift(real_vals):

    offset = full_like(real_vals,real_vals[0])
    return real_vals - offset

def sqrt_create_csv(loewner_run):

    data = loewner_run.results
    sqrt = loewner_run.sqrt_param

    param = "-" + sqrt_to_string(sqrt)
    filename = output_dir + properties_string(generate_properties(loewner_run)) + param + filename_end

    real_vals = data.real
    imag_vals = data.imag

    if loewner_run.driving_function == 10:
        real_vals = shift(real_vals)

    combined = column_stack((real_vals,imag_vals))
    savetxt(filename, combined, fmt="%.18f")

def inv_create_csv(time,driving,properties):

    filename = output_dir + properties_string(properties) + "-inv" + filename_end
    combined = column_stack((time,driving))
    savetxt(filename, combined, fmt="%.18f")

def sqrt_inv_create_csv(time,driving,properties,sqrt_param):

    filename = output_dir + properties_string(properties) + "-" + sqrt_to_string(sqrt_param) + "-inv" + filename_end
    combined = column_stack((time,driving))
    savetxt(filename, combined, fmt="%.18f")

for run in loewner_runs:

    run.perform_loewner()
    df = run.driving_function
    res = [run.start_time, run.final_time, run.total_points]
    points = run.results

    create_csv(run)

    inverse_loewner = InverseRun(df,points,res)
    inverse_loewner.perform_inverse()

    time_arr = inverse_loewner.time_arr
    driving_arr = inverse_loewner.driving_arr

    inv_create_csv(time_arr,driving_arr,[df] + res)

constant_final_times = [1,4,9,16]
constant_run = loewner_runs[0]

for final in constant_final_times:

    constant_run.final_time = final
    constant_run.perform_loewner()
    create_csv(constant_run)

for run in kappa_runs:

    run.perform_loewner()
    df = run.driving_function
    res = [run.start_time, run.final_time, run.total_points]
    points = run.results
    sqrt_param = run.sqrt_param

    sqrt_create_csv(run)

    inverse_loewner = InverseRun(df,points,res)
    inverse_loewner.perform_inverse()

    time_arr = inverse_loewner.time_arr
    driving_arr = inverse_loewner.driving_arr

    sqrt_inv_create_csv(time_arr,driving_arr,[df] + res,sqrt_param)

for run in calpha_runs:

    run.perform_loewner()
    df = run.driving_function
    res = [run.start_time, run.final_time, run.total_points]
    points = run.results
    sqrt_param = run.sqrt_param

    sqrt_create_csv(run)

    inverse_loewner = InverseRun(df,points,res)
    inverse_loewner.perform_inverse()

    time_arr = inverse_loewner.time_arr
    driving_arr = inverse_loewner.driving_arr

    sqrt_inv_create_csv(time_arr,driving_arr,[df] + res,sqrt_param)

