from kivy.clock import Clock

#------------------------------------------------------------------------------

from lib import api_client

from components import screen
from components import buttons

#------------------------------------------------------------------------------

_Debug = True

#------------------------------------------------------------------------------

class WelcomeScreen(screen.AppScreen):

    verify_network_connected_task = None

    def get_title(self):
        return 'BitDust'

    def populate_buttons(self, show_button):
        if _Debug:
            print('WelcomeScreen.populate_buttons show_button=%r' % show_button)
        if show_button:
            exists = False
            for w in self.ids.central_widget.children:
                if isinstance(w, buttons.FillRoundFlatButton):
                    exists = True
                    break
            if not exists:
                btn = buttons.FillRoundFlatButton(
                    text='create new identity',
                    pos_hint={'center_x': .5},
                    md_bg_color=self.app().color_success_green,
                    text_color=self.app().color_white99,
                    on_release=self.on_create_identity_button_clicked,
                )
                self.ids.central_widget.add_widget(btn)
        else:
            for w in self.ids.central_widget.children:
                if isinstance(w, buttons.FillRoundFlatButton):
                    self.ids.central_widget.remove_widget(w)
                    break

    def on_enter(self, *args):
        # self.ids.action_button.close_stack()
        self.ids.state_panel.attach(automat_id='initializer')
        if not self.verify_network_connected_task:
            self.verify_network_connected_task = Clock.schedule_interval(self.control().verify_network_connected, 10)
        api_client.identity_get(cb=self.on_identity_get_result)

    def on_leave(self, *args):
        # self.ids.action_button.close_stack()
        self.ids.state_panel.release()
        if self.verify_network_connected_task:
            Clock.unschedule(self.verify_network_connected_task)
            self.verify_network_connected_task = None

#     def on_action_button_clicked(self, btn):
#         if _Debug:
#             print('WelcomeScreen.on_action_button_clicked', btn.icon)
#         self.ids.action_button.close_stack()
#         if btn.icon == 'chat-plus-outline':
#             self.main_win().select_screen('create_group_screen')
#         elif btn.icon == 'account-key-outline':
#             self.main_win().select_screen('friends_screen')

    def on_nav_button_clicked(self):
        pass
        # self.ids.action_button.close_stack()

    def on_create_identity_button_clicked(self, *args):
        self.main_win().select_screen('new_identity_screen')

    def on_identity_get_result(self, resp):
        if _Debug:
            print('WelcomeScreen.on_identity_get_result', self.main_win().state_process_health, self.main_win().state_identity_get, resp)
        if self.main_win().state_process_health == 1 and self.main_win().state_identity_get != 1 and not api_client.is_ok(resp):
            self.populate_buttons(True)
        else:
            self.populate_buttons(False)
