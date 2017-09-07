import Constants
from LoewnerRun import LoewnerRun
from LoewnerRun import SqrtLoewnerRun
from Plot import Plot

def multiple_square_root(index, driving_text):

    while True:

        # Ask for user input
        total_runs = input("Please enter the number of times you wish to run " \
                         + driving_text + ": ")

        try:

            # Convert the value to an integer
            total_runs = int(total_runs)

            # Repeat if this value is less than or equal to zero
            if total_runs <= 0:
                continue

            # Return the list with the square root driving function num_runs
            # many times
            return [index for _ in range(total_runs - 1)]

        except ValueError:
            # Repeat if input could not be converted to an integer
            continue

def select_multiple():

    while True:

        try:

            # Ask for the user input
            indices = input("Please enter the indices of the driving " \
                            + "functions you wish to use seperated by a space: ")

            # Convert the indices to integer list
            indices = list(set([int(x) for x in indices.split()]))

            # Check that all the indices correspond to existing driving functions
            if all(index >= 0 and index < Constants.TOTAL_DRIVING_FUNCTIONS for index in indices):

                # Determine the kappa value
                if Constants.KAPPA_IDX in indices:
                    indices = indices + multiple_square_root(Constants.KAPPA_IDX, "KAPPA")

                # Determine the c_alpha value
                if Constants.C_ALPHA_IDX in indices:
                    indices = indices + multiple_square_root(Constants.C_ALPHA_IDX, "C_ALPHA")

                # Return if all indices are in an acceptable range
                return sorted(indices)

            else:
                # Repeat if list contained invalid values
                continue

        except ValueError:
            # Repeat if input could not be converted to integer list
            continue

def create_loewner_run(driving_function):

    if not Constants.squareroot_driving(driving_function):
        return LoewnerRun(driving_function)

    return SqrtLoewnerRun(driving_function)

def obtain_driving_selection():

    while True:

        print("AVALIABLE DRIVING FUNCTIONS:")

        # Print all of the possible driving functions
        for i in range(Constants.TOTAL_DRIVING_FUNCTIONS):
            print("[" + str(i) + "] " + Constants.DRIVING_INFO[i][0])

        print("[12] MULTIPLE")
        print("[13] ALL")

        # Ask for the user selection
        answer = input("Please select a driving function: ")

        try:

            # Convert the value to an integer
            answer = int(answer)

            # Return if one of the first nine driving functions is selected
            if answer < Constants.MULTIPLE_IDX:
                return [create_loewner_run(answer)]

            # Create a list for multiple driving functions
            elif answer == Constants.MULTIPLE_IDX:
                return [create_loewner_run(index) for index in select_multiple()]

            # Create a list containing all driving functions
            elif answer == Constants.ALL_IDX:
                return [create_loewner_run(i) for i in range(Constants.TOTAL_DRIVING_FUNCTIONS)]

            # Print message in case of invalid choice
            else:
                print("Error: Driving function selection is not recognised.")

        except ValueError:
            # Repeat if driving selection was not an integer
            continue

def obtain_exact_selection():

    while True:

        print("AVALIABLE DRIVING FUNCTIONS:")

        # Print all avaliable driving functions
        for i in range(Constants.TOTAL_DRIVING_FUNCTIONS):
            print("[" + str(i) + "] " + Constants.EXACT_OPTIONS[i][0])

        # Ask for the user selection
        answer = input("Please select a driving function: ")

        try:

            answer = int(answer)

            if answer < 0 or answer >= total_driving_functions:
                continue

            return [LoewnerRun(driving_function)]

        except ValueError:
            continue

def set_resolution_parameters(loewner_run):

    while True:

        # Ask for the run parameters
        values = input(loewner_run.driving_string() + "Please enter the star" \
                       + "t time, end time, and number of points seperated b" \
                       + "y a space: ")
        try:

            # Split the input
            values = values.split()

            # Ensure that three values were entered
            if len(values) != 3:
                continue

            start_time = float(values[0])

            # Check that the start time >= 0
            if start_time < 0:
                continue

            # Check that final time is greater than the start time
            if float(values[1]) <= start_time:
                continue

            # Check that the number of points is >= 1
            if int(values[2]) < 1:
                continue

            # Create the execution command
            return [start_time, float(values[1]), int(values[2])]

        except ValueError:
            # Repeat if input had incorrect format
            continue
            
def obtain_squareroot_parameter(loewner_run):

    if loewner_run.driving_function == Constants.KAPPA_IDX:
        query = "Please enter the desired kappa value: "

    elif loewner_run.driving_function == Constants.C_ALPHA_IDX:
        query = "Please enter the desired c_alpha value: "

    else:
        # Error
        pass

    while True:

        try:

           # Ask for the square root parameter
            answer = float(input(query))

            # Return if answer can be converted to a float and is positive
            if answer > 0:
                return answer 

        except ValueError:
            # Repeat if answer could not be converted to float
            continue

def generate_plots(loewner_runs):

    for loewner_run in loewner_runs:
        loewner_plot = Plot(loewner_run.driving_function, loewner_run.resolution_parameters, loewner_run.results)
        loewner_plot.generate_plot()

def standard_mode():

    loewner_runs = obtain_driving_selection()

    for loewner_run in loewner_runs:

        if Constants.squareroot_driving(loewner_run.driving_function):
            loewner_run.sqrt_param = obtain_squareroot_parameter(loewner_run)

        loewner_run.resolution_parameters = set_resolution_parameters(loewner_run)
        loewner_run.perform_loewner()

    generate_plots(loewner_runs)

def exact_solutions():
    exit()

def mode_selection():

    while True:

        print("RUN OPTIONS:")

        for i in range(len(Constants.RUN_OPTIONS)):
            print("[" + str(i) + "] " + Constants.RUN_OPTIONS[i])

        # Ask for user input
        answer = input("Please enter the desired mode: ")

        try:

            # Convert the value to an integer
            answer = int(answer)

            # Enter standard mode
            if answer == 0:
                return standard_mode()

            if answer == 1:
                exit()

            if answer == 2:
                return exact_solutions()

            else:
                # Error
                continue

        except ValueError:
            # Repeat if the input could not be converted to an integer
            continue


mode_selection()
