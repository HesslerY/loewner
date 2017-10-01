import npyscreen
import curses
import Constants

class RunLoewner(npyscreen.NPSAppManaged):

    def onStart(self):

        self.addForm("MAIN", LoewnerOptions, name="Main")
        self.addForm("STANDARD", DrivingOptions, name="Select the driving function(s):")

    def change_form(self, name):

        self.switchForm(name)

class LoewnerOptions(npyscreen.ActionForm):

    def create(self):

        self.option = self.add(npyscreen.TitleSelectOne, max_height=3, value = [1,], name="Pick One",
                values = ["Standard Mode","Option2","Option3"], scroll_exit=True)

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

        self.option = self.add(npyscreen.TitleSelectOne, max_height=3, value = [1,], name="Pick One",
                values = ["a","b","c"], scroll_exit=True)

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
if __name__ == "__main__":
    App = RunLoewner()
    App.run()
