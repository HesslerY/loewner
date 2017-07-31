from subprocess import call
import Constants

def obtain_squareroot_parameter(index):

    if index == Constants.KAPPA_IDX:
        query = "Select the desired value for kappa: "
    if index == Constants.C_ALPHA_IDX:
        query = "Select the desired value for c_alpha: "

    while(True):

        paramater = input(query)

        try:

            # Convert the answer to a float
            parameter = float(parameter)

            # Return if kappa is positive
            if parameter > 0:
                return [(index, parameter)]

        except:
            pass

def select_multiple():

    while(True):

        indices = input("Enter the indices of the driving functions you wish to use seperated by a space: ")
        
        try:

            indices = [int(x) for x in indices.split()]
            
            for index in indices:

                # Check that the indices have appropriate values
                if index > Constants.C_ALPHA_IDX or index < 0:
                    continue
    
                if index == Constants.C_ALPHA_IDX

            return indices

        except:
            pass

        print("Hello.")

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

            # Obtain a kappa value
            elif answer == Constants.KAPPA_IDX:
                return obtain_kappa()

            # Obtain a c_alpha value
            elif answer == Constants.C_ALPHA_IDX:
                return obtain_c_alpha()

            # Create a list for multiple driving functions
            elif answer == Constants.MULTIPLE_IDX:
                return select_multiple()

            # Create a list containing all driving functions
            elif answer == Constants.ALL_IDX:
                return [i for i in range(Constants.TOTAL_DRIVING_FUNCTIONS)]

            # Print message in case of invalid choice
            else:
                print("Error: Driving function selection is not recognised.")

        except:
            pass

print(obtain_driving_selection())
