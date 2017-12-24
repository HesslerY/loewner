from LoewnerRun import LoewnerRun, ExactLoewnerRun
from Plot import MultiPlot

# Exact solution for xi(t) = t

plot_dir = "/home/dolica/Documents/writeuploewner/finalreport/images/"
exact_results = []

exact_run = ExactLoewnerRun(1)
exact_run.final_time = 25
exact_run.start_time = 0
exact_run.total_points = 1000
exact_run.perform_loewner()

res = [5]

for i in range(3):
    res.append(res[-1] * 2)

labels = [str(res_val) for res_val in res] + ["Exact"]
df = 1
loewner_run = LoewnerRun(1)
loewner_run.start_time = 0
loewner_run.final_time = 25

for total_points in res:

    loewner_run.total_points = total_points
    loewner_run.perform_loewner()
    exact_results.append(loewner_run.results)

exact_results.append(exact_run.results)

plotter = MultiPlot(df,[0,25,1000],exact_results,plot_dir,labels)
plotter.generate_plot()
