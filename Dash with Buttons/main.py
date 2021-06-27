from typing import Set
import kivy
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
from kivy import Config
from kivy.clock import Clock, ClockBaseBehavior
from kivy.animation import Animation
from kivy.properties import (ObjectProperty, NumericProperty,
                             StringProperty, BooleanProperty)
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.screenmanager import NoTransition
from kivy.base import runTouchApp
import can
from gpiozero import LED as gpioLED
from gpiozero import Button as gpioButton
from enum import Enum


class Button_Enum(Enum):
    BLANK = 0
    ENTER = 1
    RIGHT = 2
    LEFT = 3
    UP = 4
    DOWN = 5


class Button_states(Enum):
    SELECTED = 'down'
    NOT_SELECTED = 'normal'


class inputManager:
    # This class will handle creating physical buttons
    def __init__(self):
        pass

    def buttonEnterPressed(self):
        global isPressed
        global led
        if isPressed == Button_Enum.BLANK:
            isPressed = Button_Enum.ENTER
            led.on()
            main.kivy_manager.key_down(Button_Enum.ENTER)

    def buttonEnterReleased(self):
        global isPressed
        global led
        if isPressed == Button_Enum.ENTER:
            led.off()
            main.kivy_manager.key_up(Button_Enum.ENTER)
            isPressed = Button_Enum.BLANK

    def buttonRightPressed(self):
        global isPressed
        global led
        if isPressed == Button_Enum.BLANK:
            isPressed = Button_Enum.RIGHT
            main.kivy_manager.key_down(Button_Enum.RIGHT)

    def buttonRightReleased(self):
        global isPressed
        global led
        if isPressed == Button_Enum.RIGHT:
            main.kivy_manager.key_up(Button_Enum.RIGHT)
            isPressed = Button_Enum.BLANK

    def buttonLeftPressed(self):
        global isPressed
        global led
        if isPressed == Button_Enum.BLANK:
            isPressed = Button_Enum.LEFT
            main.kivy_manager.key_down(Button_Enum.LEFT)

    def buttonLeftReleased(self):
        global isPressed
        global led
        if isPressed == Button_Enum.LEFT:
            main.kivy_manager.key_up(Button_Enum.LEFT)
            isPressed = Button_Enum.BLANK

    def buttonUpPressed(self):
        global isPressed
        global led
        if isPressed == Button_Enum.BLANK:
            isPressed = Button_Enum.UP
            main.kivy_manager.key_down(Button_Enum.UP)

    def buttonUpReleased(self):
        global isPressed
        global led
        if isPressed == Button_Enum.UP:
            main.kivy_manager.key_up(Button_Enum.UP)
            isPressed = Button_Enum.BLANK

    def buttonDownPressed(self):
        global isPressed
        global led
        if isPressed == Button_Enum.BLANK:
            isPressed = Button_Enum.DOWN
            main.kivy_manager.key_down(Button_Enum.DOWN)

    def buttonDownReleased(self):
        global isPressed
        global led
        if isPressed == Button_Enum.DOWN:
            main.kivy_manager.key_up(Button_Enum.DOWN)
            isPressed = Button_Enum.BLANK


