import Constants

class LoewnerRun:

    def __init__(self, driving_func_index):

        # Assign the driving function index
        self.driving_func_index = driving_func_index

        # Set square root parameter to None by default
        self.square_root_param = None

        # Assign the corresponding compilation command
        self.compile_command = self.generate_compile_command()

        # Determine the start time, end time, and number of points
        self.obtain_run_parameters()

    def generate_compile_command(self):

        if self.driving_func_index not in [Constants.KAPPA_IDX, Constants.C_ALPHA_IDX]:
            return "gfortran -D CASE=" + str(self.driving_func_index) + " NumericalLoewner.F03 -o NumericalLoewner.out"

        elif self.driving_func_index == Constants.KAPPA_IDX:
            self.square_root_param = self.obtain_square_root_parameter("Please enter the desired kappa value: ")
            incomp_compile_command = "gfortran -D CASE=" + str(self.driving_func_index) + " -D KAPPA="

        elif self.driving_func_index == Constants.C_ALPHA_IDX:
            self.square_root_param = self.obtain_square_root_parameter("Please enter the desired c_alpha value: ")
            incomp_compile_command = "gfortran -D CASE=" + str(self.driving_func_index) + " -D C_ALPHA="

        else:
            # Error
            pass

        return incomp_compile_command + str(self.square_root_param) + " NumericalLoewner.F03 -o NumericalLoewner.out"

    def obtain_square_root_parameter(self, query):

        while True:

            # Ask for the square root parameter
            square_root_parameter = input(query)
    
            try:

                # Convert the input to a float
                square_root_parameter = float(square_root_parameter)

                # Return if parameter is positive
                if square_root_parameter > 0:
                    return square_root_parameter

            except ValueError:
                # Repeat if input could not be converted to float
                continue

    def obtain_run_parameters(self):

        while True:

            # Ask for the run parameters
            values = input("Please enter the start time, end time, and number of points seperated by a space: ")
        
            try:

                # Split the input
                values = values.split()

                # Ensure that three values were entered
                if len(values) != 3:
                    continue

                # Ensure that the start time and end time can be converted to float
                # Ensure that the number of points can be converted to int
                values[0] = float(values[0])
                values[1] = float(values[1])
                values[2] = int(values[2])

                # Check that the start time >= 0
                if values[0] < 0:
                    continue
                
                # Check that final time is greater than the start time
                if values[1] <= values[0]:
                    continue

                # Check that the number of points is >= 1
                if values[2] < 1:
                    continue

                # Assign run parameters
                self.start_time = values[0]
                self.final_time = values[1]
                self.num_points = values[2]
                return

            except ValueError:
                # Repeat if input had improper format
                continue
