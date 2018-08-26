import sys
sys.path.append('PythonTools')
import unittest
from LoewnerRun import *

class MyTest(unittest.TestCase):

    def test_initialise(self):

        index = 0
        start_time = 0
        final_time = 0
        outer_points = 0
        inner_points = 0
        compile_fortran = True
        save_data = True
        save_plot = True

        loewner_run = LoewnerRun(index,start_time,final_time,outer_points,inner_points, \
                compile_fortran,save_data,save_plot)

        self.assertEqual(loewner_run.index,index)
        self.assertEqual(loewner_run.start_time,start_time)
        self.assertEqual(loewner_run.final_time,final_time)
        self.assertEqual(loewner_run.outer_points,outer_points)
        self.assertEqual(loewner_run.inner_points,inner_points)
        self.assertEqual(loewner_run.compile_fortran,compile_fortran)
        self.assertEqual(loewner_run.save_data,save_data)
        self.assertEqual(loewner_run.save_plot,save_plot)