class kivyScreenManager:
    # TODO button calls will call to here and update ScreenManager
    #   * Manage Selected attributes of buttons on screens
    #   * Change Screen based on touch or button input
    def __init__(self):
        self.current_screen = 'MainScreen'
        self.screen_obj = MainScreen
        self.reg_screens = ['MainScreen', 'SuspensionScreen', 'BrakeScreen',
                            'TrackScreen', 'DriveModeScreen', 'SettingsScreen',
                            'SetupScreen']
        self.Fuel_level = 0
        self.Throttle_level = 0
        self.Traction_level = 0
        self.Launch_level = 0
        self.Gearbox_level = 0
        # Maybe have the screenManager reference saved to directly call upon.

    def change_screen(self, name):
        global screens
        if name == 'MainScreen':
            self.current_screen = 'MainScreen'
            self.screen_obj = MainScreen
        elif name == 'SuspensionScreen':
            self.current_screen = 'SuspensionScreen'
            self.screen_obj =SuspensionScreen
        elif name == 'BrakeScreen':
            self.current_screen = 'BrakeScreen'
            self.screen_obj =BrakeScreen
        elif name == 'TrackScreen':
            self.current_screen = 'TrackScreen'
            self.screen_obj =TrackScreen
        elif name == 'DriveModeScreen':
            self.current_screen = 'DriveModeScreen'
            self.screen_obj =DriveModeScreen
        elif name == 'SettingsScreen':
            self.current_screen = 'SettingsScreen'
            self.screen_obj =SettingsScreen
        elif name == 'SetupScreen':
            self.current_screen = 'SetupScreen'
            self.screen_obj =SetupScreen
        screens.current = self.current_screen
        self.screen_obj.ids[self.screen_obj.button_keys[self.screen_obj.selected_pos[0]][self.screen_obj.selected_pos[1]]].state = 'down'

    def key_down(self, direction):
        pass

    def key_up(self, direction, *kwargs):
        if self.current_screen == 'MainScreen':
            self.screen_key_event(direction=direction,screen_obj=MainScreen)
        elif self.current_screen == 'SuspensionScreen':
            self.screen_key_event(direction=direction,screen_obj=SuspensionScreen)
        elif self.current_screen == 'BrakeScreen':
            self.screen_key_event(direction=direction,screen_obj=BrakeScreen)
        elif self.current_screen == 'TrackScreen':
            self.screen_key_event(direction=direction,screen_obj=TrackScreen)
        elif self.current_screen == 'DriveModeScreen':
            self.screen_key_event(direction=direction,screen_obj=DriveModeScreen)
        elif self.current_screen == 'SettingsScreen':
            self.screen_key_event(direction=direction,screen_obj=SettingsScreen)
        elif self.current_screen == 'SetupScreen':
            self.screen_key_event(direction=direction,screen_obj=SetupScreen)

    def screen_key_event(self,direction,screen_obj):
        if direction == Button_Enum.RIGHT:
            if len(screen_obj.button_keys[screen_obj.selected_pos[0]]) > screen_obj.selected_pos[1] +1: # if it can move right
                screen_obj.ids[screen_obj.button_keys[screen_obj.selected_pos[0]][screen_obj.selected_pos[1]]].state = 'normal'
                screen_obj.selected_pos[1] += 1
            else: # Cannot move right
                screen_obj.ids[screen_obj.button_keys[screen_obj.selected_pos[0]][screen_obj.selected_pos[1]]].state = 'normal'
                screen_obj.selected_pos[1] = 0

        elif direction == Button_Enum.LEFT:
            if 0 <= screen_obj.selected_pos[1]-1: # if it can move Left
                screen_obj.ids[screen_obj.button_keys[screen_obj.selected_pos[0]][screen_obj.selected_pos[1]]].state = 'normal'
                screen_obj.selected_pos[1] -= 1
            else: # Cannot move Left
                screen_obj.ids[screen_obj.button_keys[screen_obj.selected_pos[0]][screen_obj.selected_pos[1]]].state = 'normal'
                screen_obj.selected_pos[1] = len(screen_obj.button_keys[screen_obj.selected_pos[0]]) - 1

        elif direction == Button_Enum.UP:
            if 0 <= screen_obj.selected_pos[0] - 1: # if it can move Up
                screen_obj.ids[screen_obj.button_keys[screen_obj.selected_pos[0]][screen_obj.selected_pos[1]]].state = 'normal'
                screen_obj.selected_pos[0] -= 1
            else: # Cannot move Up
                screen_obj.ids[screen_obj.button_keys[screen_obj.selected_pos[0]][screen_obj.selected_pos[1]]].state = 'normal'
                screen_obj.selected_pos[0] = len(screen_obj.button_keys) - 1
            while len(screen_obj.button_keys[screen_obj.selected_pos[0]])-1 < screen_obj.selected_pos[1]:
                screen_obj.selected_pos[1] -= 1

        elif direction == Button_Enum.DOWN:
            if len(screen_obj.button_keys)-1 >= screen_obj.selected_pos[0]+1: # if it can move Down
                screen_obj.ids[screen_obj.button_keys[screen_obj.selected_pos[0]][screen_obj.selected_pos[1]]].state = 'normal'
                screen_obj.selected_pos[0] += 1
            else: # Cannot move Down
                screen_obj.ids[screen_obj.button_keys[screen_obj.selected_pos[0]][screen_obj.selected_pos[1]]].state = 'normal'
                screen_obj.selected_pos[0] = 0
            while len(screen_obj.button_keys[screen_obj.selected_pos[0]])-1 < screen_obj.selected_pos[1]:
                screen_obj.selected_pos[1] -= 1

        elif direction == Button_Enum.ENTER:
            screen_obj.ids[screen_obj.button_keys[screen_obj.selected_pos[0]][screen_obj.selected_pos[1]]].trigger_action()
            self.Clear_button_row(screen_obj.button_keys[screen_obj.selected_pos[0]],screen_obj=screen_obj)

        screen_obj.ids[screen_obj.button_keys[screen_obj.selected_pos[0]][screen_obj.selected_pos[1]]].state = 'down'        
    
    def Clear_button_row(self,array,screen_obj):
        for x in array:
            screen_obj.ids[x].background_color = (1,1,1,1)

