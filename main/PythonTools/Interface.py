from Constants import *
from LoewnerRunFactory import LoewnerRunFactory
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
        self.help_responses = {
                                "help" : HELPMSG,
                                "h" : HELPMSG,
                              }


        # Create a dictionary of response-function pairs for the 'main' menu
        self.algorithm_responses = { "forsin" : self.standard_loewner,
                                     "invsin" : self.standard_loewner,
                                     "two" : self.standard_loewner,
                                     "wedge" : self.standard_loewner,
                                     "exactsinglelinear" : self.exact_single_linear,
                                     "rms" : self.root_mean_square,
                                   }

        # Create prompt object.
        self.session = PromptSession(message=LOEWNER_PROMPT)

        # Declare 'mode' booleans - these decide which LoewnerRun algorithm to use
        self.forsingle = False
        self.invsingle = False
        self.twotrace = False
        self.wedge = False
        self.exact = False
        self.rms = False

        # Create settings of the LoewnerRunFactory
        self.time_settings =    {
                                  "starttime" : None,
                                  "finaltime" : None,
                                }

        self.res_settings =     {
                                  "outerres" : None,
                                  "innerres" : None,
                                }


        self.misc_settings =    {
                                  "compile" : None,
                                  "saveplots" : None,
                                  "savedata" : None,
                                }

        self.convert_bool = { "y" : True,
                              "n" : False,
                            }

        self.wedgealpha = 0
        self.kappa = 0
        self.drivealpha = 0
        self.constant = 0

    def exit_loewner(self,msg_type):
        # Exit the program
        exit()

    def print_help_message(self,msg_type=HELPMSG):

        # Print a help message
        help_file_loc = self.help_responses[msg_type]
        help_file = open(help_file_loc)

        for line in help_file:
            print(line.strip('\n'))

        print("")
        return ""

    def set_mode(self,mode_input):

        # Set the program mode that determines what algorithm will run
        if mode_input == "forsin":
            self.forsingle = True

        if mode_input in "invsin":
            self.invsingle = True

        if mode_input == "two":
            self.twotrace = True

        if mode_input == "wedge":
            self.wedge = True

        if mode_input == "exact":
            self.exact = True

        if mode_input == "rms":
            self.rms = True

    def standard_input(self):

        # Await the 'standard' input - help or quit
        while True:

            user_input = self.session.prompt()

            if user_input in self.basic_responses:
                user_input = self.basic_responses[user_input](user_input)

            return user_input

    def bad_input_message(self,user_input):
        # Print a message for unexpected inputs
        print("Unrecognised instruction: " + user_input + " (Press h for help)")

    def change_parameter(self,user_input):

        # Change one of the parameters that governs the LoewnerRunFactory
        inputs = user_input.split()

        if len(inputs) != 2:
            return

        if inputs[0] == "kappa":
            try:
                temp = float(inputs[1])
            except ValueError:
                return
            if temp > 0:
                self.kappa = temp
                return True

        if inputs[0] == "drivealpha":
            try:
                temp = float(inputs[1])
            except ValueError:
                return
            if temp > 0:
                self.drivealpha = temp
                return True

        if inputs[0] == "wedgealpha":
            try:
                temp = float(inputs[1])
            except ValueError:
                return
            if temp > 0:
                self.wedgealpha = temp
                return True

        if inputs[0] in self.time_settings:

            try:
                temp = float(inputs[1])
            except ValueError:
                return

            if inputs[0] == "starttime":
                if temp >= 0:
                    self.time_settings["starttime"] = temp
                    return True

            elif inputs[0] == "finaltime":
                if temp > 0:
                    self.time_settings["finaltime"] = temp
                    return True

        if inputs[0] in self.res_settings:

            try:
                temp = int(inputs[1])
            except ValueError:
                return

            if inputs[0] == "outerres":
                if temp > 0:
                    self.res_settings["outerres"] = temp
                    return True

            elif inputs[0] == "innerres":
                if temp > 0:
                    self.res_settings["innerres"] = temp
                    return True

        if inputs[0] in self.misc_settings:
            if inputs[1] in self.convert_bool.keys():
                self.misc_settings[inputs[0]] = self.convert_bool[inputs[1]]
                return True

        return False

    def create_factory(self,driving_list):

        # Validate and create a LoewnerRunFactory
        if any([val is None for val in self.time_settings.values()]):
            return False

        if any([val is None for val in self.res_settings.values()]):
            return False

        if any([val is None for val in self.misc_settings.values()]):
            return False

        if self.time_settings["starttime"] < 0:
            return False

        if self.time_settings["finaltime"] <= self.time_settings["starttime"]:
            return False

        if self.res_settings["outerres"] < 1:
            return False

        if self.res_settings["innerres"] < 1:
            return False

        if not any(self.misc_settings.values()):
            return False

        if CALPHA_IDX in driving_list:
            if self.drivealpha == 0:
                return False

        if KAPPA_IDX in driving_list:
            if self.kappa == 0:
                return False

        if CONST_IDX in driving_list:
            if self.constant == None:
                return False

        self.loewner_fact = LoewnerRunFactory(self.time_settings["starttime"],self.time_settings["finaltime"],self.res_settings["outerres"],self.res_settings["innerres"],self.misc_settings["compile"],self.misc_settings["savedata"],self.misc_settings["saveplots"])

        self.loewner_fact.alpha = self.drivealpha
        self.loewner_fact.kappa = self.kappa
        self.loewner_fact.constant = self.constant

        return True

    def create_loewner_runs(self,driving_list):
        # Create LoewnerRuns with the LoewnerRunFactory depending on the user's selections
        return [self.loewner_fact.select_single_run(index=i) for i in driving_list]

    def print_driving_functions(self):

        # Print all driving functions and their indices
        for item in DRIVING_LIST:
            print(item)

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

    # Run the forward and inverse single-trace algorithms
    def standard_loewner(self):

        # Run the prompt
        while True:

            # Await under input
            user_input = self.standard_input()

            # Attempt to change the LoewenerRunFactory parameters
            if self.change_parameter(user_input):
                continue

            # Check for 'go back' instruction
            if user_input in BACK_COMMANDS:
                return

            # Get a list of driving functions (if any were given)
            driving_list = self.validate_driving_functions(user_input)

            # check for the help instruction
            if user_input == "dr":
                self.print_driving_functions()
                continue

            # Check if in the response correponds with help/exit
            if user_input in self.basic_responses:
                self.basic_responses[user_input]()
                continue

            # Check if a list of driving functions were entered
            if driving_list is not False:

                if self.create_factory(driving_list):
                    print("Successfully initialised LoewnerRun factory.")
                else:
                    print("Could not create LoewnerRun factory. Bad or incomplete parameters given.")
                    continue

                if self.wedge and self.wedgealpha <= 0:
                    print("Can't use wedgde mode with wedge alpha value:" + str(self.wedgealpha))
                    continue

                # Create a list of LoewnerRuns from the LoewnerRunFactory
                loewner_runs = self.create_loewner_runs(driving_list)
                print("Successfully created LoewnerRuns for driving functions " + " ".join([str(i) for i in driving_list]))

                # Carry out the 'standard' runs (drving functions for which there are no extra parameters)
                for run in loewner_runs:

                    if self.forsingle or self.invsingle:

                        run.quadratic_forward_loewner()

                        if self.forsingle:
                            print("Finished single-trace forward for driving function " + str(run.name))

                    if self.invsingle:

                        run.quadratic_inverse_loewner()
                        print("Finished single-trace inverse for driving function " + str(run.name))

                    if self.wedge and self.wedgealpha > 0:

                        run.wedge_growth(self.wedgealpha)
                        print("Finished wedge-trace for driving function " + str(run.name))

                    if self.twotrace:

                        run.cubic_forward_loewner()
                        print("Finished two-trace for driving function " + str(run.name))

                print("Runs completed successfully.")
                exit()

            # Print the bad input message
            self.bad_input_message(user_input)

    # Run the root-mean-sqaure algorithms
    def root_mean_square(self):

        while True:

            user_input = self.standard_input()

            # Check for 'go back' instruction
            if user_input in BACK_COMMANDS:
                return

    # Run the exact solution algorithms
    def exact_solutions(self):

        while True:
            user_input = self.standard_input()

            # Check for 'go back' instruction
            if user_input in BACK_COMMANDS:
                return

    def start(self):

        # Run the prompt
        while True:

            # Do multiple input calls.
            user_input = self.standard_input()

            # Check if in the response correponds with any of the Loewner algorithms
            if user_input in self.algorithm_responses:
                self.set_mode(user_input)
                self.algorithm_responses[user_input]()

            # Check if in the response correponds with help/exit
            elif user_input in self.basic_responses:
                self.basic_responses[user_input](user_input)

            # Print a message if an invalid response was given
            else:
                self.bad_input_message(user_input)

