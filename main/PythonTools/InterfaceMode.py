class InterfaceMode:

    def __init__(self,name):
        self.name = name
        self.driving_list = []

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

        # Create a list of driving functions that will be used
        self.driving_list = []

    def change_single_time(self,param,value):

        # Check if the time values are being changed
        if param in self.time_settings:

            try:
                # Attempt to convert the value to a float
                temp = float(value)
            except ValueError:
                # Return false if unsuccessful
                return False

            # Change the start time value
            if param == START_TIME:
                self.time_settings[START_TIME] = temp
                return True

            # Change the final time valie
            if param == FINAL_TIME:
                self.time_settings[FINAL_TIME] = temp
                return True

        # Return false if input doesn't match intruction to change time parameters
        return False

    def change_both_times(self,param,value1,value2):

        # Check if the times values are being changed
        if param == MULTIPLE_TIMES:

            try:
                # Attempt to convert the values to floats
                temp1 = float(value1)
                temp2 = float(value2)
            except ValueError:
                # Return false if unsuccessful
                return False

            # Change the start and final time values
            self.time_settings[START_TIME] = temp1
            self.time_settings[FINAL_TIME] = temp2
            return True

        # Return false if input doesn't match instruction to change time parameters
        return False

    def validate_time(self):

        # Create an array of time values
        time_values = self.time_settings.values()

        # Check that all the times values have been set
        if any([val is None for val in time_values]):
            self.error = "Validation error: Not all the time values have been set."
            return False

        # Check that the time values are non-negative
        if any([val < 0 for val in time_values]):
            self.error = "Validation error: One or both time values are negative."
            return False

        # Check that the final time is greater than the start time
        if self.time_settings[FINAL_TIME] <= self.time_settings[START_TIME]:
            self.error = "Validation error: Final time is equal to or smaller than start time."
            return False

        # Return true if all checks are passed
        return True

    def change_single_resolution(self,param,value):

        # Check if the resolution values are being changed
        if param in self.res_settings:

            try:
                # Attempt to convert the value to an int
                temp = int(value)
            except ValueError:
                return False

            # Change the outer resolution value
            if param == OUTER_RES:
                self.res_settings[OUTER_RES] = temp
                return True

            # Change the inner resolution value
            if param == INNER_RES:
                self.res_settings[INNER_RES] = temp
                return True

        # Return false if input doesn't match intruction to change resolution parameters
        return False

    def change_both_resolutions(self,param,value1,value2):

        # Check if the resolution values are being changed
        if param == MULTIPLE_RES:

            try:
                # Attempt to convert the value to an int
                temp1 = int(value2)
                temp2 = int(value2)
            except ValueError:
                return False

            # Change the resolution values
            self.res_settings[OUTER_RES] = temp1
            self.res_settings[INNER_RES] = temp2
            return True

        # Return false if input doesn't match intruction to change resolution parameters
        return False

    def change_saving(self,param,value):

        # See if the second argument matches a True/False response
        if value not in self.convert_bool.keys():
            return False

        # See if the first argument matches the save plots/data response
        if param in [SAVE_PLOT,SAVE_DATA]:
            self.misc_settings[param] = self.convert_bool[value]
            return True

        # Return false if input doesn't match intruction to change saving parameters
        return False

    def change_compilation(self,param,value):

        # See if the second argument matches a True/False response
        if value not in self.convert_bool.keys():
            return False

        # See if the first argument matches the compile response
        if param == COMPILE:
            self.misc_settings[param] = self.convert_bool[value]
            return True

        # Return false if input doesn't match instruction to compile or not compile the modules
        return False

    def change_kappa(self,param,value):

        # Check if the kappa value is being changed
        if param == KAPPA:

            # Attempt to convert the value to a float
            try:
                self.kappa = float(value)
            except ValueError:
                return False

        # Return false if input doesn't match instruction to change kappa value
        return False

    def change_drive_alpha(self,param,value):

        # Check if the alpha value (for c-alpha driving) is being changed
        if param == DRIVE_ALPHA:

            # Attempt to convert the value to a float
            try:
                self.drivealpha = float(value)
            except ValueError:
                return False

        # Return false if input doesn't match instruction to change alpha value
        return False

    def change_parameter(self,param,value):
        pass

    def validate_settings(self):
        pass

class SingleTrace(InterfaceMode):

    def __init__(self,name):
        InterfaceMode.__init__(name)

    def change_parameter(self,user_input):

        # Split the user input by space
        inputs = user_input.split()

        # Check if the input array has two elements
        if len(inputs) == 2:

            # Assign the parameter and value
            param = inputs[0]
            value = inputs[1]

            # See if the inputs match with an instruction to change a single parameters
            return self.change_single_time(param,value) or self.change_single_resolution(param,value) or self.change_saving(param,value) or self.change_compilation(param,value) \
                    or self.change_kappa(param,value) or self.change_drive_alpha(param,value)

        # Check if the input array has three elements
        if len(inputs) == 3:

            # Assign the parameter and values
            param = inputs[0]
            value1 = inputs[1]
            value2 = inputs[2]

            # See if the inputs match with an instruction to change multiple parameters
            return self.change_both_times(param,value1,value2) or self.change_both_resolutions(param,value1,value2)

        # Return false if input doesn't match instruction to change any of the parameters
        return False

    def validate_settings(self):

        # Check that all the validation methods return True
        return self.validate_time() and self.validate_resolution() and self.validate_saving() and self.validate_compilation() \
                and self.validate_kappa() and self.validate_drive_alpha()

