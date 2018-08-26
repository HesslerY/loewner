from Constants import *
from LoewnerRunFactory import LoewnerRunFactory
from prompt_toolkit import PromptSession
from os import popen
from numpy import arange, linspace
from InterfaceMode import *

class CommandLineInterface:

    def __init__(self):

        # Create a dictionary of input-function pairs
        self.basic_responses = {
                                    HELP_FULL : self.print_help_message,
                                    HELP_SHORT : self.print_help_message,
                                    QUIT_FULL : self.exit_loewner,
                                    QUIT_SHORT : self.exit_loewner,
                                    EXIT : self.exit_loewner,
                               }

        # Create a dictionary of input-message pairs for the help command
        self.help_responses = {
                                    HELP_FULL : HELPMSG,
                                    HELP_SHORT : HELPMSG,
                              }


        # Create a dictionary of input-object pairs for the main algorithms/modes
        self.algorithm_responses = {
                                        FORWARD_SINGLE_MODE : ForwardSingle,
                                        INVERSE_SINGLE_MODE : InverseSingle,
                                        EXACT_INVERSE_MODE : ExactInverse,
                                        TWO_TRACE_MODE : TwoTrace,
                                        WEDGE_TRACE_MODE : WedgeAlpha,
                                        EXACT_LINEAR : ExactLinear,
                                        EXACT_CONST : ExactConstant,
                                   }

        # Create prompt object.
        self.session = PromptSession(message=LOEWNER_PROMPT)

        # Find the size of the terminal
        rows, columns = popen('stty size', 'r').read().split()

        # Declare a string for placing text in the center of the terminal
        self.shift_string = "{:^" + str(columns) + "}"

        # Create an empty variable for representing the program mode
        self.program_mode = None

    def exit_loewner(self,unused_arg):
        # Exit the program
        exit()

    def is_blank(self,user_input):
        return user_input == ""

    def print_help_message(self,msg_type=HELPMSG):

        # Determine the location of the help file
        help_file_loc = self.help_responses[msg_type]

        # Open the help file
        help_file = open(help_file_loc)

        # Print the help file
        for line in help_file:
            print(line.strip('\n'))

        # Add a blank line to make things look neater
        print("")

        # Clear the input to indicate that it was interpreted successfully
        return ""

    def special_text(self, style, string):

        styles = {"PURPLE" : '\033[95m',
                  "CYAN" : '\033[96m',
                  "DARKCYAN" : '\033[36m',
                  "BLUE" : '\033[94m',
                  "GREEN" : '\033[92m',
                  "YELLOW" : '\033[93m',
                  "RED" : '\033[91m',
                  "BOLD" : '\033[1m',
                  "UNDERLINE" : '\033[4m',}

        return styles[style] + string + '\033[0m'

    def standard_input(self):

        # Await the 'standard' input - help/quit/print driving functions/etc
        while True:

            user_input = self.session.prompt()

            if user_input in self.basic_responses:
                user_input = self.basic_responses[user_input](user_input)

            return user_input

    def bad_input_message(self,user_input):

        # Print a message for unexpected inputs
        print("Unrecognised instruction: " + user_input + " (Press h for help)")

    def run_algorithm(self,user_input):
        return user_input == START_ALG

    # Run the forward and inverse single-trace algorithms
    def run_loewner(self):

        # Run the prompt
        while True:

            # Await under input
            user_input = self.standard_input()

            # Continue if one of the standard inputs or a blank line was entered
            if self.is_blank(user_input):
                continue

            # Check for 'go back' instruction
            if user_input in BACK_COMMANDS:
                return

            # Attempt to change the LoewenerRunFactory parameters
            if self.program_mode.change_parameters(user_input):
                continue

            # Get a list of driving functions (if any were given)
            if self.program_mode.change_driving_functions(user_input):
                continue

            # Print the error message if something went wrong
            if self.program_mode.show_error(user_input):
                continue

            # Check if the start command was given
            if self.run_algorithm(user_input):

                # Validate the run parameters that were given and create a LoewnerRunFactory
                if not self.program_mode.validate_settings():
                    print("Could not create validate configuration: Bad or incomplete parameters given. Enter 'error' for more information.")
                    continue
                else:
                    print("Successfully validated configuration. Executing runs...")
                    self.program_mode.execute()
                    return

            # Print the bad input message
            self.bad_input_message(user_input)

    def show_start_screen(self):

        # Open the start message file
        start_file = open(START_MSG)

        # Print the help file
        for line in start_file:
            print(line.strip('\n'))

        # Add a blank line to make things look neater
        print("")

        print(self.shift_string.format(self.special_text("BOLD","*Loewner's Evolutions*")))
        print(self.shift_string.format("Numerical and exact solutions to Loewner's equation for two and single-trace evolutions."))

        # Add a blank line to make things look neater
        print("")

        # Clear the input to indicate that it was interpreted successfully
        return ""

    def start(self):

        # Show a start screen
        self.show_start_screen()

        # Run the prompt
        while True:

            # Check if the input matches with the 'standard' commands
            user_input = self.standard_input()

            # Continue if one of the standard commands was entered
            if self.is_blank(user_input):
                continue

            # Check if in the response correponds with any of the Loewner algorithms
            if user_input in self.algorithm_responses:

                # Create a program mode object
                self.program_mode = self.algorithm_responses[user_input]()

                # Prepare and execute the algorithm of the current mode
                self.run_loewner()

                # Delete the program mode object to allow the use of a different algorithm
                self.program_mode = None
                continue

            # Print a message if an invalid response was given
            self.bad_input_message(user_input)

