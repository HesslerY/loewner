COMPILER = "gfortran"

# Declare a list of all the avaliable driving functions
DRIVING_OPTIONS = ["0.0",
                   "t",
                   "cos(t)",
                   "t * cos(t)",
                   "cos(t * pi)",
                   "t * cos(t * pi)",
                   "sin(t)",
                   "t * sin(t)",
                   "sin(t * pi)",
                   "t * sin(t * pi)",
                   "2 * dsqrt(kappa * (1 - t))",
	               "dsqrt(t) * c_alpha",
                   "MULTIPLE",
                   "ALL"]

NUM_OPTIONS = len(DRIVING_OPTIONS)
TOTAL_DRIVING_FUNCTIONS = NUM_OPTIONS - 2

KAPPA_IDX = 10
C_ALPHA_IDX = 11
MULTIPLE_IDX = 12
ALL_IDX = 13

COMPILE_STRING = [COMPILER + " -D CASE=","NumericalLoewner.F03 -o NumericalLoewner.out"]


