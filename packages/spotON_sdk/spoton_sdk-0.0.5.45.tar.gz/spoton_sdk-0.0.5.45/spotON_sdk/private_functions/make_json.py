from typing import List, Tuple
from dataclasses import dataclass
import json
import base64

from config_Test import price_Logic1
from spotON_sdk import Market,Price_Logic,Continuous_On_Time,Interrupted_On_Time,Timeframes,Timeframe

@dataclass()
class SwitchPattern:
    area_code :str
    nr_of_hours_on :int
    pricefinding :dict
    resolution :float
    timeframes : List[int]


def convert_switch_pattern(price_Logic1: Price_Logic):
        
    area_code = price_Logic1.market.area_code # type: ignore
    nr_of_hours_on = price_Logic1.nr_of_hours_on
    pricefinding = price_Logic1.pricefinding.__dict__
    resolution = price_Logic1.resolution
    timeframes = price_Logic1.timeframes.possible_hours

    # Create and return a new SwitchPattern object
    return SwitchPattern(area_code, nr_of_hours_on, pricefinding, resolution, timeframes)

def create_escaped_switch_pattern_json(price_Logic:Price_Logic):
    switch_pattern = convert_switch_pattern(price_Logic)

    switch_pattern_json = json.dumps(switch_pattern.__dict__)
    escaped_switch_pattern_json = json.dumps(switch_pattern_json)

    return escaped_switch_pattern_json

def debug():
    print(create_escaped_switch_pattern_json(price_Logic1))


    
switch_pattern = convert_switch_pattern(price_Logic1)
pricefinding_Name = switch_pattern.pricefinding["name"]
if pricefinding_Name == "Continuous_On_Time":
    pricefinding = Continuous_On_Time(week=switch_pattern.pricefinding["week"],
                                      best_hour=switch_pattern.pricefinding["best_hour"])
elif pricefinding_Name == "Interrupted_On_Time":
    pricefinding = Interrupted_On_Time()
else:
    raise Exception("pricefinding_Name is not valid")

start = switch_pattern.timeframes[0]
end = switch_pattern.timeframes[-1]

'''price_Logic = Price_Logic(nr_of_hours_on=switch_pattern.nr_of_hours_on,
            market=switch_pattern.area_code,
            timeframes=Timeframes(Timeframe())'''

print(start,end)


