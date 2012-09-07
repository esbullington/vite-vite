from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics.texture import Texture


class MyWidget(Widget):
    def __init__(self, **args):
        super(MyWidget, self).__init__(**args)

        self.texture = Texture.create(size=(64, 64))

        # create 64x64 rgb tab, and fill with value from 0 to 255
        # we'll have a gradient from black to white
        size = 64 * 64 * 3
        buf = [int(x * 145 / size) for x in reversed(xrange(size))]

        # then, convert the array to a ubyte string
        buf = ''.join(map(chr, buf))

        self.texture.blit_buffer(buf, colorfmt='rgb', bufferfmt='ubyte')

        with self.canvas:
            Rectangle(pos=self.pos, size=self.size, texture=self.texture)


class TestApp(App):
    def build(self):
        return MyWidget(size=(200, 200))


if __name__ == '__main__':
    TestApp().run()
