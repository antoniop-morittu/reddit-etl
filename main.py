import argparse
from src.reddit_etl import RunRedditETL, RedditAPI
import os

def main():

    # Argument Parsing
    parser = argparse.ArgumentParser(description='Example argument parsing')
    parser.add_argument('--sub', help='Which subreddit', default='python', required=False)
    parser.add_argument('-o', '--output', help='Output folder', default='output/test', required=False)
    parser.add_argument('-c', '--credentials', help='path to .json that contains credentials', default= './credentials/keys.json', required=False)
    parser.add_argument("-l", "--limit", help='maximum number of post', default=10, type=int)
    parser.add_argument("--post_type", help='Type of posts to fetch: hot or new', choices=['hot', 'new'], default='hot', required=False)
    args = parser.parse_args()

    # Set Output folder and create it if specified
    OUTPUT_FOLDER = args.output

    if args.output:
        OUTPUT_FOLDER = args.output
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Run Twitter ETL process
    reddit_etl = RunRedditETL(args.sub, args.credentials, args.limit, args.output, args.post_type)
    df = reddit_etl.start()
    

if __name__ == "__main__":
    main()
