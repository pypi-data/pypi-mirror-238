from spotON_sdk import *
from pprint import pprint
from spotON_sdk.Logic.Output.Switchtypes import Switchtypes
from spotON_sdk.Logic.Price import Price_Logic
from operator import __ge__,__le__
from spotON_sdk.spotON_controller import Controller

temperature_sensor = Sensor(25,Units.temperature)
switch = Switchtypes.SWITCH
target_value = 27

@dataclass
class all_Configs():
    full_Day_Switch_Config = Price_Logic(nr_of_hours_on=24,
                                         market=Markets.austria,
                                         on_hours=On_Hours(timeframes_list=[Wholeday()]),
                                            pricefinding=Continuous_On_Time(week=1))



@dataclass
class all_Feedbacks():

    heater_feedback = Feedback(sensor=temperature_sensor,
                    target_value=target_value,
                    comperator=__ge__)

    humidifier_feedback = Feedback(sensor=temperature_sensor,
                        target_value=target_value,
                        comperator=__le__)

    dehumidifier_feedback = Feedback(sensor=temperature_sensor,
                        target_value=target_value,
                        comperator=__le__)

@dataclass
class all_Presets():

    heater_Preset = Controller(name="Heater",
                           config = all_Configs.full_Day_Switch_Config,
                           feedback=[all_Feedbacks.heater_feedback],
                           output_Switch=Switchtypes.SWITCH)
    humidity_Preset = Controller(name="Dehumidifier",
                           config = all_Configs.full_Day_Switch_Config,
                           feedback=[all_Feedbacks.humidifier_feedback],
                           output_Switch=Switchtypes.SWITCH)


pprint (all_Presets.heater_Preset)

