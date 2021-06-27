import kivy
#import can
import time
import threading
import os
import queue 

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.config import Config
from kivy.clock import Clock, ClockBaseBehavior
from kivy.animation import Animation
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, BooleanProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.screenmanager import NoTransition

Config.set('graphics','width',1920)
Config.set('graphics','height',1080)
Config.set('graphics','fbo','hardware')
Config.set('graphics','multisamples',-2)
Config.set('graphics','fullscreen',1)


Builder.load_file('main.kv')

global_rpm = 0
global_speed = 0
global_gear = 0
global_coolant_temperature = 0.0
global_head_temperature = 0.0
global_coolant_pressure = 0.0
global_lambda_value = 0.00
global_oil_temperature = 0.0
global_oil_pressure = 0.0
global_battery_voltage = 0.0
global_fuel_pressure = 0.0
global_throttle_percent = 0
global_clutch_percent = 0
global_brake_percent = 0
global_odo = 0
global_tune_mode = 'D'
global_BOTS_status = False
global_BSE_status = False
global_BSPD_status = False
global_TPS_status = False
global_APPS_status = False
global_front_heave = 0.0
global_front_roll = 0.0
global_rear_heave = 0.0
global_rear_roll = 0.0
global_steering_angle = 0
global_front_brake_pressure = 0.0
global_rear_brake_pressure = 0.0
global_brake_temperature = 0.0
global_brake_ratio_text = ':'

CanTX = queue.Queue(maxsize = 5)

class MainScreen(Screen):
    rpm = NumericProperty(0)
    speed = NumericProperty(0)
    gear = NumericProperty(0)
    coolant_temperature = NumericProperty(0.0)
    head_temperature = NumericProperty(0.0)
    coolant_pressure = NumericProperty(0.0)
    lambda_value = NumericProperty(0.00)
    oil_temperature = NumericProperty(0.0)
    oil_pressure = NumericProperty(0.0)
    battery_voltage = NumericProperty(0.0)
    fuel_pressure = NumericProperty(0.0)
    throttle_percent = NumericProperty(0)
    clutch_percent = NumericProperty(0)
    brake_percent = NumericProperty(0)
    time_text = StringProperty(time.strftime("%H:%M:%S"))
    odo = NumericProperty(0)
    tune_mode = StringProperty('D')
    BOTS_status = BooleanProperty(False)
    BSE_status = BooleanProperty(False)
    BSPD_status = BooleanProperty(False)
    TPS_status = BooleanProperty(False)
    APPS_status = BooleanProperty(False)

class SuspensionScreen(Screen):
    front_heave = NumericProperty(0.0)
    front_roll = NumericProperty(0.0)
    rear_heave = NumericProperty(0.0)
    rear_roll = NumericProperty(0.0)
    steering_angle = NumericProperty(0)

class BrakeScreen(Screen):
    front_brake_pressure = NumericProperty(0.0)
    rear_brake_pressure = NumericProperty(0.0)
    brake_temperature = NumericProperty(0.0)
    brake_ratio_text = StringProperty(':')
    
class TrackScreen(Screen):
    global CanTX
    def canSend(self, data):
        CanTX.put(data, block = False)
    current_latitude = NumericProperty(0.0000000)
    current_longitude = NumericProperty(0.0000000)
    beacon_latitude = NumericProperty(0.0000000)
    beacon_longitude = NumericProperty(0.0000000)

class SettingsScreen(Screen):
    ip_address = StringProperty('IP: ')

class DriveModeScreen(Screen):
    pass    


screens = ScreenManager(transition=NoTransition())
screens.add_widget(MainScreen(name = 'MainScreen'))
screens.add_widget(SuspensionScreen(name = 'SuspensionScreen'))
screens.add_widget(BrakeScreen(name = 'BrakeScreen'))
screens.add_widget(TrackScreen(name = 'TrackScreen'))
screens.add_widget(DriveModeScreen(name = 'DriveModeScreen'))
screens.add_widget(SettingsScreen(name = 'SettingsScreen'))

MainScreen = screens.get_screen('MainScreen')
SuspensionScreen = screens.get_screen('SuspensionScreen')
BrakeScreen = screens.get_screen('BrakeScreen')
TrackScreen = screens.get_screen('TrackScreen')
DriveModeScreen = screens.get_screen('DriveModeScreen')
SettingsScreen = screens.get_screen('SettingsScreen')


