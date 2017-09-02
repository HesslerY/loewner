import Constants

from LoewnerConfig import LoewnerConfig
from LoewnerRun import LoewnerRun

def multiple_square_root(index, driving_text):

    while True:

        # Ask for user input
        num_runs = input("Please enter the number of times you wish to run " + driving_text + ": ")

        try:

            # Convert the value to an integer
            num_runs = int(num_runs)

            # Repeat if this value is less than or equal to zero
            if num_runs <= 0:
                continue

            # Return the list with the square root driving function num_runs many times
            return [index for _ in range(num_runs - 1)]

        except ValueError:
            # Repeat if input could not be converted to an integer
            continue

def select_multiple():

    while True:

        try:

            # Ask for the user input
            indices = input("Plase enter the indices of the driving functions you wish to use seperated by a space: ")

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
                return [LoewnerConfig(driving_function=answer, exact_mode=False)]

            # Create a list for multiple driving functions
            elif answer == Constants.MULTIPLE_IDX:
                return [LoewnerConfig(driving_function=index, exact_mode=False) for index in select_multiple()]

            # Create a list containing all driving functions
            elif answer == Constants.ALL_IDX:
                return [LoewnerConfig(driving_function=i, exact_mode=False) for i in range(Constants.TOTAL_DRIVING_FUNCTIONS)]

            # Print message in case of invalid choice
            else:
                print("Error: Driving function selection is not recognised.")

        except ValueError:
            # Repeat if driving selection was not an integer
            continue

def obtain_exact_selection():

    total_driving_functions = len(Constants.EXACT_OPTIONS)

    while True:

        print("AVALIABLE DRIVING FUNCTIONS:")

        # Print all avaliable driving functions
        for i in range(total_driving_functions):
            print("[" + str(i) + "] " + Constants.EXACT_OPTIONS[i])

        # Ask for the user selection
        answer = input("Please select a driving function: ")

        try:

            answer = int(answer)

            if answer < 0 or answer >= total_driving_functions:
                continue

            return [LoewnerConfig(driving_function=answer, exact_mode=True)]

        except ValueError:
            continue

def standard_mode():

    driving_functions = obtain_driving_selection()

    for driving_function in driving_functions:
        loewner_run = LoewnerRun(driving_function)

def exact_solutions():

    driving_functions = obtain_exact_selection()

    for driving_function in driving_functions:
        pass

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
                pass

        except ValueError:
            # Repeat if the input could not be converted to an integer
            continue


mode_selection()
print("Done!")