Config.set('graphics', 'width', 1920)
Config.set('graphics', 'height', 1080)
Config.set('graphics', 'fbo', 'hardware')
Config.set('graphics', 'multisamples', -2)
Config.set('graphics', 'fullscreen', 1)
Config.set('graphics', 'window_state', 'maximized')

Builder.load_file('main.kv')

# initialize global variables
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
global_tune_mode = 'Null'
global_BOTS_status = False
global_BSE_status = False
global_BSPD_status = False
global_TPS_status = False
global_APPS_status = False
global_APPSA_status = False
global_BSEA_status = False
global_front_heave = 0.0
global_front_roll = 0.0
global_rear_heave = 0.0
global_rear_roll = 0.0
global_steering_angle = 0
global_front_brake_pressure = 0.0
global_rear_brake_pressure = 0.0
global_brake_temperature = 0.0
global_brake_ratio_text = ':'

# Setup Screen Variables
global_front_right_tire_pressure = 00.0
global_front_right_cam = 0.0
global_front_right_toe = 0.0
global_front_right_press = 0.0

global_front_left_tire_pressure = 00.0
global_front_left_cam = 0.0
global_front_left_toe = 0.0
global_front_left_press = 0.0

global_rear_right_tire_pressure = 00.0
global_rear_right_cam = 0.0
global_rear_right_toe = 0.0
global_rear_right_press = 0.0

global_rear_left_tire_pressure = 00.0
global_rear_left_cam = 0.0
global_rear_left_toe = 0.0
global_rear_left_press = 0.0

global_front_heave = 000
global_front_heave_lsr = 0
global_front_heave_lsc = 0
global_front_heave_hsr = 0

global_front_roll = 000
global_front_roll_lsr = 0
global_front_roll_lsc = 0
global_front_roll_hsr = 0

global_rear_heave = 000
global_rear_heave_lsr = 0
global_rear_heave_lsc = 0
global_rear_heave_hsr = 0

global_rear_roll = 000
global_rear_roll_lsr = 0
global_rear_roll_lsc = 0
global_rear_roll_hsr = 0

global_diff_preload = 000
global_accel_ramp_ang = 00
global_decel_ramp_ang = 00

# Tune modes
global_tune1 = -1
global_tune2 = -1

class MainScreen(Screen):
    selected_pos = [0,0] # y,x
    button_keys = [['Drive_Mode','Brake','Suspension','Track','Setup']]

    # Screen variables
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
    time_text = StringProperty(time.strftime("%H:%M"))
    odo = NumericProperty(0)
    tune_mode = StringProperty('Null')
    BOTS_status = BooleanProperty(False)
    BSE_status = BooleanProperty(False)
    BSPD_status = BooleanProperty(False)
    TPS_status = BooleanProperty(False)
    APPS_status = BooleanProperty(False)
    BSEA_status = BooleanProperty(False)
    APPSA_status = BooleanProperty(False)

class SuspensionScreen(Screen):
    selected_pos = [0,0] # y,x
    button_keys = [['Return']]

    # Screen variables
    front_heave = NumericProperty(0.0)
    front_roll = NumericProperty(0.0)
    rear_heave = NumericProperty(0.0)
    rear_roll = NumericProperty(0.0)
    steering_angle = NumericProperty(0)

class BrakeScreen(Screen):
    selected_pos = [0,0] # y,x
    button_keys = [['Return']]

    # Screen variables
    front_brake_pressure = NumericProperty(0.0)
    rear_brake_pressure = NumericProperty(0.0)
    brake_temperature = NumericProperty(0.0)
    brake_ratio_text = StringProperty(':')

