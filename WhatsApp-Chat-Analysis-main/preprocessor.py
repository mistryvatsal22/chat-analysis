import re
import pandas as pd

def preprocess(data):
    pattern = '(\d{1,2}/\d{1,2}/\d{4}),\s(\d{1,2}:\d{2}\s?[ap]m)\s-\s([^:]+): (.+)'

    dates = re.findall(pattern, data)

    cols=['dates','time','users','messages']
    df=pd.DataFrame(dates,columns=cols)
    
    df['dates']=pd.to_datetime(df['dates'])
    df['only_date'] = df['dates'].dt.date
    df['year'] = df['dates'].dt.year
    df['month_num'] = df['dates'].dt.month
    df['month'] = df['dates'].dt.month_name()
    df['day'] = df['dates'].dt.day
    df['day_name'] = df['dates'].dt.day_name()
    df['hour'] = df['time'].apply(lambda x: pd.to_datetime(x).hour)
    df['minute'] = df['time'].apply(lambda x: pd.to_datetime(x).minute)

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df