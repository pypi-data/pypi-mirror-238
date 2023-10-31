from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window

Window.size = (800, 600)
Window.minimum_width, Window.minimum_height = Window.size

KV = """
#:import KivyLexer kivy.extras.highlight.KivyLexer
#:import HotReloadViewer kivymd.utils.hot_reload_viewer.HotReloadViewer


BoxLayout:
    HotReloadViewer:
        path: app.path_to_kv_file
        errors: True
        errors_text_color: 0, 0, 0, 1
        errors_background_color: app.theme_cls.bg_dark
"""

__version__ = "0.1.0"
__author__ ="Sebastian Stigler"

class Example(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.author = __author__
        self.version = __version__
    # Kv file to hot reload
    path_to_kv_file = "result_screen.kv"
    # Build function
    def build(self):

        self.theme_cls.primary_palette = "Green"
        return Builder.load_string(KV)


if __name__ == "__main__":
    Example().run()