class TrackScreen(Screen):
    selected_pos = [0,0] # y,x
    button_keys = [['Return','Set_Beacon']]

    current_latitude = NumericProperty(0.0000000)
    current_longitude = NumericProperty(0.0000000)
    beacon_latitude = NumericProperty(0.0000000)
    beacon_longitude = NumericProperty(0.0000000)

class SettingsScreen(Screen):
    selected_pos = [2,0] # y,x
    button_keys = [['Launch_Terminal'],['Restart_Dash'],['Return']]

    ip_address = StringProperty('IP: ')

class DriveModeScreen(Screen):
    selected_pos = [5,0] # y,x
    button_keys = [['Gearbox_Manual','Gearbox_Auto','Gearbox_Drag'],
                    ['Launch_D','Launch_OFF','Launch_1','Launch_2','Launch_3','Launch_4','Launch_5','Launch_6','Launch_7','Launch_8','Launch_9'],
                    ['Traction_D','Traction_OFF','Traction_1','Traction_2','Traction_3','Traction_4','Traction_5','Traction_6','Traction_7','Traction_8','Traction_9'],
                    ['Throttle_Normal','Throttle_Normal2','Throttle_Skipad','Throttle_Drag'],
                    ['Fuel_A','Fuel_B','Fuel_C','Fuel_D'],
                    ['Return']]

    front_ride_height = NumericProperty(0.0)
    rear_ride_height = NumericProperty(0.0)

class SetupScreen(Screen):
    selected_pos = [0,0] # y,x
    button_keys = [['Return','Tires','Heave','Roll','Diff']]

    front_right_tire_pressure = NumericProperty(99.9)
    front_right_cam = NumericProperty(9.9)
    front_right_toe = NumericProperty(9.9)
    front_right_press = NumericProperty(0.0)

    front_left_tire_pressure = NumericProperty(99.9)
    front_left_cam = NumericProperty(9.9)
    front_left_toe = NumericProperty(9.9)
    front_left_press = NumericProperty(0.0)

    rear_right_tire_pressure = NumericProperty(99.9)
    rear_right_cam = NumericProperty(9.9)
    rear_right_toe = NumericProperty(9.9)
    rear_right_press = NumericProperty(0.0)

    rear_left_tire_pressure = NumericProperty(99.9)
    rear_left_cam = NumericProperty(9.9)
    rear_left_toe = NumericProperty(9.9)
    rear_left_press = NumericProperty(0.0)

    front_heave = NumericProperty(999)
    front_heave_lsr = NumericProperty(9)
    front_heave_lsc = NumericProperty(9)
    front_heave_hsr = NumericProperty(9)

    front_roll = NumericProperty(999)
    front_roll_lsr = NumericProperty(9)
    front_roll_lsc = NumericProperty(9)
    front_roll_hsr = NumericProperty(9)

    rear_heave = NumericProperty(999)
    rear_heave_lsr = NumericProperty(9)
    rear_heave_lsc = NumericProperty(9)
    rear_heave_hsr = NumericProperty(9)

    rear_roll = NumericProperty(999)
    rear_roll_lsr = NumericProperty(9)
    rear_roll_lsc = NumericProperty(9)
    rear_roll_hsr = NumericProperty(9)

    diff_preload = NumericProperty(999)
    accel_ramp_ang = NumericProperty(99)
    decel_ramp_ang = NumericProperty(99)

class TireScreen(Screen):
    pass


class HeaveScreen(Screen):
    pass


class RollScreen(Screen):
    pass


class DiffScreen(Screen):
    pass


screens = ScreenManager(transition=NoTransition())
screens.add_widget(MainScreen(name='MainScreen'))
screens.add_widget(SuspensionScreen(name='SuspensionScreen'))
screens.add_widget(BrakeScreen(name='BrakeScreen'))
screens.add_widget(TrackScreen(name='TrackScreen'))
screens.add_widget(DriveModeScreen(name='DriveModeScreen'))
screens.add_widget(SettingsScreen(name='SettingsScreen'))

screens.add_widget(SetupScreen(name="SetupScreen"))
screens.add_widget(TireScreen(name="TireScreen"))
screens.add_widget(HeaveScreen(name="HeaveScreen"))
screens.add_widget(RollScreen(name="RollScreen"))
screens.add_widget(DiffScreen(name="DiffScreen"))

