from math import pi

# Strings for the names of the different driving functions
DRIVING_INFO = ["0.0",
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
                "floor(t)",
                "floot(t) % 2",
                "sqrt(1 + t)"]

PLOT_TITLE = [["$\\xi (t) = ","$"],
              "$\\xi (t) = t$",
              "$\\xi (t) = \cos(t)$",
              "$\\xi (t) = t \ \cos(t)$",
              "$\\xi (t) = \cos(\pi t)$",
              "$\\xi (t) = t \ \cos(\pi t)$",
              "$\\xi (t) = \sin(t)$",
              "$\\xi (t) = t \ \sin(t)$",
              "$\\xi (t) = \sin(\pi t)$",
              "$\\xi (t) = t \ \sin(\pi t)$",
              ["$\\xi (t) = 2 \ \sqrt{","\ (1 - t)}$"],
              ["$\\xi (t) = c_{","} \sqrt{t}$"],
              "$\\xi (t) = \lfloor t \\rfloor $",
              "$\\xi (t) = \lfloor t \\rfloor \ \\mathrm{mod} \ 2$",
              "$\\xi (t) = \sqrt{1 + t}$"]

# Obtain the total number of driving functions
TOTAL_DRIVING_FUNCTIONS = len(DRIVING_INFO)

# Indices for "special" driving functions
KAPPA_IDX = 10
CALPHA_IDX = 11
CONST_IDX = 0
LINR_IDX = 1
SQRTPLUS_IDX = 14
PERIODIC_DRIVING = [i for i in range(2,10)]
MULTIPLE_IDX = TOTAL_DRIVING_FUNCTIONS
ALL_IDX = TOTAL_DRIVING_FUNCTIONS + 1
STANDARD_IDXS = [i for i in range (1,10)] + [i for i in range(12,15)] # Driving functions that don't require any extra parameters
CUBIC_EXACT_IDXS = [0,14]
QUADRATIC_FORWARD_EXACT_IDXS = [1]
ALL_EXACT_IDX = CUBIC_EXACT_IDXS + QUADRATIC_FORWARD_EXACT_IDXS
NOTORIGIN_IDXS = [0,14]

# Inicides of the driving functions
DRIVING_LIST = ["["+str(pair[0])+"] " + pair[1] for pair in enumerate(DRIVING_INFO)]

# Compilation related lists
F2PY_FIRST = ["f2py", "-c"]

def SQUAREROOT_DRIVING(driving_function):
    return driving_function in [KAPPA_IDX, CALPHA_IDX]

# Nonlinear solver tolerance
TOL = 1e-13

# Extension for data file output
DATA_EXT = ".dat"
PLOT_EXT = ".pdf"

# Extension for data fortran files
FORTRAN_EXT = ".F90"

# Extension for data fortran files
DATA_PREC = "%.18f"

# Names of the Forward files that are used to solve Loewner's equation
FOR_LOEWNER = "ForwardLoewner"
INV_LOEWNER = "InverseLoewner"

# Directories for the data files
EXACT_FORWARD_DATA_OUTPUT = "Output/Data/SingleTrace/ExactForward/"
EXACT_CUBIC_DATA_OUTPUT = "Output/Data/TwoTrace/ExactSolutions/"
FORWARD_DATA_OUTPUT = "Output/Data/SingleTrace/Forward/"
FORSHIFT_DATA_OUTPUT = "Output/Data/SingleTrace/TranslatedForward/"
INVERSE_DATA_OUTPUT = "Output/Data/SingleTrace/Inverse/"
EXACT_INVERSE_DATA_OUTPUT = "Output/Data/ExactInverse/"
CUBIC_DATA_OUTPUT = "Output/Data/TwoTrace/Forward/"
FINGER_DATA_OUTPUT = "Output/Data/FingeredGrowth/"
WEDGE_DATA_OUTPUT = "Output/Data/WedgeGrowth/"

