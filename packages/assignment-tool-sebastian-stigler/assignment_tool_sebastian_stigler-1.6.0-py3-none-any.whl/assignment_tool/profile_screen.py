import os
from typing import Dict

from kivy.core.window import Window
from kivy.properties import BooleanProperty
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.screen import MDScreen

from assignment_tool.manager import Manager


class ProfileScreen(MDScreen):
    first_login = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyboard = Window.request_keyboard(None, self)
        self.keyboard.bind(on_key_down=self.keyboad_on_key_down)

    def keyboad_on_key_down(self, window, keycode, text, modifier):
        if not self.ids.saveprofile.focus or self.ids.saveprofile.disabled:
            return
        if keycode[1] in ("enter", "numpadenter"):
            self.ids.saveprofile.dispatch("on_release")


class ProfileManager(Manager):
    screen_name = "profile"

    def __init__(self, app):
        super().__init__(app)
        self.profile_keys = self.config.get("student", "profile_keys").split(" ")

    def validate(self):
        for key in self.profile_keys:
            self.instance.ids[key].dispatch("on_text_validate")

    def check(self):
        result = not any(self.instance.ids[key].error for key in self.profile_keys)
        return result

    def load(self):
        dumpfile = os.path.expanduser(self.config.get("student", "profile"))
        store = JsonStore(dumpfile)
        if store.count() > 0:
            for key in self.profile_keys:
                if store.exists(key):
                    self.instance.ids[key].text = store.get(key)["text"]
        self.validate()

    def get_student(self) -> Dict[str, str]:
        dumpfile = os.path.expanduser(self.config.get("student", "profile"))
        store = JsonStore(dumpfile)
        result = {"name": "X", "firstname": "X", "id": "00000"}
        if store.count() > 0:
            for key in self.profile_keys:
                if store.exists(key):
                    result[key.replace("student", "")] = store.get(key)["text"]
        return result

    def save(self):
        self.validate()
        if self.check():
            dumpfile = os.path.expanduser(self.config.get("student", "profile"))
            store = JsonStore(dumpfile)
            for key in self.profile_keys:
                store.put(key, text=self.instance.ids[key].text.strip())
