from subprocess import call
import Constants

def obtain_squareroot_parameter(index):

    if index == Constants.KAPPA_IDX:
        query = "Enter the desired value for kappa: "
    if index == Constants.C_ALPHA_IDX:
        query = "Enter the desired value for c_alpha: "

    while(True):

        parameter = input(query)

        try:

            # Convert the answer to a float
            parameter = float(parameter)

            # Return if parameter is positive
            if parameter > 0:
                return (index, parameter)

        except ValueError:
            # Repeat if input could not be converted to float
            continue

def select_multiple():

    while(True):

        # Ask for the user input
        indices = input("Enter the indices of the driving functions you wish to use seperated by a space: ")
        
        try:

            # Convert the indices to integer list
            indices = [int(x) for x in indices.split()]

            # Check that all the indices are greater greater than or equal to zero
            if all(index >= 0 for index in indices):

                # Return if square-root driving was not selected
                if all(index < Constants.KAPPA_IDX for index in indices):
                    return indices

                else:
                    return [index if index < Constants.KAPPA_IDX else obtain_squareroot_parameter(index) for index in indices]

            else:
                # Repeat if list contained some negative values
                continue

        except ValueError:
            # Repeat if input could not be converted to integer list
            continue

def obtain_driving_selection():

    while (True):

        print("AVALIABLE DRIVING FUNCTIONS")

        # Print all of the possible driving functions
        for i in range(Constants.NUM_OPTIONS):
            print("[" + str(i) + "] " + Constants.DRIVING_OPTIONS[i])

        # Ask for the user selection
        answer = input("Select a driving function: ")

        try:

            # Convert the value to an integer
            answer = int(answer)

            # Return if one of the first nine driving functions is selected
            if answer < Constants.KAPPA_IDX:
                return [answer]

            # Obtain a kappa or c_alpha value
            elif answer in [Constants.KAPPA_IDX, Constants.C_ALPHA_IDX]:
                return [obtain_squareroot_parameter(answer)]

            # Create a list for multiple driving functions
            elif answer == Constants.MULTIPLE_IDX:
                return select_multiple()

            # Create a list containing all driving functions
            elif answer == Constants.ALL_IDX:
                return [i for i in range(Constants.TOTAL_DRIVING_FUNCTIONS)]

            # Print message in case of invalid choice
            else:
                print("Error: Driving function selection is not recognised.")

        except ValueError:
            # Repeat until if driving selection was not an integer
            continue

print(obtain_driving_selection())
