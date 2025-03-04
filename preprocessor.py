import re
import pandas as pd

def preprocess(data):
    pattern = r'(\d{2}/\d{2}/\d{2},\s+\d{1,2}:\d{2}\s+[ap]m)\s+-\s+(.*)'
    matches = re.findall(pattern, data)

    # Create separate lists using list comprehension
    dates = [match[0] for match in matches]
    messages = [match[1] for match in matches]

    # Alternative using zip
    dates, messages = zip(*matches)  # This creates tuples, convert to list if needed
    dates = list(dates)
    messages = list(messages)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    return df
