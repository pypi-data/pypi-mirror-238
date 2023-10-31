import re

from kivy.properties import NumericProperty
from kivymd.uix.textfield import MDTextField


class ValidateMDTextField(MDTextField):
    min_text_length = NumericProperty(0)

    def __init__(self, **kwargs):
        self.register_event_type("on_dirty")
        super().__init__(**kwargs)

    def insert_text(self, substring, from_undo=False):
        s = self.apply_constraints(substring)
        if s != "":
            self.dispatch("on_dirty")
        return super().insert_text(s, from_undo=from_undo)

    def apply_constraints(self, text):
        pat = self.pat
        s = re.sub(pat, "", text)
        return s

    def on_text_validate(self):
        self.text = self.apply_constraints(self.text)
        checks = [0 < len(self.text)]
        if self.max_text_length is not None:
            checks.append(len(self.text) <= self.max_text_length)
        if self.min_text_length > 0:
            checks.append(self.min_text_length <= len(self.text))
        if all(checks):
            self.error = False
        else:
            self.error = True

    def on_focus(self, instance, value):
        if not value:
            self.dispatch("on_text_validate")
        super().on_focus(instance, value)

    def on_text(self, instance, value):
        self.dispatch("on_text_validate")

    def on_dirty(self):
        pass


class LetterMDTextField(ValidateMDTextField):
    pat = re.compile("[^a-zA-Z.äöüßÄÖÜ\s]")


class NumberMDTextField(ValidateMDTextField):
    pat = re.compile("[^0-9]")
