import kivy
kivy.require('1.4.0-dev')
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, \
ListProperty, OptionProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.factory import Factory
from kivy.logger import Logger
from kivy.graphics.vertex_instructions import Triangle
from kivy.uix.settings import Settings
from kivy.config import ConfigParser, Config
from kivy.utils import platform
from kivy.core.window import Window
from kivy.uix.modalview import ModalView


####################################
##
##   GLOBAL SETTINGS
##
####################################

VERSION = '0.1'
PLATFORM = platform()

##Conditional Android import

try:
    android = None
    if PLATFORM == 'android':
        import android
except ImportError:
    pass

####################################
##
##  BEHAVIORS
##
####################################

# TouchEvent class inspired by behavior code in presemt:
# https://github.com/tito/presemt

class TouchEvent(object):

    grab_status = BooleanProperty(False)

    touch_obj = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super(TouchEvent, self).__init__(**kwargs)
        self.register_event_type('on_press')
        self.register_event_type('on_release')
        self.bind(
            on_touch_down=self._touch_down,
            on_touch_up=self._touch_up)

    def on_press(self, touch):
        pass

    def on_release(self, touch):
        pass

    def _touch_down(self, instance, touch):
        if not self.collide_point(*touch.pos):
            return
        touch.ungrab(self)
        touch.grab(self)
        self.touch_obj = touch
        self.dispatch('on_press', touch)
        return self.grab_status

    def _touch_up(self, instance, touch):
        if touch.grab_current is not self:
            return
        touch.ungrab(self)
        self.dispatch('on_release', touch)
        self.touch_obj = None
        return self.grab_status

Factory.register('TouchEvent', cls=TouchEvent)

class ImageButton(Factory.TouchEvent, Factory.Image):
    pass

Factory.register('ImageButton', cls=ImageButton)

class BoxButton(Factory.TouchEvent, Factory.BoxLayout):
    pass

Factory.register('BoxButton', cls=BoxButton)

####################################
##
## Spinner
##
####################################

class AppDropDown(DropDown):
    pass


class AppSpinner(Spinner):
    dropdown_cls = ObjectProperty(AppDropDown)
    '''Class used to display the dropdown list when the Spinner is pressed.

    :data:`dropdown_cls` is a :class:`~kivy.properties.ObjectProperty`, default
    to :class:`~kivy.uix.dropdown.DropDown`.
    '''

    def __init__(self, **kwargs):
        self._dropdown = None
        super(Spinner, self).__init__(**kwargs)
        self.bind(
            on_release=self._toggle_dropdown,
            dropdown_cls=self._build_dropdown,
            option_cls=self._build_dropdown,
            values=self._update_dropdown)
        self._build_dropdown()

####################################
##
##  Android Menu
##
####################################

class AppMenu(AppSpinner):
    pass


Factory.register('AppMenu', cls=AppMenu)

####################################
##
##   Main Widget Class
##
####################################


class AppScreen(Screen):
    header = StringProperty('Default Header')
    spinnertext = StringProperty('Default Spinner Text')


class ContentScreen(AppScreen):
    
    def __init__(self,**kwargs):
        super(ContentScreen, self).__init__(**kwargs)
        Logger.info("This is the ContentScreen class")


class MainScreen(AppScreen):
    pass


class HelpScreen(AppScreen):
    specialvar = StringProperty("Hello from Help Screen")


class EditScreen(AppScreen):
    pass


class AddScreen(AppScreen):
    pass


Factory.register('AppScreen', cls=AppScreen)
Factory.register('ContentScreen',cls=ContentScreen)
Factory.register('MainScreen',cls=MainScreen)
Factory.register('HelpScreen',cls=HelpScreen)
Factory.register('EditScreen', cls=EditScreen)
Factory.register('AddScreen', cls=AddScreen)
Factory.register('AppSpinner', cls=AppSpinner)
Factory.register('AppDropDown', cls=AppDropDown)

####################################
##
##   Main Application Class
##
####################################


class ViteViteApp(App):
    title = "Vite Vite"
    version = StringProperty(VERSION)

    def build_config(self, config):
        config.setdefaults('section1', {
            'key1': 'value1',
            'key2': '42' })
        config.setdefaults('private', { 'first_startup': 'false' })
        
    def build_settings(self, settings):
        settings.add_json_panel('Test application', self.config, 'settings.json')

    def build(self):
        config = self.config
        self.root = Builder.load_file('vitevite.kv')
        return self.root

    def on_start(self):
        if PLATFORM in ('windows','linux','osx'):
            self._app_window.size = 400,600


if __name__ in ('__main__', '__android__'):
    # interactive = InteractiveLauncher(ToolKitApp())
    ViteViteApp().run()
