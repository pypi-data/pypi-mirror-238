from pprint import pprint as pprint

from spotON_sdk import Price_Logic,Markets,Market,Timeframes,Continuous_On_Time,Timeframe
from spotON_sdk.Logic.Price.Price_Logic import Interrupted_On_Time

import base64
#  Test 1 Create Price_Logic Objects
timeframes = Timeframes()
timeframes.add_timeframe(1,5)
price_Logic1 = Price_Logic(nr_of_hours_on=10,market=Markets.germany,timeframes=timeframes,pricefinding=Continuous_On_Time(week=1,best_hour=1))
price_Logic2 = Price_Logic(nr_of_hours_on=10,market=Markets.germany,timeframes=timeframes,pricefinding=Interrupted_On_Time())
price_Logic3 = Price_Logic(nr_of_hours_on=24,market=Markets.germany)
timeframes = Timeframe(start=1,end=5)
print (f"{price_Logic1.timeframes.possible_hours=}")
pprint(price_Logic3.dict())

# Test 2 JSON 
price_Logic1_json = price_Logic1.to_json()

print(price_Logic1_json)

# Test 3 create API_Call object
from spotON_sdk import API_Call
from spotON_helper.authentification.expireing_Token import generate_token,verify_token
# wirte a test token
token = generate_token('test_user_id')
print(f"{token=}")

# verify the token
result = verify_token(token)
print(f"{result=}")

apiCall = API_Call(spotOn_API_code=token,price_logic=price_Logic1)

api_call_data_Json = apiCall.as_json(escaped=False)
print(f"{api_call_data_Json=}")

api_call_instance = API_Call.parse_raw(api_call_data_Json)
print(f"{api_call_instance=}")
print(f"{type(api_call_instance)=}")


escaped_api_call_data_Json = apiCall.as_json(escaped=True)
print(f"{escaped_api_call_data_Json=}")

