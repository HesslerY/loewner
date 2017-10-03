import npyscreen
import curses
import Constants

class RunLoewner(npyscreen.NPSAppManaged):

    def onStart(self):

        self.addForm("MAIN", LoewnerOptions, name="Loewner's Equation")
        self.addForm("STANDARD", DrivingOptions, name="Loewner's Equation")

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
            change_to = "STANDARD"
        elif selection == "Exact Solutions":
            change_to = "EXACT"
        else:
            change_to = "MAIN"

        self.parentApp.change_form(change_to)

class DrivingOptions(npyscreen.ActionForm):

    def create(self):

        self.add(npyscreen.TitleFixedText, name = "Use space to select/deselect the driving function(s):")
        self.option = self.add(npyscreen.TitleMultiSelect, value = [0,], name=" ",
                values = Constants.DRIVING_INFO, scroll_exit=True)

    def on_ok(self):

        selection = self.option.get_selected_objects()

        if selection is not None:
            self.change_forms(selection)

        else:
            npyscreen.notify_confirm("Please select at least one driving function","Bad Input")

    def on_cancel(self):

        self.parentApp.switchForm(None)

    def change_forms(self, selection):

        if selection == "Standard Mode":
            change_to = "STANDARD"
        elif selection == "Exact Solutions":
            change_to = "EXACT"
        else:
            change_to = "MAIN"

        self.parentApp.change_form(change_to)

if __name__ == "__main__":
    App = RunLoewner()
    App.run()
