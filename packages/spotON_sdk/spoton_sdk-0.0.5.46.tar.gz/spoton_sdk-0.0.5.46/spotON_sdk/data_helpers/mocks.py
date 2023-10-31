
import pandas as pd
import pytz

class Timestamps_for_Testing:
    ''' get a timestamp for a special timezones and dates for testing purposes
    
    usage example:timestamp = Timestamps_for_Testing("Europe/Berlin").day_before_summer_winter_timechange_end
    returns a timestamp for the day before the summer winter timechange end in Berlin

    
    this line adds all edge cases for the timestamps:
    summer_winter_timechange_start,summer_winter_timechange_end,day_before_summer_winter_timechange_start,day_before_summer_winter_timechange_end,winter_summer_timechange_start,winter_summer_timechange_end,day_before_winter_summer_timechange_start,day_before_winter_summer_timechange_end,normalday_start,normalday_end = Timestamps_for_Testing("Europe/Berlin").return_all_timestamps() 
    '''

    def __init__(self,timezone :str) -> None:
        self.timezone = timezone
        self.summer_winter_timechange_start = pd.Timestamp(2023,10,29,0,0,0).tz_localize(timezone)
        self.summer_winter_timechange_end = pd.Timestamp(2023,10,29,23,0,0).tz_localize(timezone)
        self.day_before_summer_winter_timechange_start = pd.Timestamp(2023,10,28,0,0,0).tz_localize(timezone)
        self.day_before_summer_winter_timechange_end = pd.Timestamp(2023,10,28,23,0,0).tz_localize(timezone)
        self.winter_summer_timechange_start = pd.Timestamp(2021,3,28,0,0,0).tz_localize(timezone)
        self.winter_summer_timechange_end = pd.Timestamp(2021,3,28,23,0,0).tz_localize(timezone)
        self.day_before_winter_summer_timechange_start = pd.Timestamp(2021,3,27,0,0,0).tz_localize(timezone)
        self.day_before_winter_summer_timechange_end  = pd.Timestamp(2021,3,27,23,0,0).tz_localize(timezone)

        self.normalday_start = pd.Timestamp(2021,1,1,0,0,0).tz_localize(timezone)
        self.normalday_end = pd.Timestamp(2021,1,1,23,0,0).tz_localize(timezone)

    def return_all_timestamps(self):
        return self.summer_winter_timechange_start,self.summer_winter_timechange_end,self.day_before_summer_winter_timechange_start,self.day_before_summer_winter_timechange_end,self.winter_summer_timechange_start,self.winter_summer_timechange_end,self.day_before_winter_summer_timechange_start,self.day_before_winter_summer_timechange_end,self.normalday_start,self.normalday_end


