#!/usr/bin/env python -u
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------

import os
import sys

#------------------------------------------------------------------------------

import locale
locale.setlocale(locale.LC_CTYPE, 'en_US.UTF-8')

if 'ANDROID_ARGUMENT' not in os.environ:
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

#------------------------------------------------------------------------------ 

_Debug = True

#------------------------------------------------------------------------------

if _Debug:
    print('BitDustApp __file__', os.path.dirname(os.path.abspath(__file__)))
    print('BitDustApp os.getcwd', os.path.abspath(os.getcwd()))
    print('BitDustApp sys.path', sys.path)
    print('BitDustApp os.listdir', os.listdir(os.getcwd()))

#------------------------------------------------------------------------------

# current_src_folder = os.path.abspath(os.path.join(os.getcwd(), 'src'))
# if os.path.isdir(current_src_folder):
#     if current_src_folder not in sys.path:
#         sys.path.append(current_src_folder)
#         if _Debug:
#             print('added %r to Python sys.path' % current_src_folder)

#------------------------------------------------------------------------------

from kivy.lang import Builder
from kivy.config import Config

#------------------------------------------------------------------------------

Config.set('input', 'mouse', 'mouse,multitouch_on_demand')  # disable multi-touch
Config.set('graphics', 'resizable', True)
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '740')

#------------------------------------------------------------------------------

from kivymd.app import MDApp
from kivy.core.window import Window

#------------------------------------------------------------------------------

from lib.system import is_android

from screens import controller

#------------------------------------------------------------------------------

if is_android(): 
    from jnius import autoclass  # @UnresolvedImport
    from android.permissions import request_permissions, Permission  # @UnresolvedImport
    import encodings.idna

#------------------------------------------------------------------------------

# os.environ['KIVY_METRICS_DENSITY'] = '1'
# os.environ['KIVY_METRICS_FONTSCALE'] = '1'

#------------------------------------------------------------------------------

Builder.load_string("""
#:import NoTransition kivy.uix.screenmanager.NoTransition
#:import Window kivy.core.window.Window
#:import md_icons kivymd.icon_definitions.md_icons
#:import fa_icon components.webfont.fa_icon
#:import md_icon components.webfont.md_icon
#:import icofont_icon components.webfont.icofont_icon
#:import make_icon components.webfont.make_icon
""")

#------------------------------------------------------------------------------

if is_android():
    PACKAGE_NAME = 'org.bitdust_io.bitdust1'
    SERVICE_NAME = '{packagename}.Service{servicename}'.format(
        packagename=PACKAGE_NAME,
        servicename='Bitdustnode'
    )
    APP_STARTUP_PERMISSIONS = [
        Permission.INTERNET,
        Permission.READ_EXTERNAL_STORAGE,
        Permission.WRITE_EXTERNAL_STORAGE,
        Permission.FOREGROUND_SERVICE,
    ]
    PythonActivity = autoclass('org.bitdust_io.bitdust1.BitDustActivity')

#------------------------------------------------------------------------------

orig_resolve_font_name = None

def my_resolve_font_name(cls):
    global orig_resolve_font_name
    fn = cls.options['font_name']
    ret = orig_resolve_font_name(cls)
    if _Debug:
        print('resolve_font_name', fn, cls.options['font_name_r'], len(cls.options['text']))
    return ret

#------------------------------------------------------------------------------

def request_app_permissions(list_permissions=[]):
    if not is_android():
        return None
    global APP_STARTUP_PERMISSIONS
    if _Debug:
        print('BitDustApp.request_app_permissions() : %r' % (list_permissions or APP_STARTUP_PERMISSIONS))
    ret = request_permissions(list_permissions or APP_STARTUP_PERMISSIONS)
    if _Debug:
        print('BitDustApp.request_app_permissions() result : %r' % ret)
    return ret

#------------------------------------------------------------------------------

class BitDustApp(MDApp):

    control = None
    main_window = None

    def build(self):
        global orig_resolve_font_name
        if _Debug:
            print('BitDustApp.build()')

        self.theme_cls.theme_style = 'Light'
        self.theme_cls.primary_palette = 'Indigo'
        self.theme_cls.accent_palette = 'Green'

        from components import styles
        from components import layouts
        from components import labels
        from components import buttons
        from components import text_input
        from components import list_view
        from components import navigation
        from components import main_window
        styles.init(self)

        self.control = controller.Controller(self)
        self.main_window = main_window.MainWindow()

        Window.bind(on_keyboard=self.on_key_input)

        return self.main_window

    def start_android_service(self, finishing=False):
        if not is_android():
            return None
        if _Debug:
            print('BitDustApp.start_android_service() finishing=%r' % finishing)
        service = autoclass(SERVICE_NAME)
        mActivity = PythonActivity.mActivity
        argument = ''
        if finishing:
            argument = '{"stop_service": 1}'
        service.start(mActivity, argument)
        if finishing:
            self.service = None
            if _Debug:
                print('BitDustApp.start_android_service() service expect to be STOPPED now')
        else:
            self.service = service
            if _Debug:
                print('BitDustApp.start_android_service() service STARTED : %r' % self.service)
        return self.service

    def stop_android_service(self):
        if not is_android():
            return None
        if _Debug:
            print('BitDustApp.stop_service() %r' % self.service)
        service = autoclass(SERVICE_NAME)
        service.stop(PythonActivity.mActivity)
        self.start_android_service(finishing=True)
        if _Debug:
            print('BitDustApp.stop_service() STOPPED')
        return self.service

    def check_restart_bitdust_engine(self):
        if is_android():
            return None
        # TODO: to be implemented ...

    def on_start(self):
        if _Debug:
            print('BitDustApp.on_start()')
        self.main_window.register_screens(controller.all_screens())
        self.main_window.register_controller(self.control)
        self.main_window.select_screen('process_dead_screen')
        self.control.start()
        if is_android():
            self.start_android_service()
        else:
            self.check_restart_bitdust_engine()

    def on_stop(self):
        if _Debug:
            print('BitDustApp.on_stop()')
        self.control.stop()
        self.main_window.unregister_controller()
        self.main_window.unregister_screens()
        # TODO: check if we need to stop BitDust engine after App closes

    def on_pause(self):
        if _Debug:
            print('BitDustApp.on_pause()')
        return True

    def on_resume(self):
        if _Debug:
            print('BitDustApp.on_resume()')

    def on_key_input(self, window_obj, key_code, scancode, codepoint, modifier):
        if _Debug:
            print('BitDustApp.on_key_input', key_code, scancode, modifier)
        if is_android():
            if key_code == 27:
                return True
            else:
                return False
        return False

#------------------------------------------------------------------------------

def main():
    if _Debug:
        print('BitDustApp.main() process is starting')
    request_app_permissions()
    BitDustApp().run()
    if _Debug:
        print('BitDustApp.main() process is finishing')

#------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
