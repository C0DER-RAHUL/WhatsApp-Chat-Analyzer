from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user].copy()

    # Fetch the number of messages
    num_messages = df.shape[0]

    # Fetch the total number of words
    words = [word for message in df['message'] for word in message.split()]

    # Fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    # Fetch number of links shared
    links = [url for message in df['message'] for url in extract.find_urls(message)]

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    percent_df = (df['user'].value_counts(normalize=True) * 100).reset_index()
    percent_df.columns = ['name', 'percent']
    return x, percent_df

def create_wordcloud(selected_user, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = set(f.read().split())

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user].copy()

    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>\n')].copy()

    def remove_stop_words(message):
        return " ".join(word for word in message.lower().split() if word not in stop_words)

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    return wc.generate(temp['message'].str.cat(sep=" "))

def most_common_words(selected_user, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = set(f.read().split())

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user].copy()

    temp = df[(df['user'] != 'group_notification') & (df['message'] != '<Media omitted>\n')].copy()

    words = [word for message in temp['message'] for word in message.lower().split() if word not in stop_words]

    return pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Count'])

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user].copy()

    emojis = [c for message in df['message'] for c in message if emoji.is_emoji(c)]

    return pd.DataFrame(Counter(emojis).most_common(), columns=['Emoji', 'Count'])

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user].copy()

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    timeline['time'] = timeline['month'] + "-" + timeline['year'].astype(str)

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user].copy()

    return df.groupby('only_date').count()['message'].reset_index()

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user].copy()

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user].copy()

    return df['month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user].copy()

    return df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)














