import streamlit
from urlextract import URLExtract
import emoji
import pandas as pd
from wordcloud import WordCloud
from collections import Counter
extractor=URLExtract()
def fetch_stats(selected_user,df):
    if selected_user!='overall':
        df=df[df['user']==selected_user]
    num_message=df.shape[0]
    word=[]
    for message in df['message']:
        word.extend(message.split(' '))
    # fetch number of media messages
    num_media_message=df[df['message']=='<Media omitted>'].shape[0]
    # fetch no of links
    links=[]
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    return num_message,len(word),num_media_message,len(links)
def most_buy_users(df):
    x = df['user'].value_counts().head()
    df=round(df['user'].value_counts() / df.shape[0] * 100, 2).reset_index().rename(columns={'count': 'percent'})
    return x,df
def create_wordcloud(selected_user,df):
    if selected_user!='overall' :
        df=df[df['user']==selected_user]
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df=wc.generate(df['message'].str.cat(sep=" "))
    return df
def most_common_words(selected_user,df):
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    if selected_user!='overall' :
        df=df[df['user']==selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']
    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    common_df=pd.DataFrame(Counter(words).most_common(20))
    return common_df
def cnt_emoji(selected_user,df):
    emojilist=[]
    if selected_user!='overall' :
        df=df[df['user']==selected_user]
    for message in df['message']:
        if isinstance(message, str):
            for char in message:
                if char in emoji.EMOJI_DATA:
                    emojilist.extend(char)
    Counter(emojilist)

    new_df2= pd.DataFrame(Counter(emojilist).most_common(len(Counter(emojilist))))
    return new_df2
