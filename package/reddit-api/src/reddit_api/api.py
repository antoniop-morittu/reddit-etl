"""
This class has the objective to use the Reddit API to get data from the platform. Must return a dataframe type or stream the data.
"""
import praw
import json
from datetime import datetime
import pandas as pd
from .debug import *

class RedditApi:
    """
    Reddit API class to get data from the platform.

    Parameters
    ----------
    credentials_path: str
        Path to the credentials file. Credentials file must be stored in a .json.
    """

    def __init__(self, credentials_path):
        self.credentials_path = credentials_path
        self.api = self.get_conn()

    def get_conn(self):
        try:
            with open(self.credentials_path, encoding="utf-8") as f:
                credentials = json.load(f)

            CLIENT_ID = credentials.get("reddit").get("USER_KEY")
            SECRET_KEY = credentials.get("reddit").get("SECRET_KEY")
            PSW = credentials.get("reddit").get("PSW")
            USERNAME = credentials.get("reddit").get("USERNAME")

            reddit = praw.Reddit(
                client_id=CLIENT_ID,
                client_secret=SECRET_KEY,
                user_agent=f"my-app by u/{USERNAME}",
                username=USERNAME,
                password=PSW,
            )

            reddit.auth.scopes()
            
            logging.info("Reddit API client authenticated successfully. Ready to use.")
            return reddit

        except Exception as e:
            logging.error("Authentication failed: %s", e)
            raise e

    # Api Methods

    def get_hot_posts(self, sub, limit):
        """Get the hot posts from a subreddit."""
        api = self.api

        subreddit = api.subreddit(sub)
        top_posts = subreddit.top(limit=limit)
        result_df = transform_methods.refine_posts(top_posts, sub)
        logging.info("Got %s hot posts from r/%s", len(result_df), sub)
        return result_df

    def get_new_posts(self, sub, limit):
        """Get the new posts from a subreddit."""
        api = self.api
      
        subreddit = api.subreddit(sub)
        new_posts = subreddit.new(limit=limit)
        result_df = transform_methods.refine_posts(new_posts, sub)
        logging.info("Got %s new posts from r/%s", len(result_df), sub)
        return result_df

    def get_stream(self, sub):
        """Get stream of posts from a subreddit."""
        api = self.api

        subreddit = api.subreddit(sub)
        for submission in subreddit.stream.submissions():
            print(submission.title)
            print(submission.id)


class transform_methods:
    """
    Class with methods to transform the data from the API.
    """

    @staticmethod
    def refine_posts(posts, sub):
        """Refine the posts from the API to a dataframe."""
        post_list = []

        for post in posts:
            refined_post = {
                "Title": post.title,
                "ID": post.id,
                "Author": str(post.author),
                "URL": post.url,
                "Score": post.score,
                "Comment Count": post.num_comments,
                "Created": datetime.fromtimestamp(post.created_utc),
                "Content": post.selftext.replace("\n", " "),
            }
            post_list.append(refined_post)

        df = pd.DataFrame(post_list)
        df["Subreddit"] = f"r/{sub}"
        return df
