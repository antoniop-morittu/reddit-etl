import argparse
from reddit_api import etl, extract_multiple_subreddits
import os

PATH_CREDENTIALS = os.path.join(os.getcwd(), "config/credentials/keys.json")
OUTPUT_PATH = os.path.join(os.getcwd(), "data/local")


def main():
    # Argument Parsing
    parser = argparse.ArgumentParser(description="Example argument parsing")
    parser.add_argument(
        "--sub", nargs='+', help="Which subreddit", default="solana", required=False
    )
    parser.add_argument(
        "--save-path",
        default=OUTPUT_PATH,
        help="Path to save the output file. If not specified, the file will be saved in the output folder.",
    )
    parser.add_argument(
        "-c",
        "--credentials-path",
        help="path to .json that contains credentials",
        default=PATH_CREDENTIALS,
        required=False,
    )
    parser.add_argument(
        "-l",
        "--limit",
        help="maximum number of post",
        default=10,
        type=int,
        required=False,
    )
    parser.add_argument(
        "--post-type",
        choices=["get_hot_posts", "get_new_posts"],
        default="get_new_posts",
        help="Type of post to get from the subreddit.",
        required=False,
    )
    args = parser.parse_args()

    parameters = vars(args)

    # Run Twitter ETL process
    # df = etl(**parameters)
    return extract_multiple_subreddits(**parameters)


if __name__ == "__main__":
    main()
