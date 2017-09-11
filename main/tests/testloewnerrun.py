from os import remove
from glob import glob
import sys
import inspect
import unittest
from pathlib import Path
from LoewnerRun import LoewnerRun, SqrtLoewnerRun
from re import fullmatch
import Constants

class LoewnerRunTests(unittest.TestCase):

    def create_loewner_runs(self):

        loewner_runs = []

        for driving_function in range(Constants.TOTAL_DRIVING_FUNCTIONS):

            if not Constants.squareroot_driving(driving_function):
                loewner_runs.append(LoewnerRun(driving_function))

            else:
                loewner_runs.append(SqrtLoewnerRun(driving_function))

        return loewner_runs

    def test_filename(self):

        loewner_runs = self.create_loewner_runs() 

        for loewner_run in loewner_runs:

            filename = loewner_run.fortran_filename

            my_file = Path(loewner_run.fortran_filename)
            self.assertTrue(my_file.is_file())
           
    def test_module_name(self):

        loewner_runs = self.create_loewner_runs()
        
        for loewner_run in loewner_runs:

            self.assertTrue(loewner_run.module_name[:8] == "modules.")

            if loewner_run.driving_function < 10:
                self.assertTrue(fullmatch("_\d",loewner_run.module_name[-2:]))

            else:
                self.assertTrue(fullmatch("_\d\d", loewner_run.module_name[-3:]))

    def test_compile_command(self):

        loewner_runs = self.create_loewner_runs()
        module_file_pattern = "modules/*.so"

        for module_file in glob(module_file_pattern):
            remove(module_file)

        total_module_files = len(glob(module_file_pattern))

        self.assertTrue(total_module_files == 0)

        for loewner_run in loewner_runs:
            loewner_run.set_compile_command()
            loewner_run.compile_loewner()

        total_module_files = len(glob(module_file_pattern))
        total_loewner_runs = len(loewner_runs)

        self.assertTrue(total_module_files == total_loewner_runs)
            
if __name__ == '__main__':
    unittest.main()