MainScreen = screens.get_screen('MainScreen')
SuspensionScreen = screens.get_screen('SuspensionScreen')
BrakeScreen = screens.get_screen('BrakeScreen')
TrackScreen = screens.get_screen('TrackScreen')
DriveModeScreen = screens.get_screen('DriveModeScreen')
SettingsScreen = screens.get_screen('SettingsScreen')

SetupScreen = screens.get_screen('SetupScreen')
TireScreen = screens.get_screen('TireScreen')
HeaveScreen = screens.get_screen('HeaveScreen')
RollScreen = screens.get_screen('RollScreen')
DiffScreen = screens.get_screen('DiffScreen')


CanBus = can.ThreadSafeBus(interface='socketcan', channel='can0', bitrate=1000000)  # TODO

running_flag = True


def CANComm():

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

    # Setup Screen Variables
    global global_front_right_tire_pressure
    global global_front_right_cam
    global global_front_right_toe
    global global_front_right_press
    global global_front_left_tire_pressure
    global global_front_left_cam
    global global_front_left_toe
    global global_front_left_press
    global global_rear_right_tire_pressure
    global global_rear_right_cam
    global global_rear_right_toe
    global global_rear_right_press
    global global_rear_left_tire_pressure
    global global_rear_left_cam
    global global_rear_left_toe
    global global_rear_left_press
    global global_front_heave
    global global_front_heave_lsr
    global global_front_heave_lsc
    global global_front_heave_hsr
    global global_front_roll
    global global_front_roll_lsr
    global global_front_roll_lsc
    global global_front_roll_hsr
    global global_rear_heave
    global global_rear_heave_lsr
    global global_rear_heave_lsc
    global global_rear_heave_hsr
    global global_rear_roll
    global global_rear_roll_lsr
    global global_rear_roll_lsc
    global global_rear_roll_hsr
    global global_diff_preload
    global global_accel_ramp_ang
    global global_decel_ramp_ang
    global global_tune1
    global global_tune2
    global global_BSEA_status #added 5-23-21
    global global_APPSA_status #added 5-23-21
    

    BYTEORDER_CONSTANT = 'big'

    while running_flag:

        try:

            msg = CanBus.recv(timeout=0.5)

            if msg != None:  # msg is not None:

                if msg.arbitration_id == 0x100:
                    if screens.current_screen == MainScreen:
                        global_rpm = int.from_bytes(msg.data[0:2], byteorder=BYTEORDER_CONSTANT, signed=False)
                        global_gear = int.from_bytes(msg.data[2:3], byteorder=BYTEORDER_CONSTANT, signed=False)
                        global_speed = int.from_bytes(msg.data[3:4], byteorder=BYTEORDER_CONSTANT, signed=False)
                        global_throttle_percent = int.from_bytes(msg.data[4:5], byteorder=BYTEORDER_CONSTANT, signed=False)
                        global_clutch_percent = int.from_bytes(msg.data[6:7], byteorder=BYTEORDER_CONSTANT, signed=False)
                    elif screens.current_screen == SuspensionScreen:
                        global_steering_angle = int.from_bytes(msg.data[5:6], byteorder=BYTEORDER_CONSTANT, signed=True)

                elif msg.arbitration_id == 0x101:
                    global_front_brake_pressure = int.from_bytes(msg.data[0:2], byteorder=BYTEORDER_CONSTANT, signed=False) / 10.0
                    global_rear_brake_pressure = int.from_bytes(msg.data[2:4], byteorder=BYTEORDER_CONSTANT, signed=False) / 10.0
                    global_fuel_pressure = int.from_bytes(msg.data[4:6], byteorder=BYTEORDER_CONSTANT, signed=False) / 10.0
                    global_oil_pressure = int.from_bytes(msg.data[6:8], byteorder=BYTEORDER_CONSTANT, signed=False) / 10.0

                    if screens.current_screen == MainScreen:
                        brake_percent_calculation = max(global_front_brake_pressure, global_rear_brake_pressure) / 10.0
                        global_brake_percent = brake_percent_calculation if brake_percent_calculation < 100 else 100
                    elif screens.current_screen == BrakeScreen:
                        total_brake_pressure = BrakeScreen.front_brake_pressure + BrakeScreen.rear_brake_pressure
                        if (total_brake_pressure > 0):
                            global_brake_ratio_text = str(round(BrakeScreen.front_brake_pressure*100.0/total_brake_pressure, 1)) + ' : ' + str(round(BrakeScreen.rear_brake_pressure*100.0/total_brake_pressure, 1))
                        else:
                            global_brake_ratio_text = ':'

                elif msg.arbitration_id == 0x102:
                    global_coolant_temperature = int.from_bytes(msg.data[0:2], byteorder=BYTEORDER_CONSTANT, signed=True) / 10.0
                    global_head_temperature = int.from_bytes(msg.data[2:4], byteorder=BYTEORDER_CONSTANT, signed=True) / 10.0
                    global_brake_temperature = int.from_bytes(msg.data[4:6], byteorder=BYTEORDER_CONSTANT, signed=True) / 10.0
                    global_battery_voltage = int.from_bytes(msg.data[6:7], byteorder=BYTEORDER_CONSTANT, signed=False) / 10.0
                    global_lambda_value = int.from_bytes(msg.data[7:8], byteorder=BYTEORDER_CONSTANT, signed=False) / 100.0

                elif msg.arbitration_id == 0x103:
                    global_front_heave = int.from_bytes(msg.data[0:2], byteorder=BYTEORDER_CONSTANT, signed=True) / 10.0
                    global_rear_heave = int.from_bytes(msg.data[2:4], byteorder=BYTEORDER_CONSTANT, signed=True) / 10.0
                    global_front_roll = int.from_bytes(msg.data[4:6], byteorder=BYTEORDER_CONSTANT, signed=True) / 10.0
                    global_rear_roll = int.from_bytes(msg.data[6:8], byteorder=BYTEORDER_CONSTANT, signed=True) / 10.0

                elif msg.arbitration_id == 0x104:
                    global_odo = int.from_bytes(msg.data[0:2], byteorder=BYTEORDER_CONSTANT, signed=False)
                    status = int.from_bytes(msg.data[2:3], byteorder=BYTEORDER_CONSTANT, signed=False)
                    global_BOTS_status = status & 0b10000000
                    global_BSE_status = status & 0b01000000
                    global_BSPD_status = status & 0b00100000
                    global_TPS_status = status & 0b00010000
                    global_APPS_status = status & 0b00001000
                    global_BSEA_status = status & 0b00000100 #added BAGR
                    global_APPSA_status = status & 0b00000010 #added AAGR
                    global_tune1 =  int.from_bytes(msg.data[3:4], byteorder = BYTEORDER_CONSTANT, signed = False) #added
                    global_tune2 = status & 0b00000001 #added changed
                    
                    if global_tune1 == 0:
                        global_tune_mode = 'F'
                    elif global_tune1 == 1:
                        global_tune_mode = 'M'
                    elif global_tune1 == 2:
                        if global_tune2 == 0:
                            global_tune_mode = 'A'
                        elif global_tune2 == 1:
                            global_tune_mode = 'D'
                        else:
                            global_tune_mode = 'F2'

        except:  # Whats giving the error
            pass


