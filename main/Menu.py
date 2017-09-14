import Constants
import npyscreen as np

class ModeSelection(np.ActionForm):
    def create(self):
        self.mode_selection = self.add(np.TitleSelectOne, scroll_exit=True, value=[1,], name='Select a mode:', values = Constants.RUN_OPTIONS[:])

    def afterEditing(self):

        if self.mode_selection.get_selected_objects()[0] == Constants.RUN_OPTIONS[0]:
            self.parentApp.switchForm('STANDARDMODE')
        if self.mode_selection.get_selected_objects()[0] == Constants.RUN_OPTIONS[1]:
            self.parentApp.switchForm('RESMODE')
        if self.mode_selection.get_selected_objects()[0] == Constants.RUN_OPTIONS[2]:
            self.parentApp.switchForm('EXACTMODE')

class StandardMode(np.Form):
    def afterEditing(self):
        pass
    def create(self):
        self.driving_selection = self.add(np.TitleMultiSelect, scroll_exit=True, value=[1,], name='Select the driving function(s):', values = Constants.DRIVING_INFO[:])
#        self.value = None
#        self.wgName  = self.add(np.TitleFixedText, name = "Name:",)
#        self.wgDept = self.add(np.TitleText, name = "Dept:")
#        self.wgEmp      = self.add(np.TitleText, name = "Employed:")

    def on_cancel(self):
        self.parentApp.switchFormPrevious()

class myApp(np.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', ModeSelection, name='Mode Selection')
        self.addForm('STANDARDMODE', StandardMode, name='Driving Function Selection')

if __name__ == '__main__':
    TestApp = myApp().run()
