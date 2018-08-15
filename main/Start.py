from PythonTools.Constants import LOEWNER_PROMPT, FORSINGLE_HELPMSG, INVSINGLE_HELPMSG, FORINV_HELPMSG, TWO_HELPMSG, WEDGE_HELPMSG, HELPMSG, DRIVING_LIST, BACK_COMMANDS, HELP_COMMANDS, TOTAL_DRIVING_FUNCTIONS
#from PythonTools.LoewnerRunFactory import LoewnerRunFactory
from prompt_toolkit import PromptSession
from prompt_toolkit.shortcuts import button_dialog

class CommandLineInterface:

    def __init__(self):

        # Create a dictionary of input-function pairs
        self.basic_responses = { "help" : self.print_help_message,
                                 "h" : self.print_help_message,
                                 "quit" : self.exit_loewner,
                                 "q" : self.exit_loewner,
                                 "exit" : self.exit_loewner,
                               }

        # Create a dictionary of response-function pairs for the 'main' menu
        self.help_responses = { "forsin" : FORSINGLE_HELPMSG,
                                "invsin" : INVSINGLE_HELPMSG,
                                "forinvsin" : FORINV_HELPMSG,
                                "two" : TWO_HELPMSG,
                                "wedge" : WEDGE_HELPMSG,
                                "help" : HELPMSG,
                                "h" : HELPMSG,
                              }


        # Create a dictionary of response-function pairs for the 'main' menu
        self.algorithm_responses = { "forsin" : self.forward_single_trace,
                                     "invsin" : self.inverse_single_trace,
                                     "forinvsin" : self.forinv_single_trace,
                                     "two" : self.two_trace,
                                     "wedge" : self.wedge_trace,
                                     "exact" : self.exact_solutions,
                                     "rms" : self.root_mean_square,
                                   }

        # Create prompt object.
        self.session = PromptSession(message=LOEWNER_PROMPT)

    # Exit the program
    def exit_loewner(self,msg_type):
        exit()

    # Print a help message
    def print_help_message(self,msg_type):

        help_file_loc = self.help_responses[msg_type]
        help_file = open(help_file_loc)

        for line in help_file:
            print(line.strip('\n'))

        print("")
        return

    def bad_input_message(self,user_input):
        print("Unrecognised instruction: " + user_input + " (Press h for help)")

    def print_driving_functions(self):

        # Print all driving functions and their indices
        for item in DRIVING_LIST:
            print(item)

    def print_driving_selection(self,driving_selection):

        # Print the user-selected driving functions
        for index in driving_selection:
            print(DRIVING_LIST[index])

    def validate_driving_functions(self,user_input):

        # Convert the values to integers
        try:
            driving_list = [int(item) for item in user_input.split()]
        except ValueError:
            return False

        # Check that the numbers are in the correct range
        if not all([df >= 0 and df < TOTAL_DRIVING_FUNCTIONS for df in driving_list]):
            return False

        # Return the driving list - all checks passed
        return driving_list

    def finalise_driving_choices(self,driving_list):

        # Display driving function choice
        print("Driving functions chosen:")
        self.print_driving_selection(driving_list)
        print("[a]ppend / [s]tart again / [c]ontinue?")

        while True:

            user_input = self.session.prompt()

            if user_input == "a":
                pass

            if user_input == "s":
                pass

            if user_input == "c":
                return driving_list

    # Run the forward single-trace algorithm
    def forward_single_trace(self):

        print("Forward Single-Trace Mode:")

        # Run the prompt
        while True:

            # Await under input
            user_input = self.session.prompt()

            # Check if valid driving functions were entered
            driving_list = self.validate_driving_functions(user_input)

            # Check for 'go back' instruction
            if user_input in BACK_COMMANDS:
                return

            # check for the help instruction
            elif user_input == "dr":
                self.print_driving_functions()

            # Check if in the response correponds with help/exit
            elif user_input in self.basic_responses:
                self.basic_responses[user_input](user_input)

            # Check if a list of driving functions were entered
            elif self.validate_driving_functions(user_input) is not False:
                pass

            # Print the bad input message
            else:
                self.bad_input_message(user_input)

    # Run the inverse single-trace algorithm
    def inverse_single_trace(self):

        print("Inverse Single-Trace Selected.")

        while True:

            user_input = self.session.prompt()

    # Run the forward and inverse single-trace algorithms
    def forinv_single_trace(self):

        print("Forward + Inverse Single-Trace Mode:")

        # Run the prompt
        while True:

            # Await under input
            user_input = self.session.prompt()

            # Get a list of driving functions (if any were given)
            driving_list = self.validate_driving_functions(user_input)

            # Check for 'go back' instruction
            if user_input in BACK_COMMANDS:
                return

            # check for the help instruction
            elif user_input == "dr":
                self.print_driving_functions()

            # Check if in the response correponds with help/exit
            elif user_input in self.basic_responses:
                self.basic_responses[user_input]("forinvsin")

            # Check if a list of driving functions were entered
            elif driving_list is not False:

                driving_list = self.finalise_driving_choices(driving_list)

            # Print the bad input message
            else:
                self.bad_input_message(user_input)

    def two_trace(self):

        print("Two-Trace Selected.")

        while True:
            user_input = self.session.prompt()

    def wedge_trace(self):

        print("Wedge Trace Selected.")

        while True:
            user_input = self.session.prompt()

    # Run the root-mean-sqaure algorithms
    def root_mean_square(self):

        print("Root Mean Square Mode:")

        while True:
            user_input = self.session.prompt()

    # Run the exact solution algorithms
    def exact_solutions(self):

        print("Exact Solution Mode:")

        while True:
            user_input = self.session.prompt()

    def start(self):
        # Run the prompt
        while True:

            # Do multiple input calls.
            user_input = self.session.prompt()

            # Check if in the response correponds with any of the Loewner algorithms
            if user_input in self.algorithm_responses:
                self.algorithm_responses[user_input]()

            # Check if in the response correponds with help/exit
            elif user_input in self.basic_responses:
                self.basic_responses[user_input](user_input)

            # Print a message if an invalid response was given
            else:
                self.bad_input_message(user_input)


def main():

    interface = CommandLineInterface()
    interface.start()

if __name__ == "__main__":
    main()