#CanBus = can.ThreadSafeBus(interface='socketcan', channel='can0', bitrate=1000000)

running_flag = True


def CANComm():
    
    global CanTX

    global global_rpm
    global global_speed
    global global_gear
    global global_coolant_temperature
    global global_head_temperature
    global global_coolant_pressure
    global global_lambda_value
    global global_oil_temperature
    global global_oil_pressure
    global global_battery_voltage
    global global_fuel_pressure
    global global_throttle_percent
    global global_clutch_percent
    global global_brake_percent
    global global_odo
    global global_tune_mode
    global global_BOTS_status
    global global_BSE_status
    global global_BSPD_status
    global global_TPS_status
    global global_APPS_status
    global global_front_heave
    global global_front_roll
    global global_rear_heave
    global global_rear_roll
    global global_steering_angle
    global global_front_brake_pressure
    global global_rear_brake_pressure
    global global_brake_temperature
    global global_brake_ratio_text

    BYTEORDER_CONSTANT = 'big'
    
    while running_flag:

        try:

            if not CanTX.empty():
                msg = can.Message(arbitration_id = 0xff, data = CanTX.get())
                CanBus.send(msg)
                continue

            msg = CanBus.recv(timeout = 0.5)

            if msg != None:

                if msg.arbitration_id == 0x100:
                    if screens.current_screen == MainScreen:
                        global_rpm = int.from_bytes(msg.data[0:2], byteorder = BYTEORDER_CONSTANT, signed = False)
                        global_gear = int.from_bytes(msg.data[2:3], byteorder = BYTEORDER_CONSTANT, signed = False)
                        global_speed = int.from_bytes(msg.data[3:4], byteorder = BYTEORDER_CONSTANT, signed = False)
                        global_throttle_percent = int.from_bytes(msg.data[4:5], byteorder = BYTEORDER_CONSTANT, signed = False)
                        global_clutch_percent = int.from_bytes(msg.data[6:7], byteorder = BYTEORDER_CONSTANT, signed = False)
                    elif screens.current_screen == SuspensionScreen:
                        global_steering_angle = int.from_bytes(msg.data[5:6], byteorder = BYTEORDER_CONSTANT, signed = True)
                    
                elif msg.arbitration_id == 0x101:
                    global_front_brake_pressure = int.from_bytes(msg.data[0:2], byteorder = BYTEORDER_CONSTANT, signed = False) / 10.0
                    global_rear_brake_pressure = int.from_bytes(msg.data[2:4], byteorder = BYTEORDER_CONSTANT, signed = False) / 10.0
                    global_fuel_pressure = int.from_bytes(msg.data[4:6], byteorder = BYTEORDER_CONSTANT, signed = False) / 10.0
                    global_oil_pressure = int.from_bytes(msg.data[6:8], byteorder = BYTEORDER_CONSTANT, signed = False) / 10.0
                    
                    if screens.current_screen == MainScreen:
                        brake_percent_calculation = max(global_front_brake_pressure, global_rear_brake_pressure) / 10.0
                        global_brake_percent = brake_percent_calculation if brake_percent_calculation < 100 else 100
                    elif screens.current_screen == BrakeScreen:
                        total_brake_pressure = BrakeScreen.front_brake_pressure + BrakeScreen.rear_brake_pressure
                        if (total_brake_pressure > 0):
                            global_brake_ratio_text = str(round(BrakeScreen.front_brake_pressure*100.0/total_brake_pressure,1)) + ' : ' + str(round(BrakeScreen.rear_brake_pressure*100.0/total_brake_pressure,1))
                        else:
                            global_brake_ratio_text = ':'
                    
                elif msg.arbitration_id == 0x102:
                    global_coolant_temperature = int.from_bytes(msg.data[0:2], byteorder = BYTEORDER_CONSTANT, signed = True) / 10.0
                    global_head_temperature = int.from_bytes(msg.data[2:4], byteorder = BYTEORDER_CONSTANT, signed = True) / 10.0
                    global_brake_temperature = int.from_bytes(msg.data[4:6], byteorder = BYTEORDER_CONSTANT, signed = True) / 10.0
                    global_battery_voltage = int.from_bytes(msg.data[6:7], byteorder = BYTEORDER_CONSTANT, signed = False) / 10.0
                    global_lambda_value = int.from_bytes(msg.data[7:8], byteorder = BYTEORDER_CONSTANT, signed = False) / 100.0

                elif msg.arbitration_id == 0x103:
                    global_front_heave = int.from_bytes(msg.data[0:2], byteorder = BYTEORDER_CONSTANT, signed = True) / 10.0
                    global_rear_heave = int.from_bytes(msg.data[2:4], byteorder = BYTEORDER_CONSTANT, signed = True) / 10.0
                    global_front_roll = int.from_bytes(msg.data[4:6], byteorder = BYTEORDER_CONSTANT, signed = True) / 10.0
                    global_rear_roll = int.from_bytes(msg.data[6:8], byteorder = BYTEORDER_CONSTANT, signed = True) / 10.0
                    
                    
                elif msg.arbitration_id == 0x104:
                    global_odo = int.from_bytes(msg.data[0:2], byteorder = BYTEORDER_CONSTANT, signed = False)
                    status = int.from_bytes(msg.data[2:3], byteorder = BYTEORDER_CONSTANT, signed = False)
                    global_BOTS_status = status & 0b10000000
                    global_BSE_status = status & 0b01000000
                    global_BSPD_status = status & 0b00100000
                    global_TPS_status = status & 0b00010000
                    global_APPS_status = status & 0b00001000
                     
        except:
            pass

