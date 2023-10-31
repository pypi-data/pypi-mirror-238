class Manager:
    screen_name = ""

    def __init__(self, app):
        self._instance = None
        self.app = app
        self.config = self.app.config

    @property
    def instance(self):
        if self._instance is None:
            self._instance = self.app.sm.get_screen(self.screen_name)
        return self._instance
