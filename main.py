import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from settingsjson import settings_json
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty
from kivy.clock import Clock
import os
import time
import recipes


#import screen settings
import screens as Screens

from kivy.config import ConfigParser


# config = ConfigParser()
# test = config.read("{}/settings.ini".format("",""))
# print(test)

recipe = {'malt(kg)': 0, 'meske_temp(C)': 0, 'meske_tid': 0,
          'koke_tid': 0, 'humle_1(min)': 0, 'humle_2(min)': 0,
          'humle_3(min)': 0}

recipe.update({'malt(kg)': '45'})
meskevann = recipe.get('malt(kg)')

test_list = []

class MyScreenManager(ScreenManager):
    pass


class Interface(Screen):
    pass


class BrewOne(Screen):
    sec = NumericProperty(0)
    min = NumericProperty(60)
    # set_temp = test_list[3][1]


    def measure_temp(self, *args):
        temp = os.popen("vcgencmd measure_temp").readline()
        temp_real = (temp.replace("temp=", ""))
        return temp_real

    def update_temp(self, *args):
        self.ids['temp'].text = str(self.measure_temp())

    def variables(self):
        self.ids['tempbut'].text = 'Set-Temp:' + str(test_list[3][1])


    def __init__(self, **kwargs):
        super(BrewOne, self).__init__(**kwargs)
        Clock.schedule_interval(self.increment_sec, 1)
        self.increment_sec(0)
        self.increment_min(0)
        Clock.unschedule(self.increment_sec)
        Clock.unschedule(self.increment_min)


    def increment_min(self, interval):
        pass

    def increment_sec(self, interval):
        if self.sec == 0:
            self.sec = 60
            self.min -= 1
        self.sec -= 1

    def start(self):
        Clock.unschedule(self.increment_sec)
        Clock.schedule_interval(self.increment_sec, 1)
        Clock.unschedule(self.increment_min)
        Clock.schedule_interval(self.increment_min, 1)
        Clock.schedule_interval(self.update_temp, 2)
        self.variables()

    def stop(self):
        Clock.unschedule(self.increment_sec)
        Clock.unschedule(self.increment_min)


screen_manager = ScreenManager()

screen_manager.add_widget(Interface(name="interface"))
screen_manager.add_widget(BrewOne(name="brew_one"))


class SettingsApp(App):

    def build(self):
        self.settings_cls = SettingsWithSidebar
        setting = self.config.get('custom', 'beer_recipe')
        print(setting)
        return screen_manager

    def build_config(self, config):
        config.setdefaults('custom', recipes.recipes[0])

        # config.setdefaults('custom', {
        #     'beer_recipe': 'option1',
        #     'mesketid': 'option1',
        #     'koketid': 'option1',
        #     'innmesk_temp': 70,
        #     'mesking_temp': 65,
        #     'utmesk_temp': 78,
        #     'malt1_bol': False,
        #     'malt1_str': 'None',
        #     'malt1_num': 5,
        #     'humle1_bol': True,
        #     'humle1_str': 'None',
        #     'humle1_num': 5,
        #     'humle1_time': 'option1'})

    def build_settings(self, settings):
        settings.add_json_panel('Brew Settings',
                                self.config,
                                data=settings_json)

    def on_config_change(self, config, section, key, value):
        test_list[:] = []
        for a in self.config.items('custom'):
            test_list.append(a)
        # print(test_list)
        if self.config.get('custom','beer_recipe') == 'big wave':
            config.setdefaults('big wave', recipes.recipes[1])
            print('yes')


SettingsApp().run()