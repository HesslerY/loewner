from subprocess import check_output
import Constants
from LoewnerRun import LoewnerRun

def multiple_square_root(index, driving_text):

    while True:
    
        # Ask for user input
        num_runs = input("Please enter the number of times you wish to run " + driving_text + ": ")
        
        try:
        
            # Concert the value to an integer
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

        # Ask for the user input
        indices = input("Plase enter the indices of the driving functions you wish to use seperated by a space: ")
        
        try:

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
    driving_function.run()
    
print("Done!")
