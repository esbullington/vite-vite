import kivy
kivy.require('1.0.8')

from kivy.core.window import Window
from kivy.uix.widget import Widget

class MyKeyboardListener(Widget):

    def __init__(self, **kwargs):
        super(MyKeyboardListener, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(
            self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)


    def _on_these_settings(self, window, *largs):
        key = largs[0]
        setting_key = 282  # F1

        if platform() == 'android':
            import android
            import pygame

            android.map_key(android.KEYCODE_MENU, 1000)
            android.map_key(android.KEYCODE_BACK, 1001)
            android.map_key(android.KEYCODE_HOME, 1002)
            android.map_key(android.KEYCODE_SEARCH, 1003)

        # android hack, if settings key is pygame K_MENU
        if platform == 'android':
            import pygame
            setting_key = pygame.K_MENU

        if key == setting_key:
            # toggle settings panel
            Logger.info("This is the F1 key")
            self.open_settings = None
            if not self._menu_down:
                self._app_menu.open()
                self._menu_down = True
                Logger.info("State is true")
            else:
                self._app_menu.dismiss()
                self._menu_down = False
                Logger.info("State is false")
            return True
            if key == 27:
                return self.close_menu()


    def _keyboard_closed(self):
        print 'My keyboard have been closed!'
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print 'The key', keycode, 'have been pressed'
        print ' - text is %r' % text
        print ' - modifiers are %r' % modifiers

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        if keycode[1] == 'escape':
            keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True

if __name__ == '__main__':
    from kivy.base import runTouchApp
    runTouchApp(MyKeyboardListener())
