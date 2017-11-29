from LoewnerRun import LoewnerRun, SqrtLoewnerRun
from InverseRun import InverseRun
import Constants
from Plot import Plot, MultiPlot, InversePlot, MiniPlot

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
    kappas = [1,2.5,3.5,4,4.5,6,8]

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

plot_dir = "/home/dolica/Documents/writeuploewner/finalreport/images/"
loewner_runs = create_loewner_runs()
kappa_runs = create_kappa_runs()
calpha_runs = create_calpha_runs()

for run in loewner_runs:

    run.perform_loewner()
    df = run.driving_function
    res = [run.start_time, run.final_time, run.total_points]
    points = run.results

    plotter = Plot(df,res,points,plot_dir)
    plotter.generate_plot()

    plotter = MiniPlot(df,res,points,plot_dir)
    plotter.generate_plot()

    inverse_loewner = InverseRun(df,points,res)
    inverse_loewner.perform_inverse()

    time_arr = inverse_loewner.time_arr
    driving_arr = inverse_loewner.driving_arr

    plotter = InversePlot(df,res,time_arr,driving_arr,plot_dir)
    plotter.generate_plot()

kappa_results = []

for run in kappa_runs:
    run.perform_loewner()
    kappa_results.append(run.results)

kappa_drive = kappa_runs[0].driving_function
kappa_res = [kappa_runs[0].start_time, kappa_runs[0].final_time, kappa_runs[0].total_points]

kappa_plotter = MultiPlot(kappa_drive, kappa_res, kappa_results, plot_dir)
kappa_plotter.shift_results()
kappa_plotter.generate_plot()

calpha_results = []

for run in calpha_runs:
    run.perform_loewner()
    calpha_results.append(run.results)

calpha_drive = calpha_runs[0].driving_function
calpha_res = [calpha_runs[0].start_time, calpha_runs[0].final_time, calpha_runs[0].total_points]

calpha_plotter = MultiPlot(calpha_drive, calpha_res, calpha_results, plot_dir)
calpha_plotter.shift_results()
calpha_plotter.generate_plot()
