# Declare a list of all the avaliable driving functions
DRIVING_INFO = [["0.0","$\\xi (t) = 0$"],
                ["t","$\\xi (t) = t$"],
                ["cos(t)","$\\xi (t) = \cos(t)$"],
                ["t * cos(t)","$\\xi (t) = t \ \cos(t)$","t * cos(t)"],
                ["cos(t * pi)","$\\xi (t) = \cos(\pi t)$"],
                ["t * cos(t * pi)","$\\xi (t) = t \ \cos(\pi t)$"],
                ["sin(t)","$\\xi (t) = \sin(t)$"],
                ["t * sin(t)","$\\xi (t) = t \ \sin(t)$"],
                ["sin(t * pi)", "$\\xi (t) = \sin(\pi t)$"],
                ["t * sin(t * pi)","$\\xi (t) = t \ \sin(\pi t)$"],
                ["2 * dsqrt(kappa * (1 - t))", "$\\xi (t) = 2 \ \sqrt{ SQRT_PARAM \ (1 - t)}$"],
	            ["dsqrt(t) * c_alpha","$\\xi (t) = c_{SQRT_PARAM} \sqrt{t}$"]]

# Obtain the total number of driving functions
TOTAL_DRIVING_FUNCTIONS = len(DRIVING_INFO)

# Indices for "special" driving functions
KAPPA_IDX = 10
C_ALPHA_IDX = 11
MULTIPLE_IDX = 12
ALL_IDX = 13

# Compilation-related lists
f2py_start = ["f2py", "-c"]
f2py_end = ["NumericalLoewner.F90", "-m", "NumericalLoewner"]
