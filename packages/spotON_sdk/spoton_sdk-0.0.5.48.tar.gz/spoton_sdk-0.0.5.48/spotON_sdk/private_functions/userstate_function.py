from dataclasses import dataclass,field
from spotON_sdk import Markets,Market,Country,Price_Logic,Interrupted_On_Time,Timeframes




@dataclass
class UserGeography():
    country :Country = field (init=False)
    latitude :float = field(init=False,default=0)
    longitude :float = field(init=False,default=0)
    languages :str = "ENG"
    market :Market = field(init=False)
    

    def __init__(self):
        '''try:
            self.query()
            print ("----  USER GEOGRAPHY (queried)----")
        except:
            self.manual_Country_Set(market=Markets.germany)
            print ("----  USER GEOGRAPHY (set from Preset)----")'''
        self.manual_Country_Set(market=Markets.germany)
        print ("----  USER GEOGRAPHY (set from Preset)----")
        #print (f"\n{self=}\n")

    '''def query(self):
        result = return_User_Geo()
        if result:
            # Got a result from query
            country_Name,countryISO2,timezone,self.latitude,self.longitude,self.languages,countryCapital = result

            retrieved_Zone = retrieve_BiddingZone(self.longitude,self.latitude)

            if retrieved_Zone:
                self.country = Country(countryCapital,countryISO2, country_Name)
                self.market = Markets.get_Market_by_area_code(retrieved_Zone)
                #"Fetching user Geodata Worked"
                
            else:
                # "Error retrieving Bidding Zone from coordinates"
                raise Exception
            
        else:
            # "No Geodata found"
            raise Exception'''
            


    def manual_Country_Set(self,market:Market):
        self.country = market.country
        self.languages :str = "ENG"
        self.market = market


class Plot_Constants():
    def __init__(self,min_price :float,max_price :float):
        self.min_price= min_price * 0.1
        self.max_price = max_price * 0.1
        self.space = (abs(self.max_price) - abs(self.min_price) )*0.2
        self.ylimit = (self.min_price - self.space, self.max_price + self.space)
        print (f"created Plot_Constants {self=}")
    



@dataclass
class UserState:
    
    price_Logic: Price_Logic = field(default_factory=lambda: Price_Logic(nr_of_hours_on=24,
                                                                          market=Markets.germany))
    geography: UserGeography = field(default_factory=UserGeography)
    logged_in: bool = False
    #preview_df_Container: Preview_df_Container = field(init=False)  # Placeholder type, replace with actual type

    def __post_init__(self):
        #self.preview_df_Container = Preview_df_Container(price_Logic=self.price_Logic)
        #print(f"Created UserState  {self=}")
        pass

    def changeMarket(self, new_Market: Market):  # Placeholder type, replace with actual type
        self.geography.manual_Country_Set(new_Market)
        self.price_Logic.market = new_Market

UserState()