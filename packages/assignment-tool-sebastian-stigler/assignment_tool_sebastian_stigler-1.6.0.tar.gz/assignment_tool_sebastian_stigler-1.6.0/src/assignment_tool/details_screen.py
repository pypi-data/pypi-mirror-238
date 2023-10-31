import os
import re
import subprocess
import webbrowser
from threading import Thread
from typing import List, Dict

from kivy.logger import Logger
from kivy.network.urlrequest import UrlRequest
from kivy.properties import StringProperty, ObjectProperty
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.screen import MDScreen

from requests_toolbelt import MultipartEncoder

from assignment_tool import Info
from assignment_tool.manager import Manager
from assignment_tool.utils import Assignment, Url, CheckResult


class CheckContent(MDBoxLayout):
    """
    Check content popup
    """


class DetailIconListItem(OneLineAvatarIconListItem):
    """
    Customized OneLineIconListItem with none clickable icon
    """

    icon_left = StringProperty()
    icon_left_color = ObjectProperty([1, 0, 0, 1])
    icon_right = StringProperty()
    my_callback = ObjectProperty()


class DetailsScreen(MDScreen):
    """
    The details screen
    """

    heading = StringProperty()
    assignment = ObjectProperty()
    urls = ObjectProperty()
    filemanager = StringProperty()
    workspace_filename = StringProperty()


class DownloadAssignment:
    """
    Organize the actions of the download assignment item
    """

    def __init__(self, instance, config):
        self.instance = instance
        self.config = config

    def open_browser(self):
        """
        Open Canvas course in a browser
        :return:
        """
        webbrowser.open(self.instance.urls.lms)

    def open_filemanager(self):
        """
        Open os filemanager on the assignment path
        :return:
        """
        path_filemanager = self.config.get(
            "filemanager", "path_" + self.instance.filemanager
        )

        cmd = [path_filemanager, self.instance.assignment.assignment_path]
        Logger.info("Open browser: %r" % cmd)
        thread = Thread(target=lambda: subprocess.Popen(cmd))
        thread.daemon = True
        thread.start()

    def download_action(self):
        """
        Callback for download assignment item

        Open Canvas course and, depending on the assignment, also a filemanager if it is necessary for this assignment.
        :return:
        """
        ids_download = self.instance.ids.download
        if self.instance.assignment.download_source:
            ids_download.text = "Aufgabenstellung und vorgegebenen Code herunterladen"
            ids_download.my_callback = lambda: (
                self.open_browser(),
                self.open_filemanager(),
            )
        else:
            ids_download.text = "Aufgabenstellung herunterladen"
            ids_download.my_callback = lambda: self.open_browser()


