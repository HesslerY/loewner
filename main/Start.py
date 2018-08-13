from PythonTools.Constants import LOEWNER_PROMPT, FORSINGLE_HELPMSG, INVSINGLE_HELPMSG, FORINV_HELPMSG, TWO_HELPMSG, WEDGE_HELPMSG, HELPMSG, DRIVING_LIST, BACK_COMMAND
from PythonTools.LoewnerRunFactory import LoewnerRunFactory
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import button_dialog

# Print a help message
def print_help_message(msg_type):
    print(help_responses[msg_type])
    return

# Exit the program
def exit_loewner(msg_type):
    exit()

def print_driving_functions():

    for item in DRIVING_LIST:
        print(item)

# Run the forward single-trace algorithm
def forward_single_trace():

    print("Forward Single-Trace Selected.")

    # Run the prompt
    while True:

        # Print a message to the prompt
        print("Choose driving function(s) or go [b]ack?")

        # Print the driving functions
        print_driving_functions()

        # Await under input
        user_choice = session.prompt()

        # Check for 'go back' instruction
        if user_choice is in BACK_COMMANDS:
            return

        elif user_choice is in HELP_COMMANDS:
            print_help_message("forwardsingle")

        else if

# Run the inverse single-trace algorithm
def inverse_single_trace():

    print("Inverse Single-Trace Selected.")

    while True:
        user_choice = session.prompt()

# Run the forward and inverse single-trace algorithms
def forinv_single_trace():

    print("Forward and Inverse Single-Trace Selected.")

    while True:
        user_choice = session.prompt()

def two_trace():

    print("Two-Trace Selected.")

    while True:
        user_choice = session.prompt()

def wedge_trace():

    print("Wedge Trace Selected.")

    while True:
        user_choice = session.prompt()

def main():

    # Create a dictionary of response-function pairs for the 'main' menu
    algorithm_responses = { "forwardsingle" : forward_single_trace,
                            "inversesingle" : inverse_single_trace,
                            "forinvsingle" : forinv_single_trace,
                            "two" : two_trace,
                            "wedge" : wedge_trace,
                          }

    # Run the prompt
    while True:

        # Do multiple input calls.
        user_choice = session.prompt()

        # Check if in the response correponds with any of the Loewner algorithms
        if user_choice in algorithm_responses:
            algorithm_responses[user_choice]()

        # Check if in the response correponds with help/exit
        elif user_choice in basic_responses:
            basic_responses[user_choice](user_choice)

        else:
            # Print a message if an invalid response was given
            print("Unrecognised instruction: " + user_choice + " (Press h for help)")

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
help_responses = { "forwardsingle" : FORSINGLE_HELPMSG,
                   "inversesingle" : INVSINGLE_HELPMSG,
                   "forinvsingle" : FORINV_HELPMSG,
                   "two" : TWO_HELPMSG,
                   "wedge" : WEDGE_HELPMSG,
                   "help" : HELPMSG,
                   "h" : HELPMSG,
                 }


if __name__ == "__main__":
    main()

