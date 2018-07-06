from LoewnerRun import LoewnerRun, ExactLoewnerRun
from Plot import MultiPlot
import matplotlib.pyplot as plt
from numpy import savetxt, column_stack, full_like, linspace, empty, absolute, complex128
from math import sqrt
# Exact solution for xi(t) = t

filename_end = ".csv"
MAX_RES = 1000

def generate_properties(loewner):

    return [loewner.driving_function, loewner.start_time, loewner.final_time, loewner.outer_points, loewner.inner_points]

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

inner_res = [5, 10, 50, 100, 200, 300, 400, 500]

df = 1
loewner_run = LoewnerRun(df)
loewner_run.start_time = 0
loewner_run.final_time = 25
loewner_run.outer_points = 1000

for inner_points in inner_res:

    loewner_run.inner_points = inner_points
    loewner_run.perform_loewner()
    create_csv(loewner_run)

