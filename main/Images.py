from LoewnerRun import LoewnerRun, SqrtLoewnerRun
import Constants
from Plot import Plot

def create_loewner_runs():

    loewner_runs = []

    for driving_function in range(Constants.TOTAL_DRIVING_FUNCTIONS):

        if not Constants.squareroot_driving(driving_function):
            loewner_runs.append(LoewnerRun(driving_function))
            loewner_runs[-1].final_time = 15
        else:
            loewner_runs.append(SqrtLoewnerRun(driving_function))
            loewner_runs[-1].final_time = 1

        loewner_runs[-1].start_time = 0
        loewner_runs[-1].total_points = 500

    return loewner_runs

plot_dir = "/home/dolica/Documents/writeuploewner/finalreport/images/"
loewner_runs = create_loewner_runs()

for run in loewner_runs:

    run.perform_loewner()
    df = run.driving_function
    res = [run.start_time, run.final_time, run.total_points]
    points = run.results

    plotter = Plot(df,res,points,plot_dir)
    plotter.generate_plot()
