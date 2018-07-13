from importlib import import_module
from numpy import savetxt, column_stack, full_like, linspace, empty, absolute, complex128, copy
from math import sqrt
import matplotlib.pyplot as plt
import subprocess

start_time = 0
final_time = 25
outer_n = 1000
inner_n = 10

first_g_arr = empty(outer_n, dtype=complex128)
second_g_arr = empty(outer_n,  dtype=complex128)

kappas = [i + 0.5 for i in range(10)]
alphas = [i * 0.1 for i in range(1,10)]
nonSquareRootDriving = [i for i in range(10)] + [i for i in range(12,15)]

output_dir = "/home/dolica/Documents/writeuploewner/finalreport/data/"
MAX_RES = 500

def read_exact_sol():

    exact_data = []
    exact_data.append(open("/home/dolica/Documents/writeuploewner/finalreport/data/14-0-10-500-1-Cubic-Exact.csv","r"))
    exact_data.append(open("/home/dolica/Documents/writeuploewner/finalreport/data/14-0-10-500-2-Cubic-Exact.csv","r"))

    exact_sols = [empty(MAX_RES,dtype=complex128),empty(MAX_RES,dtype=complex128)]

    for j in range(2):

        data = exact_data[j]
        i = 0

        for line in data.readlines():

            values = line.split()
            exact_sols[j][i] = float(values[0]) + (float(values[1]) * 1j)

            i += 1

    return exact_sols

def plot_me(data):
    plt.plot(data.real, data.imag)

def root_mean_squared_error(exact_sol, approx_sol):

    rms = 0

    for i in range(MAX_RES):

        diff = (absolute(approx_sol[i]) - absolute(exact_sol[i]))
        rms += diff ** 2

    return (1/MAX_RES) * sqrt(rms)

def sqrtToString(sqrt):

    sqrt = str(sqrt)
    first = sqrt[0]
    last = sqrt[2]

    return first + "dot" + last

def runCubicLoewner(i):

    if i == 14:
        module_test = ["f2py", "-c", "-DCASE="+str(i), "NumericalLoewner.F90", "-m", "modules.NumericalLoewner_"+str(i)]
    else:
        module_test = ["f2py", "-c", "-DCASE="+str(i), "NumericalLoewner.F90", "-m", "modules.NumericalLoewner_"+str(i)]

    subprocess.check_output(module_test)
    module_name = "modules.NumericalLoewner_" + str(i)
    CubicLoewner = import_module(module_name)

    if i == 0:
        CubicLoewner.cubicloewner(outerstarttime=start_time, outerfinaltime=final_time, innern=inner_n, first_g_arr=first_g_arr, secnd_g_arr=second_g_arr, constdrivingarg=1)
    else:
        CubicLoewner.cubicloewner(outerstarttime=start_time, outerfinaltime=final_time, innern=inner_n, first_g_arr=first_g_arr, secnd_g_arr=second_g_arr)

    if i == 0 or i == 14:
        createCubicCSV(i,[first_g_arr,second_g_arr],inner_n)
    else:
        createCubicCSV(i,[first_g_arr,second_g_arr])

def createCSVFilename(df,root):

    properties = [str(df), str(start_time), str(final_time), str(outer_n), str(root), "Cubic"]
    return "-".join(properties) + ".csv"

def createSquareRootCSVFilename(df,root,sqrt):

    properties = [str(df), str(start_time), str(final_time), str(outer_n), sqrtToString(sqrt), str(root), "Cubic"]
    return "-".join(properties) + ".csv"

def createCubicCSV(df, results, innerRes=False):

    filenames = [createCSVFilename(df,i) for i in range(1,3)]

    if innerRes:
        filenames[0] = filenames[0][:-4] + "-" + str(innerRes) + ".csv"
        filenames[1] = filenames[1][:-4] + "-" + str(innerRes) + ".csv"

    for i in range(2):

        data = results[i]
        filename = filenames[i]

        real_vals = data.real
        imag_vals = data.imag

        combined = column_stack((real_vals,imag_vals))
        savetxt(output_dir + filename, combined, fmt="%.18f")

def createSquareRootCubicCSV(df, sqrt, results):

    filenames = [createSquareRootCSVFilename(df,i,sqrt) for i in range(1,3)]

    for i in range(2):

        data = results[i]
        filename = filenames[i]

        real_vals = data.real
        imag_vals = data.imag

        combined = column_stack((real_vals,imag_vals))
        savetxt(output_dir + filename, combined, fmt="%.18f")

def runSquareRootCubicLoewner(i,sqrtparam):

    module_test = ["f2py", "-c", "-DCASE="+str(i), "NumericalLoewner.F90", "-m", "modules.NumericalLoewner_"+str(i)]
    subprocess.check_output(module_test)
    module_name = "modules.NumericalLoewner_" + str(i)
    CubicLoewner = import_module(module_name)
    CubicLoewner.cubicloewner(outerstarttime=start_time, outerfinaltime=final_time, innern=inner_n, first_g_arr=first_g_arr, secnd_g_arr=second_g_arr,sqrtdrivingarg=sqrtparam)

    createSquareRootCubicCSV(i,sqrtparam,[first_g_arr,second_g_arr])

def RMSCubicLoewner(i):

    inner_res = [5, 10, 50, 100, 200, 300, 400, 500]
    module_test = ["f2py", "-c", "-DCASE="+str(i), "NumericalLoewner.F90", "-m", "modules.NumericalLoewner_"+str(i)]
    subprocess.check_output(module_test)
    module_name = "modules.NumericalLoewner_" + str(i)
    CubicLoewner = import_module(module_name)

    first_g_arr = empty(outer_n, dtype=complex128)
    second_g_arr = empty(outer_n,  dtype=complex128)

    approx_sol_pairs = []

    for inner_n in inner_res:

        CubicLoewner.cubicloewner(outerstarttime=start_time, outerfinaltime=final_time, innern=inner_n, first_g_arr=first_g_arr, secnd_g_arr=second_g_arr)
        createCubicCSV(i,[first_g_arr,second_g_arr],inner_n)

# RMSCubicLoewner(0)
# RMSCubicLoewner(14)

for drivingFunction in nonSquareRootDriving:
    runCubicLoewner(drivingFunction)
    print("Completed driving function " + str(drivingFunction))

exact_res = [5,10,50,100,200,300,400,500]
error_runs = [0,14]

for df in error_runs:
    for res in exact_res:
        inner_n = res
        runCubicLoewner(df)

final_time = 1
print("Doing square root stuff.")

for kappa in kappas:
    runSquareRootCubicLoewner(10,kappa)

final_time = 10

for alpha in alphas:
    runSquareRootCubicLoewner(11,alpha)
