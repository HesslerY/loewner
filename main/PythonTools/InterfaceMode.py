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

    def change_time(self,param,value):

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

    def change_two_time(self,param,value1,value2):

        if param == MULTIPLE_TIMES:

            try:
                # Attempt to convert the values to floats
                temp1 = float(value1)
                temp2 = float(value2)
            except ValueError:
                # Return false if unsuccessful
                return False

            # Change the start time value
            self.time_settings[START_TIME] = temp1
            self.time_settings[FINAL_TIME] = temp2
            return True

        return False

    def change_resolution(self,param,value):

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

            # See if the inputs match with an instruction to change the parameters
            return self.change_time(param,value) or self.change_resolution(param,value) or self.change_saving(param,value) or self.change_compilation(param,value)

    def validate_settings(self):