CANCommThread = threading.Thread(target = CANComm)

class main(App):

    def stopApp(self):
        os._exit(0)

    def updateTime(self, *args):
        MainScreen.time_text = time.strftime("%H:%M:%S")

    def updateIpAddress(self, *args):
        try:
            SettingsScreen.ip_address = "IP: " + os.popen('ip addr show wlan0').read().split("inet ")[1].split("/")[0]
        except:
            pass
    
    def updateScreen(self, *args):
        if screens.current_screen == MainScreen:
            MainScreen.rpm = global_rpm
            MainScreen.speed = global_speed
            MainScreen.gear = global_gear
            MainScreen.coolant_temperature = global_coolant_temperature
            MainScreen.head_temperature = global_head_temperature
            MainScreen.coolant_pressure = global_coolant_pressure
            MainScreen.lambda_value = global_lambda_value
            MainScreen.oil_temperature = global_oil_temperature
            MainScreen.oil_pressure = global_oil_pressure
            MainScreen.battery_voltage = global_battery_voltage
            MainScreen.fuel_pressure = global_fuel_pressure
            MainScreen.throttle_percent = global_throttle_percent
            MainScreen.clutch_percent = global_clutch_percent
            MainScreen.brake_percent = global_brake_percent
            MainScreen.odo = global_odo
            MainScreen.tune_mode = global_tune_mode
            MainScreen.BOTS_status = global_BOTS_status
            MainScreen.BSE_status = global_BSE_status
            MainScreen.BSPD_status = global_BSPD_status
            MainScreen.TPS_status = global_TPS_status
            MainScreen.APPS_status = global_APPS_status
        
        elif screens.current_screen == SuspensionScreen:
            SuspensionScreen.front_heave = global_front_heave
            SuspensionScreen.front_roll = global_front_roll
            SuspensionScreen.rear_heave = global_rear_heave
            SuspensionScreen.rear_roll = global_rear_roll
            SuspensionScreen.steering_angle = global_steering_angle
        
        elif screens.current_screen == BrakeScreen:
            BrakeScreen.front_brake_pressure = global_front_brake_pressure
            BrakeScreen.rear_brake_pressure = global_rear_brake_pressure
            BrakeScreen.brake_temperature = global_brake_temperature
            BrakeScreen.brake_ratio_text = global_brake_ratio_text

    def on_start(self):
        Clock.schedule_interval(self.updateTime, 1)
        Clock.schedule_interval(self.updateIpAddress, 3)
        Clock.schedule_interval(self.updateScreen, 0.02)
        CANCommThread.start()

    def on_stop(self):
        global running_flag
        running_flag = False

    def restart(self):
        os.system('sudo reboot')

    def build(self):
        return screens

if __name__ == "__main__":
    main().run()
