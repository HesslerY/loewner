from subprocess import check_output
import Constants
from LoewnerRun import LoewnerRun

def select_multiple():

    while True:

        # Ask for the user input
        indices = input("Plase enter the indices of the driving functions you wish to use seperated by a space: ")
        
        try:

            # Convert the indices to integer list
            indices = [int(x) for x in indices.split()]

            if all(index >= 0 and index < Constants.TOTAL_DRIVING_FUNCTIONS for index in indices):
                # Return if all indices are in an acceptable range
                return indices

            else:
                # Repeat if list contained invalid values
                continue

        except ValueError:
            # Repeat if input could not be converted to integer list
            continue

def obtain_driving_selection():

    while True:

        print("AVALIABLE DRIVING FUNCTIONS")

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
                return [LoewnerRun(answer)]

            # Create a list for multiple driving functions
            elif answer == Constants.MULTIPLE_IDX:
                return [LoewnerRun(index) for index in select_multiple()]

            # Create a list containing all driving functions
            elif answer == Constants.ALL_IDX:
                return [LoewnerRun(i) for i in range(Constants.TOTAL_DRIVING_FUNCTIONS)]

            # Print message in case of invalid choice
            else:
                print("Error: Driving function selection is not recognised.")

        except ValueError:
            # Repeat if driving selection was not an integer
            continue

driving_functions = obtain_driving_selection()

for driving_function in driving_functions:
    # print(driving_function.compile_command)
    # print(driving_function.execute_command)
    driving_function.run()

# for driving_function in driving_functions:

#    plot_loewner(driving_function)
