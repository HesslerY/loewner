from Constants import *
from LoewnerRunFactory import LoewnerRunFactory
from prompt_toolkit import PromptSession
from os import popen
from numpy import arange, linspace

class CommandLineInterface:

    def __init__(self):

        # Create a dictionary of input-function pairs
        self.basic_responses = {
                                    HELP_FULL : self.print_help_message,
                                    HELP_SHORT : self.print_help_message,
                                    QUIT_FULL : self.exit_loewner,
                                    QUIT_SHORT : self.exit_loewner,
                                    DRIVING_FUNCTIONS : self.print_driving_functions,
                                    EXIT : self.exit_loewner,
                               }

        # Create a dictionary of input-message pairs for the help command
        self.help_responses = {
                                    HELP_FULL : HELPMSG,
                                    HELP_SHORT : HELPMSG,
                              }


        # Create a dictionary of input-function pairs for the main algorithms/modes
        self.algorithm_responses = {
                                        FORWARD_SINGLE_MODE : self.standard_loewner,
                                        INVERSE_SINGLE_MODE : self.standard_loewner,
                                        EXACT_INVERSE_MODE : self.standard_loewner,
                                        TWO_TRACE_MODE : self.standard_loewner,
                                        WEDGE_TRACE_MODE : self.standard_loewner,
                                        EXACT_MODE : self.standard_loewner,
                                        KAPPA_MODE : self.standard_loewner,
                                        CALPHA_MODE : self.standard_loewner,
                                        ERROR_MODE : self.root_mean_square,
                                   }

        # Create prompt object.
        self.session = PromptSession(message=LOEWNER_PROMPT)

        # Declare 'mode' booleans - these decide which LoewnerRun algorithm to use
        self.program_mode = {
                                FORWARD_SINGLE_MODE : False,
                                INVERSE_SINGLE_MODE : False,
                                EXACT_INVERSE_MODE : False,
                                TWO_TRACE_MODE : False,
                                WEDGE_TRACE_MODE : False,
                                EXACT_MODE : False,
                                KAPPA_MODE : False,
                                CALPHA_MODE : False,
                                ERROR_MODE : False,
                            }

        # Create settings of the LoewnerRunFactory
        self.time_settings =    {
                                    START_TIME : None,
                                    FINAL_TIME : None,
                                }

        self.res_settings =     {
                                    OUTER_RES : None,
                                    INNER_RES : None,
                                }


        self.misc_settings =    {
                                    COMPILE : None,
                                    SAVE_PLOTS : None,
                                    SAVE_DATA : None,
                                }

        # Create a dictionary to match user-input to boolean values
        self.convert_bool = {
                                USER_TRUE : True,
                                USER_FALSE : False,
                            }

        self.driving_list = []

        # Declare other variables that will be passed to the LoewnerRun factory
        self.wedgealpha = 0
        self.kappa = 0
        self.drivealpha = 0
        self.constant = 0

        # Create booleansto-be for exact solution runs
        self.linearexplicit = None
        self.linearimplicit = None

        self.phi =    {
                          START_PHI : None,
                          FINAL_PHI : None,
                      }


        self.kappas = []
        self.drivealphas = []

        # Find the size of the terminal
        rows, columns = popen('stty size', 'r').read().split()

        # Declare a string for placing text in the center of the terminal
        self.shift_string = "{:^" + str(columns) + "}"

    def exit_loewner(self,unused_arg):
        # Exit the program
        exit()

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

    def set_mode(self,mode_input):

        # Set the program mode that determines what algorithm will run
        self.program_mode[mode_input] = True

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

    def show_error(self,user_input):

        if user_input != DISP_ERROR:
            return False

        print(self.error)
        return True

    def standard_input(self):

        # Await the 'standard' input - help/quit/print driving functions/etc
        while True:

            user_input = self.session.prompt()

            if user_input in self.basic_responses:
                user_input = self.basic_responses[user_input](user_input)

            return user_input

    def is_blank(self,user_input):
        return user_input == ""

    def multiple_times(self, inputs):

        # Check that the input array consists of three entries
        if len(inputs) != 3:
            return False

        # Check that the first argument is the multiple-time argument string
        if inputs[0] != MULTIPLE_TIMES:
            return False

        # Attempt to convert the second and third arguments to floats
        try:

            # This still permits bad/negative values, but validation occurs in the next step so it will be caught then
            self.time_settings[START_TIME] = float(inputs[1])
            self.time_settings[FINAL_TIME] = float(inputs[2])

        except ValueError:

            # Return false if the values could not be converted to floats
            return False

        # Return true if basic validation was successful
        return True

    def multiple_resolutions(self, inputs):

        # Check that the input array consists of three entries
        if len(inputs) != 3:
            return False

        # Check that the first argument is the multiple-resolution argument string
        if inputs[0] != MULTIPLE_RES:
            return False

        # Attempt to convert the second and third arguments to ints
        try:

            # This still permits bad/negative values, but validation occurs in the next step so it will be caught then
            self.res_settings[OUTER_RES] = int(inputs[1])
            self.res_settings[INNER_RES] = int(inputs[2])

        except ValueError:

            # Return false if the values could not be converted to ints
            return False

        # Return true if basic validation was successful
        return True

    def bad_input_message(self,user_input):

        # Print a message for unexpected inputs
        print("Unrecognised instruction: " + user_input + " (Press h for help)")

    def change_parameter(self,user_input):

        # Change one of the parameters that governs the LoewnerRunFactory
        inputs = user_input.split()

        # Return false if the input does not consist of two strings and doesn't contain multiple arguments
        if len(inputs) != 2:
            return self.multiple_times(inputs) or self.multiple_resolutions(inputs)

        if inputs[0] == KAPPA:
            try:
                temp = float(inputs[1])
            except ValueError:
                return False
            if temp > 0:
                self.kappa = temp
                return True

        if inputs[0] == DRIVE_ALPHA:
            try:
                temp = float(inputs[1])
            except ValueError:
                return False
            if temp > 0:
                self.drivealpha = temp
                return True

        if self.program_mode[WEDGE_TRACE_MODE]:

            if inputs[0] == WEDGE_ALPHA:
                try:
                    temp = float(inputs[1])
                except ValueError:
                    return False
                if temp > 0:
                    self.wedgealpha = temp
                    return True

        if inputs[0] in self.time_settings:

            try:
                temp = float(inputs[1])
            except ValueError:
                return False

            if inputs[0] == START_TIME:
                if temp >= 0:
                    self.time_settings[START_TIME] = temp
                    return True

            elif inputs[0] == FINAL_TIME:
                if temp > 0:
                    self.time_settings[FINAL_TIME] = temp
                    return True

        if inputs[0] in self.res_settings:

            try:
                temp = int(inputs[1])
            except ValueError:
                return False

            if inputs[0] == OUTER_RES:
                if temp > 0:
                    self.res_settings[OUTER_RES] = temp
                    return True

            elif inputs[0] == INNER_RES:
                if temp > 0:
                    self.res_settings[INNER_RES] = temp
                    return True

        if inputs[0] in self.misc_settings:
            if inputs[1] in self.convert_bool.keys():
                self.misc_settings[inputs[0]] = self.convert_bool[inputs[1]]
                return True

        if self.program_mode[EXACT_MODE]:

            if inputs[0] in self.phi:

                try:
                    temp = float(inputs[1])
                    if temp >= 0:
                        self.phi[inputs[0]] = temp
                        return True
                    else:
                        return False
                except ValueError:
                    return False

            if inputs[0] == LINR_IM:
                if inputs[1] in self.convert_bool.keys():
                    self.linearimplicit = self.convert_bool[inputs[1]]
                    return True

            if inputs[0] == LINR_EX:
                if inputs[1] in self.convert_bool.keys():
                    self.linearexplicit = self.convert_bool[inputs[1]]
                    return True

        return False

    def only_exact_implicit(self):
        return self.program_mode[EXACT_MODE] and len(self.driving_list) == 1 and LINR_IDX in self.driving_list and self.linearexplicit

    def validate_configuration(self):

        # Clear the error message string
        self.error = None

        only_exact_implicit = self.only_exact_implicit()

        # Check that all of the relevant parameters have been set to something
        if not only_exact_implicit and any([val is None for val in self.time_settings.values()]):
            self.error = "Validation error: Not all the time values have been set."
            return False

        if not self.program_mode[EXACT_INVERSE_MODE] and not self.program_mode[EXACT_MODE]:
            if any([val is None for val in self.res_settings.values()]):
                self.error = "Validation error: Not all the resolution values have been set."
                return False

        elif self.res_settings[OUTER_RES] is None:
            self.error = "Validation error: Resolution value hasn't been set."
            return False

        if self.program_mode[KAPPA_MODE] or self.program_mode[CALPHA_MODE]:
            self.misc_settings[COMPILE] =  True

        if not self.program_mode[EXACT_INVERSE_MODE] and not self.program_mode[EXACT_MODE] and not self.program_mode[WEDGE_TRACE_MODE]:
            if any([val is None for val in self.misc_settings.values()]):
                self.error = "Validation error: Compilation and/or saving values haven't been set."
                return False

        elif not any([self.misc_settings[SAVE_PLOTS], self.misc_settings[SAVE_DATA]]):
            self.error = "Validation error: Not all saving values have been set."
            return False

        # Check that the start time is greater than zero
        if not only_exact_implicit and self.time_settings[START_TIME] < 0:
            self.error = "Validation error: Negative start time."
            return False

        # Check that the final time is greater than the start time
        if not only_exact_implicit and self.time_settings[FINAL_TIME] <= self.time_settings[START_TIME]:
            self.error = "Validation error: Final time is less than or equal to start time."
            return False

        # Check that the outer resolution is at least 1
        if self.res_settings[OUTER_RES] < 1:
            self.error = "Validation error: Outer resolution is less than one."
            return False

        # Check that the inner resolution is at least 1
        if not self.program_mode[EXACT_INVERSE_MODE] and not self.program_mode[EXACT_MODE]:
            if self.res_settings[INNER_RES] < 1:
                self.error = "Validation error: Inner resolution is less than one."
                return False

        # Check that that user has chosen at least one form of saving (data or plot)
        if not any([self.misc_settings[SAVE_DATA], self.misc_settings[SAVE_PLOTS]]):
            self.error = "Validation error: Both saving options have been set to false. This means the program will run without preserving its output. Set at least one to true."
            return False

        # Check that c-alpha driving is being run with a suitable value
        if CALPHA_IDX in self.driving_list:
            if self.drivealpha <= 0:
                self.error = "Validation error: C-Alpha driving was chosen but alpha value is <= 0."
                return False

        # Check that kappa driving is being run with a suitable value
        if KAPPA_IDX in self.driving_list:
            if self.kappa == 0:
                self.error = "Validation error: Kappa driving was chosen but kappa value is <= 0."
                return False

        # Check that constant driving is being run with a suitable value
        if CONST_IDX in self.driving_list:
            if self.constant == None:
                self.error = "Validation error: Constant driving was chosen but constant value wasn't set."
                return False

        # Check that the wedge algorithm is being run with a suitable value
        if self.program_mode[WEDGE_TRACE_MODE] and self.wedgealpha <= 0:
            self.error = "Validation error: Wedge mode was chosen but wedge angle value is <= 0."
            return False

        if self.program_mode[EXACT_MODE] and LINR_IDX in self.driving_list and self.linearexplicit:
            if any([val is None for val in list(self.phi.values())]):
                self.error = "Validation error: Not all phi values have been set for linear exact solution."
                return False

            if self.phi[START_PHI] < 0:
                self.error = "Validation error: Start phi has a value less than zero."
                return False

            if self.phi[FINAL_PHI] <= self.phi[START_PHI]:
                self.error = "Validation error: Final phi is smaller than or equal to start phi."
                return False

        if only_exact_implicit:
            self.time_settings[START_TIME] = 0
            self.time_settings[FINAL_TIME] = 0

        # Create the LoewnerRunFactory object with the user-given parameters
        self.loewner_fact = LoewnerRunFactory(self.time_settings[START_TIME],self.time_settings[FINAL_TIME],self.res_settings[OUTER_RES],self.res_settings[INNER_RES],self.misc_settings[COMPILE],self.misc_settings[SAVE_DATA],self.misc_settings[SAVE_PLOTS])

        # Set the 'extra' parameters of the LoewnerRunFactory
        self.loewner_fact.alpha = self.drivealpha
        self.loewner_fact.kappa = self.kappa

        if self.program_mode[EXACT_MODE]:
            self.loewner_fact.constant = 1
        else:
            self.loewner_fact.constant = self.constant

        # Return true to indicate that it was created successfully
        return True

    def create_loewner_runs(self):

        # Create LoewnerRuns with the LoewnerRunFactory depending on the user's selections
        if self.program_mode[KAPPA_MODE]:
            return self.loewner_fact.vary_kappa(self.kappas)

        if self.program_mode[CALPHA_MODE]:
            return self.loewner_fact.vary_alpha(self.drivealphas)

        return [self.loewner_fact.select_single_run(index=i) for i in self.driving_list]

    def print_driving_functions(self, unused_arg):

        print("List of avaliable driving functions and their indices:")
        print("Note: Not all of these are avaliable in every mode. See instructions or enter help for more information.")

        # Print all driving functions and their indices
        for item in DRIVING_LIST:
            print(item)

        # Clear input to indicate that it has been interpreted successfully
        return ""

    def run_algorithm(self,user_input):
        return user_input == START_ALG

    def create_driving_list(self,user_input):

        # Seperate the inputs by space
        inputs = user_input.split()

        # Determine if the first argument is the command for creating a list of driving functions to be run
        if inputs[0] != CREATE_DRIVING_LIST:
            return False

        # Convert the values to integers
        try:
            driving_list = [int(item) for item in inputs[1:]]
        except ValueError:
            return False

        # Check that the numbers are in the correct range
        if not self.program_mode[WEDGE_TRACE_MODE]:
            if not all([df >= 0 and df < TOTAL_DRIVING_FUNCTIONS for df in driving_list]):
                return False

        elif self.program_mode[EXACT_MODE]:
            if not all([df in ALL_EXACT_IDX for df in driving_list]):
                return False

        else:
            if not all([df in NOTORIGIN_IDXS for df in driving_list]):
                return False

        # Create the driving list - all checks passed
        self.driving_list = driving_list
        return True

    def print_driving_list(self,user_input):

        if user_input != PRINT_DRIVING_LIST:
            return False

        print("Current driving list selection:")

        for i in range(len(self.driving_list)):
            print(DRIVING_LIST[i])

        print("Enter 'clear' to erase.")

    def clear_driving_list(self,user_input):

        # Check if an instruction to clear the driving list has been given
        if user_input == CLEAR_DRIVING:
            self.driving_list = []
            return True

        return False

    def set_drive_alphas(self, user_input):

        # Return false if the program is not in kappa mode
        if not self.program_mode[CALPHA_MODE]:
            return False

        # Split the user input
        inputs = user_input.split()

        # Return false if the first argument is not the kappa string
        if inputs[0] != CALPHAS:
            return False

        # Attempt to convert the next two strings to a starting kappa and a final kappa
        try:
            startalpha = float(inputs[1])
            finalalpha = float(inputs[2])
        except ValueError:
            return False

        if startalpha <= 0:
            return False

        if finalalpha <= startalpha:
            return False

        if finalalpha >= 1:
            return False

        # See if the next argument indicates a step value, or a number of kappa runs
        if inputs[3] not in [SQRT_STEP, NUM_SQRT_RUNS]:
            return False

        if inputs[3] == SQRT_STEP:

            try:
                increment = float(inputs[4])

                if increment <= 0:
                    return False

                self.drivealphas = arange(startalpha,finalalpha,increment)
            except ValueError:
                return False

        if inputs[3] == NUM_SQRT_RUNS:

            try:
               num_steps = int(inputs[4])

               if num_steps <= 0:
                   return False

               self.drivealphas = linspace(startalpha,finalalpha,num_steps)
            except ValueError:
                return False

        return True

    def set_kappas(self,user_input):

        # Return false if the program is not in kappa mode
        if not self.program_mode[KAPPA_MODE]:
            return False

        # Split the user input
        inputs = user_input.split()

        # Return false if the first argument is not the kappa string
        if inputs[0] != KAPPAS:
            return False

        # Attempt to convert the next two strings to a starting kappa and a final kappa
        try:
            startkappa = float(inputs[1])
            finalkappa = float(inputs[2])
        except ValueError:
            return False

        if startkappa <= 0:
            return False

        if finalkappa <= startkappa:
            return False

        # See if the next argument indicates a step value, or a number of kappa runs
        if inputs[3] not in [SQRT_STEP, NUM_SQRT_RUNS]:
            return False

        if inputs[3] == SQRT_STEP:

            try:
                increment = float(inputs[4])

                if increment <= 0:
                    return False

                self.kappas = arange(startkappa,finalkappa,increment)
            except ValueError:
                return False

        if inputs[3] == NUM_SQRT_RUNS:

            try:
               num_steps = int(inputs[4])

               if num_steps <= 0:
                   return False

               self.kappas = linspace(startkappa,finalkappa,num_steps)
            except ValueError:
                return False

        return True

    # Run the forward and inverse single-trace algorithms
    def standard_loewner(self):

        # Run the prompt
        while True:

            # Await under input
            user_input = self.standard_input()

            # Continue if one of the standard inputs was entered
            if self.is_blank(user_input):
                continue

            # Check for 'go back' instruction
            if user_input in BACK_COMMANDS:
                return

            # Attempt to change the LoewenerRunFactory parameters
            if self.change_parameter(user_input):
                continue

            # Get a list of driving functions (if any were given)
            if self.create_driving_list(user_input):
                continue

            # Print a list of the current driving-list to be used with the algorithm that the user has chosen
            if self.print_driving_list(user_input):
                continue

            # Print a list of the current driving-list to be used with the algorithm that the user has chosen
            if self.print_driving_list(user_input):
                continue

            # Print the error message if something went wrong
            if self.show_error(user_input):
                continue

            # Set a range of kappas (kappa mode)
            if self.set_kappas(user_input):
                continue

            # Set a range of alphas (calpha mode)
            if self.set_drive_alphas(user_input):
                continue

            # Check if the start command was given
            if self.run_algorithm(user_input):

                # Validate the run parameters that were given and create a LoewnerRunFactory
                if self.validate_configuration():
                    print("Successfully initialised a LoewnerRunFactory.")
                else:
                    #
                    print("Could not create validate configuration: Bad or incomplete parameters given. Enter 'error' for more information.")
                    continue

                # Create a list of LoewnerRuns from the LoewnerRunFactory
                loewner_runs = self.create_loewner_runs()
                print("Successfully created LoewnerRuns for driving functions " + " ".join([str(i) for i in self.driving_list]))

                # Carry out the desired runs
                for run in loewner_runs:

                    if self.program_mode[EXACT_MODE]:

                        # Run the two-trace exact solution for xi(t) = 1 or xi(t) = sqrt(1 + t)
                        if run.index == CONST_IDX or run.index == SQRTPLUS_IDX:
                            run.exact_cubic_forward_loewner()

                        # Run the single-trace exact solutions for xi(t) = t
                        if run.index == LINR_IDX:

                            if self.linearexplicit:
                                run.phi_quadratic_exact(self.phi[START_PHI], self.phi[FINAL_PHI])

                            if self.linearimplicit:
                                run.exact_quadratic_forward_loewner()

                    if self.program_mode[FORWARD_SINGLE_MODE] or self.program_mode[INVERSE_SINGLE_MODE] or self.program_mode[KAPPA_MODE] or self.program_mode[CALPHA_MODE]:

                        # Run the single-trace forward algorithm
                        run.quadratic_forward_loewner()

                        if self.program_mode[FORWARD_SINGLE_MODE]:
                            print("Finished single-trace forward for driving function " + str(run.name))

                    if self.program_mode[INVERSE_SINGLE_MODE]:

                        # Run the single-trace inverse algorithm
                        run.quadratic_inverse_loewner()
                        print("Finished single-trace inverse for driving function " + str(run.name))

                    if self.program_mode[EXACT_INVERSE_MODE]:

                        # Run the exact inverse algorithm
                        run.exact_inverse()
                        print("Finished exact inverse for driving function " + str(run.name))

                    if self.program_mode[WEDGE_TRACE_MODE]:

                        # Run the wedge-trace algorithm
                        run.wedge_growth(self.wedgealpha)
                        print("Finished wedge-trace for driving function " + str(run.name))

                    if self.program_mode[TWO_TRACE_MODE]:

                        # Run the two-trace algorithm
                        run.cubic_forward_loewner()
                        print("Finished two-trace for driving function " + str(run.name))

                print("Runs completed successfully.")
                # Change all modes back to null here.
                # Change all parameters back to zero here.
                return

            # Print the bad input message
            self.bad_input_message(user_input)

    # Run the root-mean-sqaure algorithms
    def root_mean_square(self):

        while True:

            user_input = self.standard_input()

            # Check for 'go back' instruction
            if user_input in BACK_COMMANDS:
                return

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
                self.set_mode(user_input)
                self.algorithm_responses[user_input]()
                continue

            # Print a message if an invalid response was given
            self.bad_input_message(user_input)

