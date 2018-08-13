from PythonTools.Constants import LOEWNER_PROMPT
from prompt_toolkit import PromptSession

# Print a help message
def print_help_message():
    print("This is a help message.")

# Run the forward single-trace algorithm
def forward_single_trace():

    print("Forward Single-Trace Selected.")

    while True:
        user_choice = session.prompt(LOEWNER_PROMPT)

# Run the inverse single-trace algorithm
def forward_single_trace():

    print("Inverse Single-Trace Selected.")

    while True:
        user_choice = session.prompt(LOEWNER_PROMPT)

# Run the forward and inverse single-trace algorithms
def forinv_single_trace():

    print("Forward and Inverse Single-Trace Selected.")

    while True:
        user_choice = session.prompt(LOEWNER_PROMPT)

def two_trace():

    print("Two-Trace Selected.")

    while True:
        user_choice = session.prompt(LOEWNER_PROMPT)

def wedge_trace():

    print("Wedge Trace Selected.")

    while True:
        user_choice = session.prompt(LOEWNER_PROMPT)

def main():

    # Create a dictionary of response-function pairs for the 'main' menu
    algorithm_responses = { "forwardsingle" : forward_single_trace,
                            "inversesingle" : inverse_single_trace,
                            "forinvsingle" : forinv_single_trace,
                            "two" : two_trace,
                            "wedge" : wedge_trace,
                          }

    while True:

        # Do multiple input calls.
        user_choice = session.prompt(LOEWNER_PROMPT)

        # Check if in the response correponds with any of the Loewner algorithms
        if user_choice in algorithm_responses:
            algorithm_responses[user_choice]()

        # Check if in the response correponds with help/exit
        elif user_choice in basic_responses:
            basic_responses[user_choice]()

        else:
            # Print a message if an invalid response was given
            print("Unrecognised instruction: " + user_choice + " (Press h for help)")

# Create prompt object.
session = PromptSession()

# Create a dictionary of input-function pairs
basic_responses = { "help" : print_help_message,
                    "h" : print_help_message,
                    "quit" : exit,
                    "q" : exit,
                    "exit" : exit,
                  }

if __name__ == "__main__":
    main()

