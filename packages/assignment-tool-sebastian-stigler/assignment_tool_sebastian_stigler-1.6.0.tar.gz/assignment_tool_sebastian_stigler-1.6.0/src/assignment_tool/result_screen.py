from kivy.properties import ObjectProperty
from kivymd.toast import toast
from kivymd.uix.button import MDRectangleFlatButton, MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen

from assignment_tool.manager import Manager
from assignment_tool.utils import CheckResult


class ResultScreen(MDScreen):
    check_result = ObjectProperty(CheckResult(), rebind=True)


class ResultManager(Manager):
    screen_name = "result"

    def __init__(self, app):
        super().__init__(app)
        self.dialog = None

    def populate(self, check_result: CheckResult):
        self.instance.check_result = check_result

    def callback(self, with_popup=True):
        if with_popup:
            self.open_dialog()
        else:
            self.open_browser_and_filemanager()
            self.app.navigate("details", "right")
            toast("Testat abgegeben.", duration=5)

    def open_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Wollen Sie das Testat wirklich abgeben?",
                auto_dismiss=False,
                buttons=[
                    MDRectangleFlatButton(
                        text="Abbrechen",
                        on_release=lambda x: (
                            self.app.navigate("details", "right"),
                            self.close_dialog(),
                        ),
                    ),
                    MDRaisedButton(
                        text="Trotzdem Abgeben",
                        on_release=lambda x: (
                            self.open_browser_and_filemanager(),
                            self.app.navigate("details", "right"),
                            self.close_dialog(),
                            toast("Testat trotz Compiler Warnungen abgegeben!", duration=5)
                        ),
                        md_bg_color=self.app.theme_cls.accent_dark,
                    ),
                ],
            )
        self.dialog.open()

    def close_dialog(self):
        self.dialog.dismiss()

    def open_browser_and_filemanager(self):
        self.app.details.download_assignment.open_browser()
        self.app.details.download_assignment.open_filemanager()
