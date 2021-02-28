from kivy.metrics import dp
from kivy.core.window import Window

from kivymd.uix.snackbar import Snackbar

from components import screen

#------------------------------------------------------------------------------

def success(text, duration=5):
    sb = Snackbar(
        pos_hint={'right': 1, },
        size_hint_x=1,
        height=dp(32),
        snackbar_x=0,
        snackbar_y=Window.height - screen.toolbar().height - dp(32),
        radius=[0, 0, 0, 0, ],
        elevation=0,
        padding=dp(5),
        snackbar_animation_dir='Right',
        bg_color=screen.my_app().theme_cls.accent_color,
        duration=duration,
        text=text,
    )
    sb.ids.text_bar.halign = 'right'
    sb.open()


def error(text, duration=5):
    sb = Snackbar(
        pos_hint={'right': 1, },
        size_hint_x=1,
        height=dp(32),
        snackbar_x=0,
        snackbar_y=Window.height - screen.toolbar().height - dp(32),
        radius=[0, 0, 0, 0, ],
        elevation=0,
        padding=dp(5),
        snackbar_animation_dir='Right',
        bg_color=screen.my_app().theme_cls.error_color,
        duration=duration,
        text=text,
    )
    sb.ids.text_bar.halign = 'right'
    sb.open()
