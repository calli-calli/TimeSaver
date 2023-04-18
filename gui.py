from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.switch import Switch
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.spinner import Spinner
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
import apiInteractions
import timesheeBuilder
import userConfig

# todo align some both widgets closer together. Read on Layouts in doc


class CalendarName(GridLayout):
    def __init__(self, **kwargs):
        super(CalendarName, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text="Calendar Name:"))
        calendar_name = Spinner(
            text='Home',  # default value shown
            values=('Home', 'Work', 'Other', 'Custom'),  # available values
            # positioning
            # size_hint=(None, None),
            # size=(100, 44),
            # height=44,
            pos_hint={'center_x': .5, 'center_y': .5}, )

        def show_selected_value(spinner, text):
            print('The spinner', spinner, 'has text', text)

        calendar_name.bind(text=show_selected_value)
        self.add_widget(calendar_name)


class Default(BoxLayout):
    def __init__(self, **kwargs):
        super(Default, self).__init__(**kwargs)
        self.orientation = "horizontal"
        self.add_widget(Switch(active=True))
        self.add_widget(Label(text="Default"))


class Start(BoxLayout):
    def __init__(self, **kwargs):
        super(Start, self).__init__(**kwargs)
        self.add_widget(Button(text="Start"))


class OutputDir(BoxLayout):
    def __init__(self, **kwargs):
        super(OutputDir, self).__init__(**kwargs)
        self.orientation = "horizontal"
        # self.option = Label(text="Output Dir:")
        # self.add_widget(self.option)
        self.load = Button(text="Output Path")
        # self.load.bind(on_release=self.show_load)
        self.add_widget(self.load)
        # todo make popup window containing: FileChooserListView, Button("Cancel), Button("Save").
        #  Text on Button("Load") depends on chosen path i.e.: f"Output: {dir}"


class DatePreset(GridLayout):
    def __init__(self, **kwargs):
        super(DatePreset, self).__init__(**kwargs)
        self.cols = 2
        last_month = ToggleButton(text="Last Month", group="date_preset", state="down")
        custom = ToggleButton(text="Custom", group="date_preset")
        self.add_widget(last_month)
        self.add_widget(custom)
        pass


class FullDay(BoxLayout):
    def __init__(self, **kwargs):
        super(FullDay, self).__init__(**kwargs)
        self.full_day = Switch(active=False)
        self.add_widget(self.full_day)
        self.add_widget(Label(text="Full Day Entries"))


class Dates(GridLayout):
    def __init__(self, **kwargs):
        super(Dates, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text="Start Date"))
        self.start_input = TextInput()
        self.add_widget(self.start_input)
        self.add_widget(Label(text="Start Date"))
        self.end_input = TextInput()
        self.add_widget(self.end_input)


class Header(BoxLayout):
    def __init__(self, **kwargs):
        super(Header, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.add_widget(CalendarName())
        self.add_widget(Default())
        self.add_widget(Start())


class Options(BoxLayout):
    def __init__(self, **kwargs):
        super(Options, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.add_widget(OutputDir())
        self.add_widget(DatePreset())
        self.add_widget(FullDay())
        self.add_widget(Dates())


class FullLayout(GridLayout):
    def __init__(self, **kwargs):
        super(FullLayout, self).__init__(**kwargs)
        self.cols = 1
        self.add_widget(Header())
        self.add_widget(Options())


class TimeSaverApp(App):
    def build(self):
        return FullLayout()


# testing
class SayHello(App):
    def build(self):
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        # add widget to window
        # image widget
        self.window.add_widget(Image(source="cover.png"))
        # label widget
        self.greeting = Label(
            text="What's your name",
            font_size=18,
            color="#00FFCE"
        )
        self.window.add_widget(self.greeting)
        # user text input
        self.user = TextInput(
            multiline=False,
            padding_y=(20, 20),
            size_hint=(1, 0.5),
            on_text_validate=self.callback
        )

        self.window.add_widget(self.user)
        # button widget
        self.button = Button(
            text="Greet",
            size_hint=(1, 0.5),
            bold=True,
            background_color="#00FFCE"
        )
        self.button.bind(on_press=self.callback)
        self.window.add_widget(self.button)

        return self.window

    def callback(self, instance):
        self.greeting.text = "Hello " + self.user.text + "!"


if __name__ == "__main__":
    TimeSaverApp().run()
