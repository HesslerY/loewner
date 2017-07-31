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

def obtain_plot_parameters():

    while True:

        values = input("Enter the start time, end time, and number of points seperated by a space: ")
        
        try:

            values = values.split()

            if len(values) != 3:
                continue

            values[0] = float(values[0])
            values[1] = float(values[1])
            values[2] = int(values[2])

            if values[0] < 0:
                continue
            if values[1] < 0:
                continue
            if values[2] < 1:
                continue

            return values

        except ValueError:
            continue

def compile_loewner(driving_selection, plot_parameters):

    compile_string = Constants.COMPILE_STRING[:]

    for driving_function in driving_selection:

        if type(driving_function) is int:
            compile_string[0] += str(driving_function)
            
        elif type(driving_function) is tuple:
            compile_string[0] += str(driving_function[0])

            if driving_function[0] == Constants.KAPPA_IDX:
                compile_string[0] += " -D KAPPA="
            elif driving_function[0] == Constants.C_ALPHA_IDX:
                compile_string[0] += " -D C_ALPHA="
            else:
                print("Error?")

            compile_string[0] += str(driving_function[1])

        else:
            print("Error?")

        compile_string = " ".join(compile_string)
        call(compile_string, shell = True)

def execute_loewner(plot_parameters):

    execute_string = ["./NumericalLoewner.out"] + [str(param) for param in plot_parameters]
    execute_string = " ".join(execute_string)
    print(execute_string)
    call(execute_string, shell = True)
    call("tail result.txt", shell = True)

def plot_loewner():
    pass
        

driving_selection = obtain_driving_selection()
plot_parameters = obtain_plot_parameters()

print(plot_parameters)
test = input("Let's look")

compile_loewner(driving_selection,plot_parameters)
execute_loewner(plot_parameters)
plot_loewner()
