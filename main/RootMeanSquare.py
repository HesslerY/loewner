import sys
sys.path.append('PythonTools')
from RootMeanSquareError import RootMeanSquareError

# Set time and resolution parameters
start_time = 0
final_time = 25
cubic_final_time = 10
outer_points = 1000
inner_points = 10

# Create a set of inner resolution parameters
res = [5,50,100,200,300,400,500]

# Create a RootMeanSqaure object
rms_tool = RootMeanSquareError(start_time,final_time,outer_points,inner_points,res)

# Compute the error for single-trace runs with a known exact solution
rms_tool.quadratic_forward_error()

# Create a RootMeanSquare object
cubic_rms_tool = RootMeanSquareError(start_time,cubic_final_time, outer_points, inner_points, res)

# Compute the error for two-trace runs with a known exact solution
cubic_rms_tool.cubic_forward_error()
