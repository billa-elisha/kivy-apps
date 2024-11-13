from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from administration_window.admin import AdministrationPage
from login.login import LogInWindow
from operator_window.operation_window import OperationWindow


class MainWindow(BoxLayout):
    operator_widget = OperationWindow()
    admin_widget = AdministrationPage()
    signin_widget = LogInWindow()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.scrn_si.add_widget(self.signin_widget)
        self.ids.scrn_admin.add_widget(self.admin_widget)
        self.ids.scrn_op.add_widget(self.operator_widget)
    

class MainApp(App):
    def build(self):
        return MainWindow()
    pass

if __name__ =='__main__':
    MainApp().run()