# Directories for the plot files
EXACT_FORWARD_PLOT_OUTPUT = "Output/Plots/SingleTrace/ExactForward/"
EXACT_CUBIC_PLOT_OUTPUT = "Output/Plots/TwoTrace/ExactSolutions/"
FORWARD_PLOT_OUTPUT = "Output/Plots/SingleTrace/Forward/"
FORSHIFT_PLOT_OUTPUT = "Output/Plots/SingleTrace/TranslatedForward/"
INVERSE_PLOT_OUTPUT = "Output/Plots/SingleTrace/Inverse/"
EXACT_INVERSE_PLOT_OUTPUT = "Output/Plots/ExactInverse/"
CUBIC_PLOT_OUTPUT =  "Output/Plots/TwoTrace/Forward/"
FINGER_PLOT_OUTPUT = "Output/Plots/FingeredGrowth/"
WEDGE_PLOT_OUTPUT = "Output/Plots/WedgeGrowth/"

# Directories for root mean squared error data
QUADRATIC_FORWARD_RMS =  "Output/Data/SingleTrace/RootMeanSquared/Forward/"
QUADRATIC_INVERSE_RMS =  "Output/Data/SingleTrace/RootMeanSquared/Forward/"
CUBIC_FORWARD_RMS =  "Output/Data/TwoTrace/RootMeanSquared/Forward/"

# Names for the different algorithms used
FOR_RUN_STR = "Forward"
INV_RUN_STR = "Inverse"
CBC_RUN_STR = "Cubic"

# Plot axis labels for forward/cubic runs
FOR_PLOT_XL = 'Re($z$)'
FOR_PLOT_YL = 'Im($z$)'

# Plot axis labels for inverse runs
INV_PLOT_XL = '$t$'
INV_PLOT_YL = r'$\xi(t)$'

# Define the constant that is used for the exact solutions in the case of xi(t) = Constant
EXACT_CUBIC_CONSTANT = 1

# Define pi/2 constant for solving Gubiec + Szymczak equation
HALF_PI = pi / 2

# Prompt message
LOEWNER_PROMPT = "Loewner >> "

# Define location for start message
START_MSG = "PythonTools/Misc/Start"

# Define location of help message for interface
HELPMSG = "PythonTools/HelpMessages/MainHelp"

# Create lists/strings of common commands for interface
BACK_COMMANDS = ["b","back"]
HELP_FULL = "help"
HELP_SHORT = "h"
QUIT_FULL = "quit"
QUIT_SHORT = "q"
EXIT = "exit"
DRIVING_FUNCTIONS = "df"

# Strings for various parameters that can be changed thorough the interface
START_TIME = "starttime"
FINAL_TIME = "finaltime"
OUTER_RES = "outerres"
INNER_RES = "innerres"
COMPILE = "compile"
SAVE_PLOTS = "saveplots"
SAVE_DATA = "savedata"
KAPPA = "kappa"
KAPPAS = "kappas"
CALPHAS = "calphas"
DRIVE_ALPHA = "drivealpha"
WEDGE_ALPHA = "wedgealpha"
MULTIPLE_TIMES = "times"
MULTIPLE_RES = "res"
START_PHI = "startphi"
FINAL_PHI = "finalphi"
LINR_IM = "linearimplicit"
LINR_EX = "linearexplicit"
CONSTANT = "constant"

# Strings for arguments that are converted to booleans (used for saving and compilation)
USER_TRUE = "y"
USER_FALSE = "n"

# Strings for the modes that can be selected through the interface:
FORWARD_SINGLE_MODE = "forsin"
INVERSE_SINGLE_MODE = "invsin"
TWO_TRACE_MODE = "two"
WEDGE_TRACE_MODE = "wedge"
EXACT_INVERSE_MODE = "exactinv"
KAPPA_MODE = KAPPA
CALPHA_MODE = "calpha"
EXACT_MODE = "exact"
ERROR_MODE = "rms"

# Other commands
CLEAR_DRIVING = "cleardriving"
PRINT_DRIVING_LIST = "printdriving"
START_ALG = "start"
DISP_ERROR = "error"
SQRT_STEP = "step"
NUM_SQRT_RUNS = "num"
CREATE_DRIVING_LIST = "run"
