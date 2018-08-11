import sys
sys.path.append('../PythonTools')
from RootMeanSquareError import RootMeanSquareError

start_time = 0
final_time = 25
cubic_final_time = 10
outer_points = 1000
inner_points = 10

res = [5,50,100,200,300,400,500]

rms_tool = RootMeanSquareError(start_time,final_time,outer_points,inner_points,res)
rms_tool.quadratic_forward_error()

cubic_rms_tool = RootMeanSquareError(start_time,cubic_final_time, outer_points, inner_points, res)
cubic_rms_tool.cubic_forward_error()
