import re
import pandas as pd


def preprocess(data):
    pattern = "\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{2}\s\S{2}\s-\s"
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_messages': messages, 'dates': dates})
    df['dates'] = df['dates'].str[:-3]
    df['final_dates'] = pd.to_datetime(df['dates'], format='%m/%d/%y, %H:%M %p')
    df.drop(['dates'], inplace=True, axis=1)


    users = []
    messages = []
    for message in df['user_messages']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(['user_messages'], inplace=True, axis=1)
    df['day_name']=df['final_dates'].dt.day_name()
    df['only_date'] = df['final_dates'].dt.date
    df['year'] = df['final_dates'].dt.year
    df['month_num']=df['final_dates'].dt.month
    df['month'] = df['final_dates'].dt.month_name()
    df['day'] = df['final_dates'].dt.day
    df['hour'] = df['final_dates'].dt.hour
    df['minute'] = df['final_dates'].dt.minute

    period=[]
    for hour in df[['day_name','hour']]['hour']:
        if hour==23:
            period.append(str(hour)+"-"+str('00'))
        elif hour==0:
            period.append(str('00')+"-"+str(hour+1))
        else:
            period.append(str(hour)+'-'+str(hour+1))
    df['period']=period

    return df