import Constants

class LoewnerRun:

    def __init__(self, driving_func_index):

        self.driving_func_index = driving_func_index
        self.compile_string = "gfortran -D CASE=" + str(driving_func_index) + " NumericalLoewner.F03 -o NumericalLoewner.out"

        if driving_func_index == Constants.KAPPA_IDX:
            self.query = "Enter the desired value for kappa: "
        if driving_func_index == Constants.C_ALPHA_IDX:
            self.query = "Enter the desired value for c_alpha: "
