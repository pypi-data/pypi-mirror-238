import pandas as pd

def preprocess(df):
    #TODO: modify so that it works with more days
    df.index =  pd.to_datetime(df.index, utc=True)
    df = df.rename_axis('DateTime')
    df = df.rename(columns={"value":"Price"})
    df['Week'] = df.index.isocalendar().week
    df['Day'] = df.index.day
    df["Hour"] = df.index.hour
    print (f"{df=}")
    # Calculate the daily average price and store it in a new DataFrame
    average_price = df['Price'].mean()

    df['Price_daily_AVG'] = average_price
    
    return df

def add_priceRating(df):
    df['rating'] = df['Price'] - df['Price_daily_AVG']
    df['rating_rank'] = df.groupby(df.index.date)['rating'].rank(ascending=True)-1
    return df

def add_priceRatings(df):
    df['savings'] = df['Price'] - df['Price_daily_AVG']
    df['rating_rank'] = df.groupby(df.index.date)['savings'].rank(ascending=True)-1
    return df

def add_timeslot_savings(df):
    df['savings'] = df['Price'] - df['Price_daily_AVG']
    for timeslot_length in range(1,24):
        df[f"timeslot_{timeslot_length}H"] = df["savings"].rolling(timeslot_length).mean().shift(-timeslot_length+1)
    return df


def reduce_Filesize(df:pd.DataFrame):
    df["Price"] = df["Price"].astype('float16')
    df["Week"] = df["Week"].astype("int8")
    df["Day"] = df["Day"].astype("int8")
    df["Hour"] = df["Hour"].astype("int8")
    df["Price_daily_AVG"] = df["Price_daily_AVG"].astype('float16')
    df["savings"] = df["savings"].astype('float16')
    for timeslot_length in range(1,24):
        df[f"timeslot_{timeslot_length}H"] = df[f"timeslot_{timeslot_length}H"].astype('float16')
    return df

