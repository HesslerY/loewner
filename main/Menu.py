import npyscreen
import curses
import Constants
from LoewnerRun import LoewnerRun
from LoewnerRun import SqrtLoewnerRun

loewner_runs = []
sqrt_bool = [False, False]

def selection_contains_squareroot(selections):

    global sqrt_bool
    indices = [Constants.DRIVING_INDICES[selection] for selection in selections]

    if (Constants.KAPPA_IDX in indices):
        sqrt_bool[0] = True

    if (Constants.C_ALPHA_IDX in indices):
        sqrt_bool[1] = True

def create_loewner_runs(selections):

    global loewner_runs

    for selection in selections:

        index = Constants.DRIVING_INDICES[selection]

        if Constants.squareroot_driving(index):
            loewner_runs.append(SqrtLoewnerRun(index))

        else:
            loewner_runs.append(LoewnerRun(index))

class RunLoewner(npyscreen.NPSAppManaged):

    def onStart(self):

        self.addForm("MAIN", LoewnerOptions, name="Loewner's Equation")
        self.addForm("SELECTSTANDARD", DrivingOptions, name="Loewner's Equation")

    def change_form(self, name):

        self.switchForm(name)

class LoewnerOptions(npyscreen.ActionForm):

    def create(self):

        self.option = self.add(npyscreen.TitleSelectOne, max_height=3, value = [1,], name="Pick One",
                values = Constants.RUN_OPTIONS, scroll_exit=True)

    def on_ok(self):

        selection = self.option.get_selected_objects()[0]
        self.change_forms(selection)

    def on_cancel(self):

        self.parentApp.switchForm(None)

    def change_forms(self, selection):

        if selection == "Standard Mode":
            change_to = "SELECTSTANDARD"

        elif selection == "Exact Solutions":
            change_to = "EXACT"

        elif selection == "Standard Parameters":
            change_to = "PARAMSSTANDARD"

        else:
            change_to = "MAIN"

        self.parentApp.change_form(change_to)

class StandardParameters(npyscreen.ActionForm):

    def create(self):

        for run in loewner_runs:

            self.add(npyscreen.TitleText, name="Start time:")
            self.add(npyscreen.TitleText, name="Final time:")
            self.add(npyscreen.TitleText, name="Resolution:")


    def on_ok(self):
        pass

    def on_cancel(self):
        pass

class NumberSqrtRuns(npyscreen.ActionForm):

    def create(self):

        if sqrt_bool[0]:
            self.kappa = self.add(npyscreen.TitleText, name="Enter the number of desired kappa runs:")

        if sqrt_bool[1]:
            self.c_alpha = self.add(npyscreen.TitleText, name="Enter the number of desired c_alpha runs:", value=1)

    def on_ok(self):

        change_screen = True

        if sqrt_bool[0]:

            kappa_num = self.kappa.value

            try:

                kappa_num = int(kappa_num)

                if kappa_num < 1:

                    npyscreen.notify_confirm("The number of kappa runs should be greater than or equal to one.","Bad Input")
                    change_screen = False

            except ValueError:

                npyscreen.notify_confirm("The number of kappa runs could not be converted to an integer.","Bad Input")
                change_screen = False

        if sqrt_bool[1]:

            c_alpha_num = self.c_alpha.value

            try:

                c_alpha_num = int(c_alpha_num)

                if c_alpha_num < 1:

                    npyscreen.notify_confirm("The number of c-alpha runs should be greater than or equal to one.","Bad Input")
                    change_screen = False

            except ValueError:

                npyscreen.notify_confirm("The number of c-alpha runs could not be converted to an integer.","Bad Input")
                change_screen = False

        if change_screen:
            self.parentApp.addForm("PARAMSSTANDARD", StandardParameters, name="Loewner's Equation")
            self.parentApp.switchForm("PARAMSSTANDARD")

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

class DrivingOptions(npyscreen.ActionForm):

    def create(self):

        self.option = self.add(npyscreen.TitleMultiSelect, max_height=Constants.TOTAL_DRIVING_FUNCTIONS + 2, value = [0,], name="Use space to select/deselect the driving function(s):",
                values = Constants.DRIVING_INFO, scroll_exit=True)

    def on_ok(self):

        selections = self.option.get_selected_objects()

        if selections is not None:

            selection_contains_squareroot(selections)
            create_loewner_runs(selections)

            if any(sqrt_bool):
                self.parentApp.addForm("SQRTRUNS", NumberSqrtRuns, name="Loewner's Equation")
                self.parentApp.switchForm("SQRTRUNS")

            else:
                self.parentApp.addForm("PARAMSSTANDARD", StandardParameters, name="Loewner's Equation")
                self.parentApp.change_form("PARAMSSTANDARD")

        else:
            npyscreen.notify_confirm("Please select at least one driving function","Bad Input")

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

if __name__ == "__main__":
    App = RunLoewner()
    App.run()
