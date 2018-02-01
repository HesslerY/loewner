from LoewnerRun import LoewnerRun, ExactLoewnerRun
from Plot import MultiPlot
import matplotlib.pyplot as plt
from numpy import savetxt, column_stack, full_like, linspace, empty, absolute
from math import sqrt
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

def read_exact_sol():

    exact_data = open("/home/dolica/Documents/writeuploewner/finalreport/data/1-0-25-1000-exact.csv","r")
    exact_sol = empty(res[-1],dtype=complex)

    i = 0

    for line in exact_data.readlines():
        values = line.split()
        huhhh = float(values[0])
        exact_sol[i] = float(values[0]) + (float(values[1]) * 1j)

        i += 1

    return exact_sol

def root_mean_squared_error(exact_sol, approx_sol):

    approx_res = len(approx_sol)

    approx_t = linspace(0,25,approx_res)

    rms = 0
    incr = 1000/(approx_res - 1)

    rms += absolute(approx_sol[0] - exact_sol[0]) ** 2

    for i in range(1,approx_res):

        diff = (approx_sol[i] - exact_sol[int(incr * i) - 1])
        rms += absolute(diff) ** 2

    return sqrt(rms/approx_res)

output_dir = "/home/dolica/Documents/writeuploewner/finalreport/data/"
exact_results = []

res = [5, 10, 50, 100, 500, 1000]

df = 1
loewner_run = LoewnerRun(1)
loewner_run.start_time = 0
loewner_run.final_time = 25

approx_results = []

for total_points in res:

    loewner_run.total_points = total_points
    loewner_run.perform_loewner()
    create_csv(loewner_run)
    approx_results.append(loewner_run.results)

exact_sol = read_exact_sol()
print(exact_sol[-5:])

print("Root mean squared error:")
for approx_run in approx_results:
    print(root_mean_squared_error(exact_sol,approx_run))

