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

# Inicides of the driving functions
DRIVING_INDICES = {pair[1] : pair[0] for pair in enumerate(DRIVING_INFO)}

# Compilation related lists
F2PY_FIRST = ["f2py", "-c"]

def SQUAREROOT_DRIVING(driving_function):
    return driving_function in [KAPPA_IDX, CALPHA_IDX]

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
EXACT_FORWARD_DATA_OUTPUT = "../Output/Data/Quadratic/ExactSolutions/"
EXACT_CUBIC_DATA_OUTPUT = "../Output/Data/Cubic/ExactSolutions/"
FORWARD_DATA_OUTPUT = "../Output/Data/Quadratic/Forward/"
FORSHIFT_DATA_OUTPUT = "../Output/Data/Quadratic/TranslatedForward/"
INVERSE_DATA_OUTPUT = "../Output/Data/Quadratic/Inverse/"
CUBIC_DATA_OUTPUT = "../Output/Data/Cubic/Forward/"

# Directories for the plot files
EXACT_FORWARD_PLOT_OUTPUT = "../Output/Plots/Quadratic/ExactSolutions/"
EXACT_CUBIC_PLOT_OUTPUT = "../Output/Plots/Cubic/ExactSolutions/"
FORWARD_PLOT_OUTPUT = "../Output/Plots/Quadratic/Forward/"
FORSHIFT_PLOT_OUTPUT = "../Output/Plots/Quadratic/TranslatedForward/"
INVERSE_PLOT_OUTPUT = "../Output/Plots/Quadratic/Inverse/"
CUBIC_PLOT_OUTPUT =  "../Output/Plots/Cubic/Forward/"

# Names for the different algorithms used
FOR_RUN_STR = "Forward"
INV_RUN_STR = "Inverse"
CBC_RUN_STR = "Cubic"

# Plot axis labels for forward/cubic runs
FOR_PLOT_XL = 'Re($g$)'
FOR_PLOT_YL = 'Im($g$)'

# Plot axis labels for inverse runs
INV_PLOT_XL = '$t$'
INV_PLOT_YL = r'$\xi(t)$'
