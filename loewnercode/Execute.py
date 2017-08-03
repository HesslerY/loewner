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

            # Check that all the indices are in an acceptable range
            if all(index >= 0 and index < Constants.TOTAL_DRIVING_FUNCTIONS for index in indices):
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
                return [LoewnerRun(mult) for mult in select_multiple()]

            # Create a list containing all driving functions
            elif answer == Constants.ALL_IDX:
                return [LoewnerRun(i) for i in range(Constants.TOTAL_DRIVING_FUNCTIONS)]

            # Print message in case of invalid choice
            else:
                print("Error: Driving function selection is not recognised.")

        except ValueError:
            # Repeat if driving selection was not an integer
            continue

def compile_loewner(driving_selection):

    compile_string = Constants.COMPILE_STRING[:]

    if type(driving_function) is int:
        compile_string[0] += str(driving_function)
            
    elif type(driving_function) is tuple:
        compile_string[0] += str(driving_function[0])

        if driving_function[0] == Constants.KAPPA_IDX:
            compile_string[0] += " -D KAPPA="
        elif driving_function[0] == Constants.C_ALPHA_IDX:
            compile_string[0] += " -D C_ALPHA="
        else:
            # This is an error
            pass

        compile_string[0] += str(driving_function[1])

    else:
        # This is an error
        pass

    compile_string = " ".join(compile_string)
    check_output(compile_string, shell = True)

def execute_loewner(plot_parameters):

    execute_string = ["./NumericalLoewner.out"] + [str(param) for param in plot_parameters]
    execute_string = " ".join(execute_string)

    check_output(execute_string, shell = True)
    # check_output("tail result.txt", shell = True)

def plot_loewner(driving_function):
    
    plot_string = ["python Plot.py"]

    if type(driving_function) is int:
        plot_string += [str(driving_function), "1", "0"]
    elif type(driving_function) is tuple:
        plot_string += [str(driving_function[0]), "1", str(driving_function[1])]
    else:
        # Error
        pass

    plot_string = " ".join(plot_string)
    check_output(plot_string, shell = True)

driving_functions = obtain_driving_selection()

for driving_function in driving_functions:
    print(driving_function.compile_command)
    print([driving_function.start_time, driving_function.final_time, driving_function.num_points])


# plot_parameters = obtain_plot_parameters()

# for driving_function in driving_functions:

#    compile_loewner(driving_function)
#    execute_loewner(plot_parameters)
#    plot_loewner(driving_function)