class GenerateMixin:
    """
    Mixin to create / rename the assignment file if necessary.
    """

    def __init__(self, app, instance, config):
        self.app = app
        self.instance = instance
        self.config = config

    def generate_assignment_file(self, create_empty_file: bool = True):
        """
        Generate the assignment file (if requested) and renamed with the given student id. Furthermore, add an author
        and help line in the assignment file.
        :param create_empty_file: Should an empty assignment file be created if it is missing.
        :return:
        """
        student_profile = self.app.profile.get_student()
        assignment_filename = os.path.join(
            self.instance.assignment.assignment_path,
            f"{student_profile['id']}-{self.instance.assignment.base_filename}",
        )
        self._unique_assignment_file(assignment_filename, create_empty_file)
        self._update_author(assignment_filename, student_profile)

    def _get_testat_candidates(self) -> List[str]:
        """
        Get a list of all files which look like a candidate for an assignment file (filename with or without student id
        or wrong student id)
        :return: List of assignment file candidates
        """
        pattern = r"^(\d{5,7}-)?" + self.instance.assignment.base_filename + "$"
        files = [
            entry.path
            for entry in os.scandir(self.instance.assignment.assignment_path)
            if entry.is_file() and re.fullmatch(pattern, entry.name)
        ]
        return files

    def _unique_assignment_file(
        self, assignment_filename: str, create_empty_file: bool
    ):
        """
        1. Finds candidates for the assignment file (correct name, wrong student id, just base name).
        2. If the assignment file already exists, keep it and rename all other files with the .bak extension.
        3. If there is only on file in the candidates list, this file will be renamed to the assignment file.
        4. If there are two files (that are not the assignment file), check if one has the base name.
           Then the other file must be an assignment file with a wrong studentid.
           Correct the studentid and rename the other file to a bak file.
        5. In all other cases rename all files to bak files
        6. Create an empty assignment file if it not already exists.

        :param assignment_filename: full name of the assignment with correct student id like "<id>-testat-<nr>.c"
        :param create_empty_file: if true and no file exists, the file will be created
        :return:
        """
        assignment_path = self.instance.assignment.assignment_path
        base_filename = self.instance.assignment.base_filename
        full_base_filename = os.path.join(assignment_path, base_filename)

        files = self._get_testat_candidates()

        if assignment_filename in files:
            files.remove(assignment_filename)
            self._rename_additional_files(files)
            return

        if len(files) == 1:
            src_file = files.pop()
            os.rename(src_file, assignment_filename)
        if len(files) == 2:
            if full_base_filename in files:
                files.remove(full_base_filename)
                os.rename(files[0], assignment_filename)
                files = [full_base_filename]
        self._rename_additional_files(files)
        if not os.path.isfile(assignment_filename) and create_empty_file:
            with open(assignment_filename, "w") as fp:
                fp.write("")

    @staticmethod
    def _rename_additional_files(files: List[str]):
        cnt = 0
        while len(files) > 0:
            filename = files[0]
            ext = ".bak" if cnt == 0 else ".bak%d" % cnt
            dst_filename = filename + ext
            if os.path.isfile(dst_filename) and cnt < 10:
                cnt += 1
                continue
            os.rename(filename, dst_filename)
            cnt = 0
            files.pop(0)

    @staticmethod
    def _update_author(filename: str, student_profile: Dict[str, str]):
        """
        Add author and help line in the assignment file
        :param filename: Name of the assignment file
        :param student_profile: A dictionary with firstname, name and student id
        :return:
        """
        first_line = "// Autor: {firstname} {name} ({id})\n".format(**student_profile)
        second_line = "// Tastenkombination zum Übersetzen: <Strg>+<Shift>+<b>\n"
        content = ""
        if not os.path.isfile(filename):
            return
        with open(filename) as fp:
            for line in fp:
                sline = line.strip()
                if sline.startswith(first_line.split(":")[0]) or sline.startswith(
                    second_line.strip(":")[0]
                ):
                    continue
                content += line
        content = first_line + second_line + content
        with open(filename, "w") as fp:
            fp.write(content)


class VSCodeAssignment(GenerateMixin):
    def __init__(self, app, instance, config):
        super().__init__(app, instance, config)
        self.app = app
        self.instance = instance
        self.config = config
        self.vscode_dialog = None

    def open_vscode_dialog(self):
        assignment_path = self.instance.assignment.assignment_path
        base_filename = self.instance.assignment.base_filename
        title = f"[color=#ff1a0e]Keine Datei der Form [b][i]*{base_filename}[/i][/b] gefunden![/color]"
        text = (
            f"\n[color=#202020][b]Führen Sie zunächst Schritt 1 aus:[/b]\n\n"
            f"Laden Sie hierfür die Datei\n\n"
            f"[color=#0000ff][i]{base_filename}[/i][/color]\n\n"
            f"herunter und speichern Sie sie im Verzeichnis\n\n"
            f"[color=#0000ff][i]{assignment_path}[/i][/color][/color]"
        )
        if not self.vscode_dialog:
            self.vscode_dialog = MDDialog(
                auto_dismiss=False,
                buttons=[
                    MDFlatButton(
                        text="Schließen",
                        on_release=self.close_vscode_dialog,
                    )
                ],
            )
        self.vscode_dialog.text = text
        self.vscode_dialog.ids.text.halign = "center"
        self.vscode_dialog.title = title
        self.vscode_dialog.open()

    def vscode_callback(self):
        if len(self._get_testat_candidates()) > 0:
            self.generate_assignment_file()
            self.open_vscode()
        else:
            self.open_vscode_dialog()

    def close_vscode_dialog(self, *args):
        self.vscode_dialog.dismiss()

    def open_vscode(self):
        student_profile = self.app.profile.get_student()
        assignment_filename = os.path.join(
            self.instance.assignment.assignment_path,
            f"{student_profile['id']}-{self.instance.assignment.base_filename}",
        )
        path_code = self.config.get("vscode", "path")

        cmd = [
            path_code,
            self.instance.workspace_filename,
            "-g",
            assignment_filename + ":3",
        ]
        Logger.info("Open vscode: %r" % cmd)
        thread = Thread(target=lambda: subprocess.Popen(cmd))
        thread.daemon = True
        thread.start()

    def vscode_action(self):
        ids_vscode = self.instance.ids.vscode
        ids_vscode.text = "Editor starten"
        ids_vscode.my_callback = lambda: self.vscode_callback()


