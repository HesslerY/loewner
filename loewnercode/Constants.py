# Declare a list of mode options
RUN_OPTIONS = ["Standard Mode","Resolution Mode","Exact Solutions"]

# Declare a list of driving function options
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
                "dsqrt(t) * c_alpha"]

PLOT_TITLE = ["$\\xi (t) = 0$",
              "$\\xi (t) = t$",
              "$\\xi (t) = \cos(t)$",
              "$\\xi (t) = t \ \cos(t)$",
              "$\\xi (t) = \cos(\pi t)$",
              "$\\xi (t) = t \ \cos(\pi t)$",
              "$\\xi (t) = \sin(t)$",
              "$\\xi (t) = t \ \sin(t)$",
              "$\\xi (t) = \sin(\pi t)$",
              "$\\xi (t) = t \ \sin(\pi t)$",
              "$\\xi (t) = 2 \ \sqrt{ SQRT_PARAM \ (1 - t)}$",
              "$\\xi (t) = c_{SQRT_PARAM} \sqrt{t}$"]

# Declare a list of "exact" solution options
EXACT_INFO = [["t", "$\\xi (t) = t$"]]

# Obtain the total number of driving functions
TOTAL_DRIVING_FUNCTIONS = len(DRIVING_INFO)

# Indices for "special" driving functions
KAPPA_IDX = 10
C_ALPHA_IDX = 11
MULTIPLE_IDX = 12
ALL_IDX = 13

# Compilation-related lists
F2PY_FIRST = ["f2py", "-c"]

def squareroot_driving(driving_function):
    return driving_function in [KAPPA_IDX, C_ALPHA_IDX]
