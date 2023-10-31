from locale import currency
from .spotON_Areas import Currency, spotON_Area,Area_details
import pandas as pd
from dataclasses import dataclass, field
from typing import Optional, Dict,Any

from typing import List
from .countries import *
from .bidding_zones import bidding_zones

from .customBaseModel import CustomBaseModel

from pydantic import Field, root_validator,validate_model




class Market(CustomBaseModel):
    area: Area_details
    country: Country
    alias: Optional[str] = None
    cities: str = Field(default="")
    name: str = Field(default= "",init = False)

    @root_validator(pre=True)
    def set_codes(cls, values):
        country = values.get('country')
        if country and 'country_name' in country:
            values["name"] = country['country_name']
        return values
    
    @root_validator(pre=True)
    def set_name(cls, values):
        country :Country= values.get('country')
        area = values.get('area')
        if country and area:
            values["name"] = f"{country.emoji} {country.country_name} {area.name}"
        return values
    


class MarketNotFoundError(ValueError):
    pass



class Markets():

    austria = Market(area=spotON_Area.AT.value,country=all_Countries.Austria)
    germany = Market(area=spotON_Area.DE_LU.value,country=all_Countries.Germany,alias="DE_LU")
    sweden1 = Market(area=spotON_Area.SE_1.value,country=all_Countries.Sweden)    
    #luxembourg = Market(Area.DE_LU,Luxembourg)

    #sweden2 = Market(Area.SE_2,Sweden)
    #sweden3 = Market(Area.SE_3,Sweden)
    #sweden4 = Market(Area.SE_4,Sweden)
    markets_List = [value for key, value in vars().items() if isinstance(value, Market)]
    merged_Markets = []

    @staticmethod
    def get_market_by_name(name: str) -> Optional[Market]:
        for market in Markets.markets_List:
            if market.name == name: # type: ignore
                return market

        raise MarketNotFoundError

    @staticmethod
    def get_market_by_code(area_code: str) -> Optional[Market]:
        for market in Markets.markets_List:
            #print (f"Try to find {area_code =} in {market}")
            if market.country.country_code == area_code or market.alias == area_code:
                return market

        raise MarketNotFoundError





