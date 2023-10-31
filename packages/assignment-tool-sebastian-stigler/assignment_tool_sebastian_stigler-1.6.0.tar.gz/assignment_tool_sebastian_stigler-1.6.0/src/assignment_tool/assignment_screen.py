"""
The assignment screen
"""
import json
import os.path
import shutil
from typing import List, Any, Dict

from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.list import OneLineIconListItem
from kivymd.uix.screen import MDScreen

from assignment_tool.manager import Manager
from assignment_tool.utils import Assignment, Url


class CustomOneLineIconListItem(OneLineIconListItem):
    """
    Customized OneLineIconListItem with none clickable icon
    """
    icon = StringProperty()
    my_callback = ObjectProperty()


class AssignmentScreen(MDScreen):
    """
    The Assignment screen
    """
    heading = StringProperty()


class AssignmentManager(Manager):
    """
    The manager class for the assignment screen
    """
    screen_name = "assignment"

    def __init__(self, app):
        super().__init__(app)

    def populate(
        self, courses: Dict, index: int, base_directory: str, filemanager: str
    ):
        """
        Populate the Assignment screen
        :param courses: Dictionary of the course list
        :param index: The index of the course
        :param base_directory: The documents' directory in the home directory of the current user
        :param filemanager: The path to the current filemanager
        :return:
        """
        urls = Url(lms=courses["lms_url"], compiler=courses["compiler_url"])
        current_course = courses["courses"][index]
        self.instance.heading = current_course["name"]
        course_path = os.path.join(base_directory, current_course["path"])
        workspace_filename = os.path.join(
            course_path, f".{os.path.basename(course_path)}.code-workspace"
        )

        # create_course_path
        os.makedirs(course_path, mode=0o0755, exist_ok=True)

        self.instance.ids.rv.data = []
        folders = []
        for idx, entry in enumerate(current_course["assignments"]):
            entry["course_path"] = course_path
            assignment = Assignment.from_dict(entry)
            folders.append({"path": assignment.path})
            self._add_item("abacus", assignment, urls, filemanager, workspace_filename)
            self._create_assignment_path(assignment.assignment_path, idx == 0)

        self._create_workspace_file(folders, workspace_filename)

    def _create_workspace_file(
        self, folders: List[Dict[str, Any]], workspace_filename: str
    ):
        """
        Create a workspace file for vscode
        :param folders: List of the folders in the workspace (taken form the list of assignments)
        :param workspace_filename: Path to the workspace file
        :return:
        """
        workspace = {
            "folders": folders,
            "settings": {
                "[c]": {"editor.defaultFormatter": "xaver.clang-format"},
                "files.autoSave": "afterDelay",
                "files.exclude": {},
            },
        }
        for exclude in self.config.get("workspace.settings", "files.exclude").split():
            workspace["settings"]["files.exclude"][exclude] = True
        with open(workspace_filename, "w") as fd:
            json.dump(workspace, fd, indent=2)

    def _add_item(
        self,
        icon: str,
        assignment: Assignment,
        urls: Url,
        filemanager: str,
        workspace_filename: str,
    ):
        """
        Create an item for the given assignment in the view widget
        :param icon: Name of the icon
        :param assignment: The Assignment object for this assignment
        :param urls: The Url object for the url to the canvas course and the online compiler
        :param filemanager: The path to the current filemanager
        :param workspace_filename: The path to the workspace file
        :return:
        """
        text = assignment.name
        self.instance.ids.rv.data.append(
            {
                "viewclass": "CustomOneLineIconListItem",
                "icon": icon,
                "text": text,
                "my_callback": lambda app: app.details.populate(
                    f"{self.instance.heading} / {text}",
                    assignment,
                    urls,
                    filemanager,
                    workspace_filename,
                ),
            }
        )

    def _create_assignment_path(
        self, assignment_path: str, make_default_task: bool = False
    ):
        """
        Create the path for the assignment and the subdirectory .vscode with the compiler task.
        :param assignment_path:  Path for the assignment
        :param make_default_task: Should a default task of a normal task be used
        :return:
        """
        os.makedirs(assignment_path, mode=0o755, exist_ok=True)

        # populate VSCode directories
        os.makedirs(os.path.join(assignment_path, ".vscode"), mode=0o755, exist_ok=True)
        vs_task_file = os.path.join(assignment_path, ".vscode", "tasks.json")
        template_name = "tasks_default.json" if make_default_task else "tasks.json"
        shutil.copy(
            os.path.join(self.app.directory, "assets", "vscode", template_name),
            vs_task_file,
        )
