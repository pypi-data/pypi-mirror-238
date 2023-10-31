from typing import List, Tuple
from dataclasses import dataclass
import json
import base64

from pricelogic_Test import price_Logic1
from spotON_sdk import Market,Price_Logic

@dataclass()
class SwitchPattern:
    area_code :str
    nr_of_hours_on :int
    pricefinding :dict
    resolution :float
    timeframes : List[int]

def encode_switch_pattern(switch_pattern: SwitchPattern) -> str:
    switch_pattern_str = json.dumps(switch_pattern.__dict__)
    switch_pattern_bytes = switch_pattern_str.encode('utf-8')
    switch_pattern_b64 = base64.b64encode(switch_pattern_bytes)
    return switch_pattern_b64.decode('utf-8')

def decode_switch_pattern(encoded_switch_pattern: str) -> SwitchPattern:
    switch_pattern_bytes = base64.b64decode(encoded_switch_pattern)
    switch_pattern_str = switch_pattern_bytes.decode('utf-8')
    switch_pattern_dict = json.loads(switch_pattern_str)
    return SwitchPattern(**switch_pattern_dict)

def convert_switch_pattern(price_Logic1: Price_Logic):
        
    area_code = price_Logic1.market.area_code # type: ignore
    nr_of_hours_on = price_Logic1.nr_of_hours_on
    pricefinding = price_Logic1.pricefinding.__dict__
    resolution = price_Logic1.resolution
    timeframes = price_Logic1.timeframes.possible_hours

    # Create and return a new SwitchPattern object
    return SwitchPattern(area_code, nr_of_hours_on, pricefinding, resolution, timeframes)

def debug():

    switch_pattern = convert_switch_pattern(price_Logic1)
    print(switch_pattern)

    # Encode the switch pattern
    switch_pattern_encoded = encode_switch_pattern(switch_pattern)
    print(switch_pattern_encoded)
    

    # Decode the switch pattern
    switch_pattern_decoded = decode_switch_pattern(switch_pattern_encoded)
    print(switch_pattern_decoded)

    # Verify that the decoded switch pattern matches the original
    assert switch_pattern == switch_pattern_decoded



switch_pattern = convert_switch_pattern(price_Logic1)
switch_pattern_encoded = encode_switch_pattern(switch_pattern)
print(f"{switch_pattern_encoded=}")