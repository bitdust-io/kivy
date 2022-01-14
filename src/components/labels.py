from kivy.properties import StringProperty, NumericProperty  # @UnresolvedImport
from kivy.uix.label import Label

from kivymd.uix.label import MDLabel
from kivymd.theming import ThemableBehavior

#------------------------------------------------------------------------------

from lib import api_client

#------------------------------------------------------------------------------

_Debug = False

#------------------------------------------------------------------------------

class CustomIcon(MDLabel):

    icon = StringProperty("ab-testing")
    icon_pack = StringProperty("IconMD")
    icon_width = NumericProperty("32dp")
    icon_height = NumericProperty("32dp")


class BaseLabel(MDLabel):
    pass


class MarkupLabel(BaseLabel):
    pass


class NormalLabel(MarkupLabel):
    pass


class SingleLineLabel(NormalLabel):
    pass


class HFlexMarkupLabel(ThemableBehavior, Label):
    label_height = NumericProperty('32dp')


class VFlexMarkupLabel(ThemableBehavior, Label):
    label_width = NumericProperty('100dp')


class ChatMessageLabel(NormalLabel):
    pass


class StatusLabel(NormalLabel):

    def from_api_response(self, response):
        if api_client.is_ok(response):
            self.text = ''
            return
        errors = api_client.response_errors(response)
        if not isinstance(errors, list):
            errors = [errors, ]
        txt = ', '.join(errors)
        self.text = '[color=#f00]%s[/color]' % txt
