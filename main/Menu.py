import npyscreen
import curses
import Constants
from LoewnerRun import LoewnerRun
from LoewnerRun import SqrtLoewnerRun

loewner_runs = []

def create_loewner_runs(selections):

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
        self.addForm("PARAMSSTANDARD", DrivingOptions, name="Loewner's Equation")

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
        pass

    def on_ok(self):
        pass

    def on_cancel(self):
        pass

class DrivingOptions(npyscreen.ActionForm):

    def create(self):

        self.add(npyscreen.TitleFixedText, name = "Use space to select/deselect the driving function(s):")
        self.option = self.add(npyscreen.TitleMultiSelect, value = [0,], name=" ",
                values = Constants.DRIVING_INFO, scroll_exit=True)
        self.next_screen = "PARAMSSTANDARD"

    def on_ok(self):

        selections = self.option.get_selected_objects()

        if selections is not None:

            create_loewner_runs(selections)
            self.parentApp.change_form(self.next_screen)

        else:
            npyscreen.notify_confirm("Please select at least one driving function","Bad Input")

    def on_cancel(self):

        self.parentApp.switchForm(None)

if __name__ == "__main__":
    App = RunLoewner()
    App.run()
