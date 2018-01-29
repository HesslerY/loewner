from LoewnerRun import LoewnerRun, ExactLoewnerRun
from Plot import MultiPlot
import matplotlib.pyplot as plt
from numpy import savetxt, column_stack, full_like
# Exact solution for xi(t) = t

filename_end = ".csv"

def generate_properties(loewner):

    return [loewner.driving_function, loewner.start_time, loewner.final_time, loewner.total_points]

def properties_string(properties):

    desc = [str(attr) for attr in properties]
    return "-".join(desc)

def create_csv(loewner_run,label=None):

    data = loewner_run.results
    filename = output_dir + properties_string(generate_properties(loewner_run))

    val = len(output_dir)

    if bool(label):

        filename = filename[:val + 4] + filename[val + 9:]
        filename = filename + "-" + label

    filename = filename + filename_end

    real_vals = data.real
    imag_vals = data.imag

    combined = column_stack((real_vals,imag_vals))
    savetxt(filename, combined, fmt="%.18f")

output_dir = "/home/dolica/Documents/writeuploewner/finalreport/data/"
exact_results = []

exact_run = ExactLoewnerRun(1)
exact_run.start_time = 0
exact_run.final_time = 25
# exact_run.total_points = 500
exact_run.total_points = 1000
exact_run.perform_loewner()
res = [5]

exact_run.results = exact_run.results[:-10]
create_csv(exact_run,"exact")

for i in range(3):
    res.append(res[-1] * 2)

df = 1
loewner_run = LoewnerRun(1)
loewner_run.start_time = 0
# loewner_run.final_time = 108
loewner_run.final_time = 25

for total_points in res:

    loewner_run.total_points = total_points
    loewner_run.perform_loewner()
    create_csv(loewner_run)

