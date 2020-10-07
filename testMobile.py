from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.properties import StringProperty
from kivy.properties import ListProperty
from kivy.uix.recycleview import RecycleView

import time
# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
#:import Factory kivy.factory.Factory
<MyPopup>:#@Popup
    auto_dismiss: False
    title:'Take photo of item'
    BoxLayout:
        orientation: 'vertical'
        Camera:
            id: camera
            resolution: (640, 480)
            play: False
        ToggleButton:
            text: 'Play'
            on_press: camera.play = not camera.play
            size_hint_y: None
            height: '48dp'
        Button:
            text: 'Capture'
            size_hint_y: None
            height: '48dp'
            on_press: root.capture()
        Button:
            text: 'Close me!'
            on_release: root.dismiss()
<MainScreen>:
    id:screen0
    on_pre_enter : root.manager.store = 'other'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Store:'
        BoxLayout:
            orientation: 'horizontal'
            CheckBox:
                id : Real
                group: 'stores'
                on_press: root.manager.store = 'Real Canadian SuperStore'
            Label:
                text: 'Real Canadian SuperStore'
            #on_press: root.manager.current = 'AddRecords'
        BoxLayout:
            orientation: 'horizontal'
            CheckBox:
                group: 'stores'
                on_press: root.manager.store = 'Dollarama'
                id : Dollarama 
            Label:
                text: 'Dollarama'
        BoxLayout:
            orientation: 'horizontal'
            CheckBox:
                group: 'stores'
                on_press: root.manager.store = 'Walmart'
                id : Walmart 
            Label:
                text: 'Walmart'
        BoxLayout:
            orientation: 'horizontal'
            CheckBox:
                group: 'stores'
                on_press: root.manager.store = 'other'
                active: True
            TextInput:
                text: ''
                id : other_store_id
        Button:
            text: 'Start shopping'
            on_press: root.manager.current = 'AddRecords'
            on_press: root.check(root.manager.store, root.ids.other_store_id.text)
        Button:
            text: 'View / Edit / Update the log'
            on_press: root.manager.current = 'ViewLog'
<ViewLog>:
    on_pre_enter: root.init__records(root.ids.records)
    id:log
    BoxLayout:
        orientation:'vertical'
        BoxLayout:
            orientation: 'horizontal'
            size_hint: 1,0.15
            TextInput:
                on_text: root.search(root.ids.search_bar.text,root.ids.records)
                #pos_hint : {'top': 0.2}
                id: search_bar
            Button:
                on_press: root.search(root.ids.search_bar.text, root.ids.records)
                size_hint: 0.2, 1
                text: 'FIND'
        RecycleView:
            viewclass: 'Label'
            id:records
            RecycleBoxLayout:
                default_size: None, dp(56)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
        Button:
            text: 'Back'
            size_hint: 1,0.15
            on_press: root.manager.current = 'main'
    
<AddRecords>:
    id:screen1
    on_pre_enter : root.ids.store_name.text = root.manager.store
    on_pre_enter : root.manager.price = 0.00
    BoxLayout:
        orientation: 'vertical'
        TextInput:
            id : store_name
            multiline: False
        Label:
            text: 'Product'
        TextInput:
            id:product
            multiline: False
        Label:
            text: 'Price'
        BoxLayout:
            Label:
                text: '$'
                halign: 'right'
            TextInput:
                id: price
                multiline: False
                text: '0.00'
        Label:
            text: 'Description'
        TextInput:
            id:descr
            multiline: False
        Label:
            text: 'Rating (0.00 - 1.00)'
        TextInput:
            id:rating
            multiline: False
        Label:
            text: 'Comment'
        TextInput:
            id:comment
            multiline: False
        BoxLayout:
            Button:
                text:'Photo'
                on_release: Factory.MyPopup().open()
            #image
        Button:
            text: 'Add'
            on_press:root.create_product(root.ids.store_name.text,root.ids.product.text,root.ids.price.text,root.ids.descr.text,root.ids.rating.text,root.ids.comment.text)
        Button:
            text: 'clear'
            on_press: root.ids.product.text = ''
            on_press: root.ids.price.text = '0.00'
            on_press: root.ids.descr.text = ''
            on_press: root.ids.rating.text = ''
            on_press: root.ids.comment.text = ''
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'main'
""")
class record():
    def __init__(self,id=-1, store=None, product=None, price=None, rating=None,descr=None, comment=None):
        self.id = id
        self.store = store
        self.product = product
        self.price = price
        self.descr = descr
        self.rating = rating
        self.comment = comment
def get_data():
        f = open('records.txt', 'r')
        data = []
        for line in f:
            data.append(line.lower())
        return data
class ViewLog(Screen):
    def text_changed(self,text):
        print(text)
    def search(self, search_phrase, rv):
        results = []
        data = get_data()
        for i in data:
            if search_phrase in i:
                results.append(i)
        rv.data = [{'text':str(x)} for x in results]
        #rv.refresh_from_data()
        print(len(results))
    def init__records(self,rv):
        rv.data = [{'text':str(x)} for x in get_data()]
        #print(self.ids)
class MainScreen(Screen):
    global store
    store = ObjectProperty(None)
    def check(self, store_name0, other_name):
        print(store_name0)
        if(store_name0 == 'other'):
            store = other_name
            print(store)
    pass
class AddRecords(Screen):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_" + timestr)
        print("Captured")
    '''layout = BoxLayout(orientation='vertical', id = 'o')
    cam = Camera(play=True, id = 'camera_id')
    capture_button = Button(text = "Capture")
    capture_button.bind(on_press = capture)
    layout.add_widget(cam)
    layout.add_widget(capture_button)
    popup = Popup(title='Take photo of item', content=layout,auto_dismiss=False)'''
    def create_product(self,s='def',pro='?',pri='0.00',d='...',r='0.00',c='...'):
        print(s,pro,pri,d,r,c)
        f = open("records.txt", "a")
        f.write(s + "|" + pro + "|" + pri + "|" + d + "|" + r + "|" + c + "\n")
        f.close()
    def open_popup(self):
        self.popup.open()
    pass
class MyPopup(Popup):
    def capture(self):
        '''
        Function to capture the images and give them the names
        according to their captured time and date.
        '''
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("IMG_" + timestr)
        print("Captured")



# Create the screen manager
# create custom class for 
sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
sm.add_widget(AddRecords(name='AddRecords'))
sm.add_widget(ViewLog(name='ViewLog'))

class TestApp(App):
    def build(self):
        return sm

if __name__ == '__main__':
     TestApp().run()