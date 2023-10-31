"""
The Assignment Tool

This application helps to coordinate the assignments for "Programmieren 1" lecture at Aalen University.
"""
import os
import os.path
from configparser import ConfigParser

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, FadeTransition, SlideTransition
from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.floatlayout import MDFloatLayout

from assignment_tool.splash_screen import SplashManager
from assignment_tool.profile_screen import ProfileManager
from assignment_tool.assignment_screen import AssignmentManager
from assignment_tool.details_screen import DetailsManager
from assignment_tool.result_screen import ResultManager

from assignment_tool import Info

Window.fullscreen = False
Window.size = (800, 600)
Window.minimum_width, Window.minimum_height = Window.size


class About(MDFloatLayout):
    """
    The about page
    """


class AssignmentToolApp(MDApp):
    """
    The main application
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.previous_screen = "assignment"
        self.splash = None
        self.profile = None
        self.assignment = None
        self.details = None
        self.result = None
        self.sm = ScreenManager()
        self.info = Info()
        self.about = None

    def build_config(self, config):
        """
        Set default values for the configuration object/file
        :param config: The config object
        :return:
        """

        config.setdefaults(
            "student",
            {
                "profile": os.path.join(self.user_data_dir, "student_profile.json"),
                "profile_keys": " ".join(
                    ["studentname", "studentfirstname", "studentid"]
                ),
            },
        )
        config.setdefaults(
            "courses",
            {
                "url": "https://image.informatik.htw-aalen.de/~stigler/download/assignment_tool/courses.json",
                "path": os.path.join(self.user_data_dir, "courses.json"),
            },
        )
        config.setdefaults(
            "user-dirs",
            {
                "file": os.path.join(
                    os.path.dirname(self.user_data_dir), "user-dirs.dirs"
                ),
                "key": "xdg_documents_dir",
            },
        )
        config.setdefaults(
            "filemanager",
            {
                "programs": "nautilus caja",
                "path_nautilus": "/usr/bin/nautilus",
                "path_caja": "/usr/bin/caja",
            },
        )
        config.setdefaults(
            "workspace.settings",
            {"files.exclude": " ".join(["**/.assignment_tool", "**/.vscode"])},
        )
        config.setdefaults("vscode", {"path": "/snap/bin/code"})

    def get_application_config(self, defaultpath="%(appdir)s/%(appname)s.ini"):
        """
        Set the path and filename for the config file
        :param defaultpath:
        :return:
        """
        path = os.path.join(self.user_data_dir, "%(appname)s.ini")
        return super().get_application_config(path)

    def build(self):
        """
        Build the application
        :return: The screenmanager object
        """
        self.title = "Assignment Tool"
        self.icon = os.path.join(self.directory, "assets/logo255.png")
        self.theme_cls.primary_palette = "Green"

        # update new config defaults (won't update value changes!)
        self.config.write()

        self.splash = SplashManager(self)
        self.profile = ProfileManager(self)
        self.assignment = AssignmentManager(self)
        self.details = DetailsManager(self)
        self.result = ResultManager(self)
        self.sm.add_widget(
            Builder.load_file(os.path.join(self.directory, "splash_screen.kv"))
        )
        self.sm.add_widget(
            Builder.load_file(os.path.join(self.directory, "assignment_screen.kv"))
        )
        self.sm.add_widget(
            Builder.load_file(os.path.join(self.directory, "profile_screen.kv"))
        )
        self.sm.add_widget(
            Builder.load_file(os.path.join(self.directory, "details_screen.kv"))
        )
        self.sm.add_widget(
            Builder.load_file(os.path.join(self.directory, "result_screen.kv"))
        )
        return self.sm

    def get_base_directory(self):
        """
        Get the name of the documents' directory according to the currently set language
        :return: The absolute path of the documents directory
        """
        user_dirs_file = self.config.get("user-dirs", "file")
        user_dirs_key = self.config.get("user-dirs", "key")
        with open(user_dirs_file) as fd:
            config_content = "[DEFAULT]\n" + fd.read()
        cfg = ConfigParser()
        cfg.read_string(config_content)
        base_directory = os.path.expandvars(
            cfg.get("DEFAULT", user_dirs_key).replace('"', "")
        )
        return base_directory

    def populate_assignment_screen(self):
        """
        Populate the assignment screen with data, collected by the splash screen
        :return:
        """
        courses = self.sm.get_screen("splash").courses
        filemanager = self.sm.get_screen("splash").filemanager

        self.assignment.populate(courses, 0, self.get_base_directory(), filemanager)

    def leave_splash_screen(self):
        """
        Leave the splash screen and transition to the assignment screen
        or the profile screen if the profile is not registered yet.
        :return:
        """
        self.profile.load()
        self.root.transition = FadeTransition()
        self.root.transition.duration = 1
        if not self.profile.check():
            self.root.current = "profile"
            self.profile.instance.first_login = True
        else:
            self.root.current = "assignment"
        self.root.transition = SlideTransition()

    def back(self, condition=True):
        """
        Navigate back to the previous screen
        :param condition: Execute the transition only if the condition is true
        :return:
        """
        self.navigate(self.previous_screen, "right", condition=condition)

    def navigate(self, target, direction="left", condition=True):
        """
        Navigation methode to transition to other screens
        :param target: Name of the target screen
        :param direction: The direction of the transition ["left", "right", "up", "down"]
        :param condition: Execute the transition only if the condition is true
        :return:
        """
        if condition:
            self.root.transition.direction = direction
            self.root.current = target

    def open_about(self, _):
        """
        Open the about popup
        :param _: Dummy argument
        :return:
        """
        if self.about is None:
            self.about = MDDialog(
                type="custom",
                content_cls=About(),
                buttons=[
                    MDRectangleFlatButton(
                        text="Schließen",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close_about,
                    )
                ],
            )
        self.about.open()

    def close_about(self, _):
        """
        Close the about popup
        :param _: Dummy argument
        :return:
        """
        self.about.dismiss()


def run():
    """
    Run the application
    :return:
    """
    app = AssignmentToolApp()
    app.run()


if __name__ == "__main__":
    run()
