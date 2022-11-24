from urlextract import URLExtract
from wordcloud import WordCloud
import advertools as adv
import pandas as pd
import seaborn as sns

extractor=URLExtract()
def fetch_stats(selected_user,df):

    if selected_user !='Overall':
        df=df[df['user']==selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())
    num_words = len(words)
    num_media=df[df['message'] == "<Media omitted>\n"].shape[0]
    urls=[]
    for message in df['message']:
        urls.extend(extractor.find_urls(message))
    num_urls=len(urls)

    return num_messages, num_words,num_media,num_urls

def fetch_busy_user(df):
    most_five=df['user'].value_counts().drop("group_notification")
    df_percent=round(most_five/df.shape[0]*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return most_five,df_percent

def create_wordcloud(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    temp_df = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>\n')]
    words = []
    for i in temp_df['message']:
        words.extend(i.split())

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc=wc.generate(' '.join(words))
    return df_wc

def emojis(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    emojis=adv.extract_emoji(df['message'])['top_emoji'][:10]
    emoji_df=pd.DataFrame(emojis,columns=['emojis','count'])
    return emoji_df





def monthly_timeline(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    user_heatmap=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return user_heatmap