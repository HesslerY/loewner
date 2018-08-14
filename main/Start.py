from PythonTools.Constants import LOEWNER_PROMPT, FORSINGLE_HELPMSG, INVSINGLE_HELPMSG, FORINV_HELPMSG, TWO_HELPMSG, WEDGE_HELPMSG, HELPMSG, DRIVING_LIST, BACK_COMMANDS, HELP_COMMANDS
#from PythonTools.LoewnerRunFactory import LoewnerRunFactory
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import button_dialog

# Print a help message
def print_help_message(msg_type):

    help_file_loc = help_responses[msg_type]
    help_file = open(help_file_loc)

    for line in help_file:
        print(line.strip('\n'))

    print("")
    return

# Exit the program
def exit_loewner(msg_type):
    exit()

def bad_input_message(user_input):
    print("Unrecognised instruction: " + user_input + " (Press h for help)")

def print_driving_functions():

    for item in DRIVING_LIST:
        print(item)

def valid_driving_functions(user_input):

    for item in user_input.split():

        try:
            temp = float(item)
        except ValueError:
            return False

    return True

# Run the forward single-trace algorithm
def forward_single_trace():

    print("Forward Single-Trace Mode:")

    # Run the prompt
    while True:

        # Await under input
        user_input = session.prompt()

        # Check for 'go back' instruction
        if user_input in BACK_COMMANDS:
            return

        # check for the help instruction
        elif user_input == "dr":
            print_driving_functions()

        # Check if in the response correponds with help/exit
        elif user_input in basic_responses:
            basic_responses[user_input](user_input)

        # Check if a list of driving functions were entered
        elif valid_driving_functions(user_input):
            pass

        # Print the bad input message
        else:
            bad_input_message(user_input)

# Run the inverse single-trace algorithm
def inverse_single_trace():

    print("Inverse Single-Trace Selected.")

    while True:
        user_input = session.prompt()

# Run the forward and inverse single-trace algorithms
def forinv_single_trace():

    print("Forward + Inverse Single-Trace Mode:")

    # Run the prompt
    while True:

        # Await under input
        user_input = session.prompt()

        # Check for 'go back' instruction
        if user_input in BACK_COMMANDS:
            return

        # check for the help instruction
        elif user_input == "dr":
            print_driving_functions()

        # Check if in the response correponds with help/exit
        elif user_input in basic_responses:
            basic_responses[user_input]("forinvsin")

        # Check if a list of driving functions were entered
        elif valid_driving_functions(user_input):
            pass

        # Print the bad input message
        else:
            bad_input_message(user_input)

def two_trace():

    print("Two-Trace Selected.")

    while True:
        user_input = session.prompt()

def wedge_trace():

    print("Wedge Trace Selected.")

    while True:
        user_input = session.prompt()

# Run the inverse single-trace algorithm
def root_mean_square():

    print("Root Mean Square Mode:")

    while True:
        user_input = session.prompt()

def main():

    # Create a dictionary of response-function pairs for the 'main' menu
    algorithm_responses = { "forsin" : forward_single_trace,
                            "invsin" : inverse_single_trace,
                            "forinvsin" : forinv_single_trace,
                            "two" : two_trace,
                            "wedge" : wedge_trace,
                            "rms" : root_mean_square,
                          }

    # Run the prompt
    while True:

        # Do multiple input calls.
        user_input = session.prompt()

        # Check if in the response correponds with any of the Loewner algorithms
        if user_input in algorithm_responses:
            algorithm_responses[user_input]()

        # Check if in the response correponds with help/exit
        elif user_input in basic_responses:
            basic_responses[user_input](user_input)

        # Print a message if an invalid response was given
        else:
            bad_input_message(user_input)

# Create prompt object.
session = PromptSession(message=LOEWNER_PROMPT)

# Create a dictionary of input-function pairs
basic_responses = { "help" : print_help_message,
                    "h" : print_help_message,
                    "quit" : exit_loewner,
                    "q" : exit_loewner,
                    "exit" : exit_loewner,
                  }

# Create a dictionary of response-function pairs for the 'main' menu
help_responses = { "forsin" : FORSINGLE_HELPMSG,
                   "invsin" : INVSINGLE_HELPMSG,
                   "forinvsin" : FORINV_HELPMSG,
                   "two" : TWO_HELPMSG,
                   "wedge" : WEDGE_HELPMSG,
                   "help" : HELPMSG,
                   "h" : HELPMSG,
                 }


if __name__ == "__main__":
    main()

