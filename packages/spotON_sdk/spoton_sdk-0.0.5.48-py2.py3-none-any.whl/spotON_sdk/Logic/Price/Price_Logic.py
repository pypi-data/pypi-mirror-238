from typing import Any, List, Union
from pydantic import  Field, validator, root_validator
import json

from .timeframes import Timeframes,Timeframe, hours_to_timeframes
from .markets import Market, Markets
from .customBaseModel import CustomBaseModel
from pprint import pprint
import pandas as pd
import pytz

class PricefindingError(ValueError):
    pass

class Interrupted_On_Time(CustomBaseModel):
    name: str = Field(default="Interrupted_On_Time",init = False)
    minimum_hours_on: int = Field(default=1,init = False)
    pass

class Continuous_On_Time(CustomBaseModel):
    name: str = Field(default="Continuous_On_Time",init = False)
    week: int = Field(default=None)
    best_hour: int = Field(default=None)

class Price_Logic(CustomBaseModel):
    nr_of_hours_on: int
    market: Market   
    timeframes: Timeframes = Timeframes()
    pricefinding: Union[Continuous_On_Time, Interrupted_On_Time] = Interrupted_On_Time()
    resolution: float = Field(default=1)
    timeframe_shorter_than_nr_of_hours_on: bool = Field(default=False)

    def __init__(self, **data):
        super().__init__(**data)

        if data.get("pricefinding") is not None:
            self.pricefinding = data["pricefinding"]

    def update_pricefinding(self, pricefinding: Union[Continuous_On_Time, Interrupted_On_Time]):
        if not isinstance(pricefinding, (Continuous_On_Time, Interrupted_On_Time)):
            raise ValueError("Invalid type for pricefinding")
        self.pricefinding = pricefinding

    @root_validator(pre=True)
    def set_market_to_market_object(cls, values):
        if isinstance(values["market"], str):
            result = Markets.get_market_by_name(values["market"])
            result = Markets.get_market_by_code(values["market"])
            if result is None:
                raise ValueError("Market is not valid")
            values["market"] = result
        return values


    def update_timeframes(self, timeframes: Timeframes):
        self.timeframes = timeframes
    


    def to_json(self) -> str:
        switch_pattern_dict = self.to_dict()
        json_str = json.dumps(switch_pattern_dict)

        return json_str
    
    def pack(self) -> dict[str, Any]:
        '''Pack the object into a dictionary'''
        details = {
            "area": self.market.area.name,  
            "nr_of_hours_on": self.nr_of_hours_on,
            "timeframes": self.timeframes.possible_hours,
            "pricefinding": self.pricefinding.name,
            "minimum_hours_on": self.pricefinding.minimum_hours_on#type: ignore
        }
        return details

    def get_start_end_hours_in_UTC(self) -> tuple[pd.Timestamp,pd.Timestamp]:
        return self.market.get_start_end_hours_in_UTC()

    @staticmethod
    def unpack(details: dict[str, Any]) -> "Price_Logic":
        pprint (f"{details=}")
        '''Unpack the dictionary into a Price_Logic object'''
        market = Markets.get_market_by_code(details["area"])
        nr_of_hours_on = details["nr_of_hours_on"]
        timeframes_decimal = details['timeframes']
        minimum_hours_on = details['minimum_hours_on']
        # Convert 'timeframes' list of Decimal to list of int
        timeframes_int = [int(tf) for tf in timeframes_decimal]
        print(f"timeframes_int before unpacking: {timeframes_int}")
        # If there's a function called 'hours_to_timeframes' you want to use, apply it here
        timeframes = hours_to_timeframes(timeframes_int)
        print(f"timeframes after unpacking: {timeframes}")
        pricefinding_class_string = details["pricefinding"]

        price_logic = Price_Logic(market=market, nr_of_hours_on=nr_of_hours_on)
        price_logic.update_timeframes(timeframes)


        if pricefinding_class_string == Interrupted_On_Time().name:
            price_logic.update_pricefinding(Interrupted_On_Time())
            price_logic.pricefinding.minimum_hours_on = int(minimum_hours_on)
        elif pricefinding_class_string == Continuous_On_Time().name:
            price_logic.update_pricefinding(Continuous_On_Time())
        else:
            raise PricefindingError
        

        

        print (f"{price_logic=}")

        return price_logic



    @validator('nr_of_hours_on')
    def validate_nr_of_hours_on(cls, v):
        if v <= 0:
            raise ValueError('nr_of_hours_on must be greater than 0')
        return v

    @root_validator
    def validate_timeframes(cls, values):
        timeframes = values.get('timeframes')
        nr_of_hours_on = values.get('nr_of_hours_on')
        if timeframes and nr_of_hours_on:
            possible_hours = timeframes.possible_hours
            if nr_of_hours_on > len(possible_hours):
                values['timeframe_shorter_than_nr_of_hours_on'] = True
            else:
                values['timeframe_shorter_than_nr_of_hours_on'] = False
        return values