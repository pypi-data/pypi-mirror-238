import json
import os.path

from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from kivymd.toast import toast
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivy.properties import StringProperty

from assignment_tool import Info
from assignment_tool.manager import Manager

LOAD_DELAY = 0.2


class SplashScreen(MDScreen):
    loading_text = StringProperty("Initialisierung...")
    error_text = StringProperty("")

    def __init__(self, **kwargs):
        self.register_event_type("on_next_task")
        self.register_event_type("on_tasks_done")
        self.register_event_type("on_task_error")
        super().__init__(**kwargs)
        self.tasks = []
        self.task_cnt = 0
        self.courses = None
        self.next_task_delay = None
        self.filemanager = ""

    def on_next_task(self):
        self.ids.progress.value = (
            (self.task_cnt - len(self.tasks)) * 100.0 / self.task_cnt
        )
        if len(self.tasks) == 0:
            self.loading_text = "Fertig"
            self.next_task(done=True)
            return
        task = self.tasks.pop(0)
        task()

    def on_tasks_done(self):
        pass

    def on_task_error(self):
        pass

    def register_task(self, task_manager, task):
        if hasattr(task_manager, "task_" + task):
            self.tasks.append(getattr(task_manager, "task_" + task))
        else:
            raise AttributeError(f"{task_manager} has no attribute 'task_{task}'!")
        self.task_cnt = len(self.tasks)

    def next_task(self, done=False):
        event = "on_next_task" if not done else "on_tasks_done"
        if self.next_task_delay is not None:
            Clock.unschedule(self.next_task_delay)
        self.next_task_delay = Clock.schedule_once(
            lambda dt: self.dispatch(event), LOAD_DELAY
        )


class SplashManager(Manager):
    screen_name = "splash"

    def __init__(self, app):
        super().__init__(app)
        self.event = None
        self.dialog = None

    def task_load_local_course(self):
        self.instance.loading_text = "Lade lokale Kursliste..."
        local_file = self.config.get("courses", "path")
        if os.path.isfile(local_file):
            try:
                with open(local_file) as local_fd:
                    self.instance.courses = json.load(local_fd)
            except json.JSONDecodeError:
                self.instance.courses = {}
        self.instance.next_task()

    def task_check_filemanager(self):
        text = "Prüfe Dateimanager {}"
        self.instance.loading_text = text.format("...")
        filemanagers = self.config.get("filemanager", "programs").split(" ")
        available = []
        for filemanager in filemanagers:
            if os.path.isfile(self.config.get("filemanager", "path_" + filemanager)):
                available.append(filemanager)
                self.instance.loading_text = text.format(repr(available))
        if len(available) == 0:
            self.instance.error_text = "Kein Dateimanager installiert."
            self.instance.dispatch("on_task_error")
        else:
            self.instance.filemanager = available[0]
            self.instance.next_task()

    def task_check_vscode(self):
        text = "Prüfe VSCode..."
        self.instance.loading_text = text.format("...")
        vscode_path = self.config.get("vscode", "path")
        if os.path.isfile(vscode_path):
            self.instance.next_task()
        else:
            self.instance.error_text = "VSCode ist nicht installiert."
            self.instance.dispatch("on_task_error")

    def error_popup(self):
        if not self.dialog:
            self.dialog = MDDialog(
                auto_dismiss=False,
                title="[color=#ff1a0e]Beim Laden ist ein Problem aufgetreten[/color]",
                text=f"[color=#202020]{self.instance.error_text}[/color]",
                buttons=[
                    MDRectangleFlatIconButton(
                        text="BEENDEN",
                        icon="close",
                        theme_text_color="Custom",
                        icon_color=(1, 26 / 255.0, 14 / 255.0, 1),
                        text_color=(0.13, 0.13, 0.13, 1),
                        line_color=(1, 26 / 255.0, 14 / 255.0, 1),
                        on_release=self.app.stop,
                    ),
                ],
            )
        self.dialog.open()

    def task_download_course(self):
        self.instance.loading_text = "Lade Kursliste vom Server..."
        UrlRequest(
            self.config.get("courses", "url"),
            on_success=self.check_on_success,
            on_redirect=self.check_on_redirect,
            on_failure=self.check_on_failure,
            on_error=self.check_on_error,
            req_headers={"User-Agent": Info().user_agent},
            verify=True,
        )

    def check_on_success(self, req, result):
        local_file = self.config.get("courses", "path")
        with open(local_file, "w") as fd:
            json.dump(result, fd, indent=4)
        self.instance.next_task()

    def check_on_redirect(self, req, result):
        toast("Es ist ein Problem mit dem Server aufgetreten.", duration=5)

    def check_on_failure(self, req, result):
        toast("Es ist ein Problem mit dem Server aufgetreten.", duration=5)

    def check_on_error(self, req, result):
        toast(
            "Der Server kann nicht erreicht werden.\nPrüfen Sie ihre Netzwerkverbindung!",
            duration=5,
        )
