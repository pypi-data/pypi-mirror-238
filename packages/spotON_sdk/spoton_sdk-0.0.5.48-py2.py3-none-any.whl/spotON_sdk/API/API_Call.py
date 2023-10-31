from dataclasses import dataclass
from ..Logic.Price.customBaseModel import CustomBaseModel
from ..Logic.Price.Price_Logic import Price_Logic
import json

class API_Call(CustomBaseModel):
    spotOn_API_code: str
    price_logic : Price_Logic

    def as_json(self,escaped=False):

        API_Call_dict = self.to_dict()
        json_str = json.dumps(API_Call_dict)
        if escaped:
            json_str = json.dumps(json_str)

        return json_str
    



import aiohttp
import json

from spotON_sdk import Price_Logic,Continuous_On_Time,Markets,Timeframes

async def request_Day_Ahead_Price(data:API_Call):
           
    url = 'https://km28t5snp5.execute-api.eu-central-1.amazonaws.com/Prod/echo'
    #url = 'http://127.0.0.1:8000/echo'



    headers = {'Content-type': 'application/json'} # Set the content type to JSON

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data.json(), headers=headers) as resp:
            print("Header:",resp.headers)
            print("Status:", resp.status)
            print("Content-type:", resp.headers['content-type'])
            #print(data)
            response = await resp.json()
            
            print(response)




