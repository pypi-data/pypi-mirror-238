import asyncio


from spotON_sdk import API_Call,Timeframes,Price_Logic,Markets,Continuous_On_Time,request_Day_Ahead_Price


from pricelogic_Test import price_Logic1

from spotON_helper.authentification.expireing_Token import generate_token
API_token = generate_token("test")



timeframes = Timeframes()
timeframes.add_timeframe(1,5)
price_Logic1 = Price_Logic(nr_of_hours_on=10,market=Markets.germany,timeframes=timeframes,pricefinding=Continuous_On_Time(week=1,best_hour=1))
#apicode = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMTIzNCIsImV4cCI6MTY4NTU3MzAwOH0.hqPhb7IvpB53qP3NRKkWEd3cp4qtWlND1cVcjTCo-zg"
apicode = generate_token("test")

data = API_Call(spotOn_API_code=apicode,price_logic=price_Logic1)


asyncio.run(request_Day_Ahead_Price(data))