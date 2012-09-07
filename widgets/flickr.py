import urllib2,json,random

from kivy.uix.button import Button
from kivy.properties import StringProperty,ObjectProperty
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout


Builder.load_string('''
<ImageViewer>
    orientation: 'vertical'
    spacing: 20
    padding: 30
<ViewerButton>:
    size_hint: None,None
    width: 100
    height: 40
''')


class ViewerImage(AsyncImage):
    pass


class ViewerButton(Button):
    pass


class ImageViewer(BoxLayout):

    image_cls = ObjectProperty(ViewerImage)
    
    title_cls = ObjectProperty(Label)
    

    def __init__(self, **kwargs):
        super(ImageViewer, self).__init__(**kwargs)
        ## Build an initial list of photos from Flickr's public photo feed 
        data = urllib2.urlopen('http://api.flickr.com/services/feeds/photos_public.gne?format=json&nojsoncallback=1')
        ## Flickr returns invalid json, so we must fix
        json_string = data.read()
        js = json_string.replace("\\'","'")
        photo_tuples = json.loads(js)
        for k,v in photo_tuples.iteritems():
            if k == 'items':
                self.photos = v
        self._init_image()

    def _retrieve_photo(self, *largs):
        ## Select and download the image
        photos = self.photos
        photo_count = len(photos)
        photo = photos[random.randint(0,photo_count-1)]
        title = self.title_cls(text=photo[u'title'], text_size=(200,None), id='title')
        img = self.image_cls(source=photo[u'media'][u'm'], id='img')
        layout = AnchorLayout(anchor_x='center', anchor_y='center')
        btn = ViewerButton(text='Flickr!')
        btn.bind(on_press=self._select_image)
        layout.add_widget(btn)
        return (img,title,layout)

    def _init_image(self, *largs):
        photo = self._retrieve_photo()
        title = photo[0]
        img = photo[1]
        layout = photo[2]
        self.add_widget(img)
        self.add_widget(title)
        self.add_widget(layout)
        return True

    def _select_image(self, *largs):
        if self._init_image:
            self.clear_widgets()
            photo = self._retrieve_photo()
            self._build_widget(img=photo[1],title=photo[0], layout = photo[2])
            return True

    def _build_widget(self, img, title, layout, *largs):
        self.add_widget(img)
        self.add_widget(title)
        self.add_widget(layout)
        return True


if __name__ == '__main__':
    from kivy.base import runTouchApp

    imageviewer = ImageViewer()

    runTouchApp(imageviewer) 



