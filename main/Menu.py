import npyscreen
import curses

class RunLoewner(npyscreen.NPSAppManaged):

    def onStart(self):

        self.addForm("MAIN", LoewnerOptions, name="Main")

class LoewnerOptions(npyscreen.ActionForm):

    def create(self):

        self.option = self.add(npyscreen.TitleSelectOne, max_height=4, value = [1,], name="Pick One",
                values = ["Option1","Option2","Option3"], scroll_exit=True)

    def on_ok(self):

        if str(self.option.get_selected_objects()) == "['Opt1']":
            change_forms()

    def on_cancel(self):

        self.parentApp.switchForm(None)

    def change_forms(self, *args, **keywords):

        if self.name == "Main":
            change_to = "SECOND"
        elif self.name == "Screen 2":
            change_to = "THIRD"
        else:
            change_to = "MAIN"

        # Tell the MyTestApp object to change forms.
        self.parentApp.change_form(change_to)

if __name__ == "__main__":
    App = RunLoewner()
    App.run()
