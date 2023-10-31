import time
from pydantic import validator
from typing import List, Any

from .customBaseModel import CustomBaseModel


class Timeframe(CustomBaseModel):
    start: int
    end: int

    @validator('*')
    def validate_hours(cls, value):
        if not 0 <= value < 24:
            raise ValueError("hours should be in range 0-23")
        return value


class Timeframes(CustomBaseModel):
    timeframes: List[Timeframe] =  [Timeframe(start=0, end=23)]

    # Create a new constructor that accepts the start and end parameters directly
    def __init__(self, **data: Any) -> None:
        # We intercept the "start" and "end" arguments and use them to create a Timeframe
        start = data.pop('start', 0)  # Provide a default value if you want
        end = data.pop('end', 23)  # Provide a default value if you want
        timeframe = Timeframe(start=start, end=end)
        data['timeframes'] = [timeframe]
        super().__init__(**data)

    @property
    def possible_hours(self) -> List[int]:
        hours = set()
        for timeframe in self.timeframes:
            start, end = timeframe.start, timeframe.end
            end += 1
            if start <= end:
                hours.update(range(start, end))
            else:  # the timeframe goes over midnight
                hours.update(range(start, 24))
                hours.update(range(0, end))
        return sorted(list(hours))


    def add_timeframe(self, start: int, end: int):
        self.timeframes.append(Timeframe(start=start, end=end))

    def add_timeframe_array(self, timeframe_array: List[Timeframe]):
        for timeframe in timeframe_array:
            self.add_timeframe(timeframe.start, timeframe.end)

        

    def remove_timeframe(self, start: int, end: int):
        self.timeframes = [timeframe for timeframe in self.timeframes if not (timeframe.start == start and timeframe.end == end)]
    
    def remove_initial_timeframe(self):
        self.timeframes = self.timeframes[1:]

    def set_whole_day(self):
        self.timeframes.append(Timeframe(start=0, end=23))

    def set_morning(self):
        self.timeframes.append(Timeframe(start=5, end=12))

    def set_afternoon(self):
        self.timeframes.append(Timeframe(start=12, end=17))

    def set_evening(self):
        self.timeframes.append(Timeframe(start=17, end=20))

    def set_night(self):
        self.timeframes.append(Timeframe(start=20, end=5))

    def as_String(self):
        timeframe_list = []
        for timeframe in self.timeframes:
            timeframe_list.append(str(timeframe.start) + " - " + str(timeframe.end) + " ")
        timeframe_str = ', '.join(map(str, timeframe_list))
        return timeframe_str

            

def hours_to_timeframes(hours_list: List[int]) -> Timeframes:
    timeframes = Timeframes()
    timeframes.remove_initial_timeframe()

    hours_list = sorted(set(hours_list))  # Ensure hours are unique and sorted

    start = None
    prev_hour = None

    for hour in hours_list:
        if start is None:
            start = hour  # Start of a new timeframe
        elif prev_hour is not None and hour != prev_hour + 1:
            # If there's a gap, we end the current timeframe and start a new one
            timeframes.add_timeframe(start=start, end=prev_hour)
            start = hour
        prev_hour = hour

    if start is not None and prev_hour is not None:
        # Close the last timeframe
        timeframes.add_timeframe(start=start, end=prev_hour)

    
    return timeframes


