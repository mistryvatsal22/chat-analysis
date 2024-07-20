import re
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['messages']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['messages'] == '<Media omitted>\n'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['messages']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    x = df['users'].value_counts().head()
    df = round((df['users'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'users': 'percent'})
    return x,df

def create_wordcloud(selected_user,df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['messages'] = temp['messages'].apply(remove_stop_words)
    df_wc = wc.generate(temp['messages'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):

    f = open('D:\python programs\All\.venv\Include\WhatsApp Chat Analysis\stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']

    words = []

    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user, df):

    emoji_pattern = re.compile(u'(\U0001F600-\U0001F64F)|(\U0001F300-\U0001F5FF)|(\U0001F680-\U0001F6FF)|(\U0001F1E0-\U0001F1FF)|(\U00002702-\U000027B0)|(\U000024C2-\U0001F251)|(\U0001F930-\U0001F939)|(\U0001F980-\U0001F9C0)|(\U0001F692-\U0001F697)|(\U0001F699-\U0001F69B)|(\U0001F6EB-\U0001F6EC)|(\U00002694-\U00002697)|(\U00002699-\U0000269B)|(\U0000203C-\U00003299)|(\U000023CF)|(\U000023E9-\U000023F3)|(\U000023F8-\U000023FA)', re.UNICODE)


    emoji_counts = {}
    for index, row in df.iterrows():
        message = row['messages']
        user = row['users']

        emojis = emoji_pattern.findall(message)
        emoji_count = len(emojis)

        # Count emojis for each user
        if emoji_count > 0:
            if user in emoji_counts:
                emoji_counts[user] += emoji_count
            else:
                emoji_counts[user] = emoji_count

    # Convert the emoji_counts dictionary to a DataFrame
        emoji_summary_df = pd.DataFrame(list(emoji_counts.items()), columns=['users', 'emoji'])

    return emoji_summary_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap















