import pandas as pd 
import json
from datetime import datetime
import praw
import os

class RedditAPI:
    def __init__(self, sub = "python", credentials_path='./credentials/keys.json', limit=10):
        self.sub = sub
        self.credentials_path = credentials_path
        self.limit = limit
        self.reddit = self.auth()

    def auth(self):
        # Get Credentials
        with open(self.credentials_path) as f:
            credentials = json.load(f)

        # Reddit keys
        CLIENT_ID = credentials.get("reddit").get('USER_KEY')
        SECRET_KEY = credentials.get("reddit").get('SECRET_KEY')
        PSW = credentials.get("reddit").get('PSW')
        USERNAME = credentials.get("reddit").get('USERNAME')

        # Reddit Auth
        reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=SECRET_KEY,
            user_agent=f"my-app by u/{USERNAME}",
            username=USERNAME,
            password=PSW,
        )

        return reddit

    def get_hot_posts(self, sub="python"):
        subreddit = self.reddit.subreddit(sub)
        top_posts = subreddit.top(limit=self.limit)
        return self.refine_posts(top_posts)

    def get_new_posts(self, sub="python"):
        subreddit = self.reddit.subreddit(sub)
        new_posts = subreddit.new(limit=self.limit)
        return self.refine_posts(new_posts)

    def refine_posts(self, posts):
        post_list = []

        # Transform Data
        for post in posts:
            refined_post = {
                "Title": post.title,
                "ID": post.id,
                "Author": str(post.author),
                "URL": post.url,
                "Score": post.score,
                "Comment Count": post.num_comments,
                "Created": datetime.fromtimestamp(post.created_utc),
                "Content": post.selftext
            }
            
            post_list.append(refined_post)
                                
        df = pd.DataFrame(post_list)
        df['Subreddit'] = f"r/{self.sub}"
        return df
    
    def get_stream(self, sub="python"):
        subreddit = self.reddit.subreddit(sub)
        for submission in subreddit.stream.submissions():
            print(submission.title)
            print(submission.id)

class RunRedditETL:
    def __init__(self, sub="python", credentials_path='.credentials/keys.json', limit=10, output_folder='./output', post_type='hot'):
        self.sub = sub
        self.credentials_path = credentials_path
        self.output_folder = output_folder
        self.limit = limit
        self.post_type = post_type

    def extract(self):
        reddit_api = RedditAPI(credentials_path = self.credentials_path, limit = self.limit)
        if self.post_type == 'hot':
            return reddit_api.get_hot_posts(self.sub)
        elif self.post_type == 'new':
            return reddit_api.get_new_posts(self.sub)
        else:
            raise ValueError('Invalid post type. Choose between hot or new.')

    def transform(self, df):
        df = df.astype({
            'Title': 'string',
            'ID': 'string',
            'Author': 'string',
            'URL': 'string'
        })
        return df

    def load(self, df):
        df.to_csv(os.path.join(self.output_folder, f"refined_reddit_{self.post_type}_posts_{self.sub}.csv"))

    def start(self):
        df = self.extract()
        df = self.transform(df)
        self.load(df)
        return df