CANCommThread = threading.Thread(target=CANComm)

isPressed = Button_Enum.BLANK
led = gpioLED("board35")
buttonEnter = gpioButton("board33")
buttonLeft = gpioButton("board31")
buttonRight = gpioButton("board37")
buttonUp = gpioButton("board40")
buttonDown = gpioButton("board38")
buttonEnter.when_pressed = inputManager.buttonEnterPressed
buttonEnter.when_released = inputManager.buttonEnterReleased
buttonLeft.when_pressed = inputManager.buttonLeftPressed
buttonLeft.when_released = inputManager.buttonLeftReleased
buttonRight.when_pressed = inputManager.buttonRightPressed
buttonRight.when_released = inputManager.buttonRightReleased
buttonUp.when_pressed = inputManager.buttonUpPressed
buttonUp.when_released = inputManager.buttonUpReleased
buttonDown.when_pressed = inputManager.buttonDownPressed
buttonDown.when_released = inputManager.buttonDownReleased


class main(App):
    kivy_manager = kivyScreenManager()

    def sendCanMsg(self, func, msg_data):
        
        try:
            if func == 'ThrottleMap':
                msg = can.Message(arbitration_id = 0xFF, is_extended_id = False, data = [0,msg_data])
                           
            elif func == 'SetBeacon':  
                msg = can.Message(arbitration_id = 0xFF, is_extended_id = False, data = [1])
                
            elif func == 'RideHeight':
                msg = can.Message(arbitration_id = 0xFF, is_extended_id = False, data = [2] + list(struct.pack("!f", msg_data)))
               
            elif func == 'TractionSlipMap':
                msg = can.Message(arbitration_id = 0xFF, is_extended_id = False, data = [3,msg_data])
                
            elif func == 'TractionRangeMap':
                msg = can.Message(arbitration_id = 0xFF, is_extended_id = False, data = [4,msg_data])
                
            elif func == 'LaunchMap':
                msg = can.Message(arbitration_id = 0xFF, is_extended_id = False, data = [5,msg_data]) 
                
            elif func == 'ShiftMode':
                msg = can.Message(arbitration_id = 0xFF, is_extended_id = False, data = [6,msg_data])
                
            elif func == 'EngineMap':
                msg = can.Message(arbitration_id = 0xFF, is_extended_id = False, data = [7,msg_data])    
               
            CanBus.send(msg)
        except:
            pass

    def stopApp(self):
        os._exit(0)

    def updateTime(self, *args):
        MainScreen.time_text = time.strftime("%H:%M")

    def updateIpAddress(self, *args):
        try:
            SettingsScreen.ip_address = "IP: " + os.popen('ip addr show wlan0').read().split("inet ")[1].split("/")[0]  # TODO uncomment later.
        except:  # Whats giving the error
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
            MainScreen.APPSA_status = global_APPSA_status #added 5-22-21
            MainScreen.BSEA_status = global_BSEA_status #added 5-22-21

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

        elif screens.current_screen == SetupScreen:
            SetupScreen.front_right_tire_pressure = global_front_right_tire_pressure
            SetupScreen.front_right_cam = global_front_right_cam
            SetupScreen.front_right_toe = global_front_right_toe
            SetupScreen.front_right_press = global_front_right_press
            SetupScreen.front_left_tire_pressure = global_front_left_tire_pressure
            SetupScreen.front_left_cam = global_front_left_cam
            SetupScreen.front_left_toe = global_front_left_toe
            SetupScreen.front_left_press = global_front_left_press
            SetupScreen.rear_right_tire_pressure = global_rear_right_tire_pressure
            SetupScreen.rear_right_cam = global_rear_right_cam
            SetupScreen.rear_right_toe = global_rear_right_toe
            SetupScreen.rear_right_press = global_rear_right_press
            SetupScreen.rear_left_tire_pressure = global_rear_left_tire_pressure
            SetupScreen.rear_left_cam = global_rear_left_cam
            SetupScreen.rear_left_toe = global_rear_left_toe
            SetupScreen.rear_left_press = global_rear_left_press
            SetupScreen.front_heave = global_front_heave
            SetupScreen.front_heave_lsr = global_front_heave_lsr
            SetupScreen.front_heave_lsc = global_front_heave_lsc
            SetupScreen.front_heave_hsr = global_front_heave_hsr
            SetupScreen.front_roll = global_front_roll
            SetupScreen.front_roll_lsr = global_front_roll_lsr
            SetupScreen.front_roll_lsc = global_front_roll_lsc
            SetupScreen.front_roll_hsr = global_front_roll_hsr
            SetupScreen.rear_heave = global_rear_heave
            SetupScreen.rear_heave_lsr = global_rear_heave_lsr
            SetupScreen.rear_heave_lsc = global_rear_heave_lsc
            SetupScreen.rear_heave_hsr = global_rear_heave_hsr
            SetupScreen.rear_roll = global_rear_roll
            SetupScreen.rear_roll_lsr = global_rear_roll_lsr
            SetupScreen.rear_roll_lsc = global_rear_roll_lsc
            SetupScreen.rear_roll_hsr = global_rear_roll_hsr
            SetupScreen.diff_preload = global_diff_preload
            SetupScreen.accel_ramp_ang = global_accel_ramp_ang
            SetupScreen.decel_ramp_ang = global_decel_ramp_ang

        elif screens.current_screen == TireScreen:
            pass

        elif screens.current_screen == HeaveScreen:
            pass

        elif screens.current_screen == RollScreen:
            pass

        elif screens.current_screen == DiffScreen:
            pass

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