class CheckCodeAssignment(GenerateMixin):
    def __init__(self, app, instance, config):
        super().__init__(app, instance, config)
        self.app = app
        self.instance = instance
        self.config = config
        self.check_dialog = None
        self.error_dialog = None

    def open_error_dialog(self):
        student_profile = self.app.profile.get_student()
        testat_filename = (
            f"{student_profile['id']}-{self.instance.assignment.base_filename}"
        )

        title = f"[color=#ff1a0e]Keine Datei mit dem Namen [b][i]{testat_filename}[/i][/b] gefunden![/color]"
        text = f"\n[color=#202020][b]Führen Sie zunächst Schritt 1 und 2 aus.[/b]"
        if not self.error_dialog:
            self.error_dialog = MDDialog(
                auto_dismiss=False,
                buttons=[
                    MDFlatButton(
                        text="Schließen",
                        on_release=self.close_error_dialog,
                    )
                ],
            )
        self.error_dialog.text = text
        self.error_dialog.ids.text.halign = "center"
        self.error_dialog.title = title
        self.error_dialog.open()

    def check_code_callback(self):
        self.generate_assignment_file(False)
        if len(self._get_testat_candidates()) > 0:
            self.open_check_code()
        else:
            self.open_error_dialog()

    def close_error_dialog(self, *args):
        self.error_dialog.dismiss()

    def open_check_code(self):
        self.open_check_dialog()
        student_profile = self.app.profile.get_student()
        assignment_filename = os.path.join(
            self.instance.assignment.assignment_path,
            f"{student_profile['id']}-{self.instance.assignment.base_filename}",
        )

        with open(assignment_filename) as fp:
            file_content = fp.read()

        payload = MultipartEncoder(
            fields={
                "filename": (
                    os.path.basename(assignment_filename),
                    file_content,
                    "text/x-csrc",
                )
            }
        )
        header = {"Content-Type": payload.content_type,
                  "User-Agent": Info().user_agent}

        UrlRequest(
            self.instance.urls.compiler,
            on_success=self.check_on_success,
            on_redirect=self.check_on_redirect,
            on_failure=self.check_on_failure,
            on_error=self.check_on_error,
            req_headers=header,
            req_body=payload,
            verify=True,
        )

    def open_check_dialog(self):
        if not self.check_dialog:
            self.check_dialog = MDDialog(
                auto_dismiss=False,
                title="Überprüfen des Codes",
                type="custom",
                content_cls=CheckContent(),
            )
        self.check_dialog.open()

    def check_on_success(self, req, result):
        self.check_dialog.dismiss()
        check_result = CheckResult.from_dict(result)
        self.app.result.populate(check_result)
        self.app.navigate("result")

    def check_on_redirect(self, req, result):
        self.check_dialog.dismiss()
        toast("Es ist ein Problem mit dem Server aufgetreten.", duration=5)

    def check_on_failure(self, req, result):
        self.check_dialog.dismiss()
        toast("Es ist ein Problem mit dem Server aufgetreten.", duration=5)

    def check_on_error(self, req, result):
        self.check_dialog.dismiss()
        toast(
            "Der Server kann nicht erreicht werden.\nPrüfen Sie ihre Netzwerkverbindung!",
            duration=5,
        )

    def check_code_action(self):
        self.instance.ids.check_code.text = "Code vor der Abgabe überprüfen"
        self.instance.ids.check_code.my_callback = lambda: self.check_code_callback()


class DetailsManager(Manager):
    screen_name = "details"

    def __init__(self, app):
        super().__init__(app)
        self.download_assignment = None

    def populate(
        self,
        text: str,
        assignment: Assignment,
        urls: Url,
        filemanager: str,
        workspace_filename: str,
    ):
        self.instance.assignment = assignment
        self.instance.urls = urls
        self.instance.filemanager = filemanager
        self.instance.workspace_filename = workspace_filename
        if not assignment.download_source:
            gm = GenerateMixin(self.app, self.instance, self.config)
            gm.generate_assignment_file()

        self.instance.heading = text

        # download
        self.download_assignment = DownloadAssignment(self.instance, self.config)
        self.download_assignment.download_action()

        # vscode
        vscode_assignment = VSCodeAssignment(self.app, self.instance, self.config)
        vscode_assignment.vscode_action()

        check_code_assignment = CheckCodeAssignment(
            self.app, self.instance, self.config
        )
        check_code_assignment.check_code_action()
