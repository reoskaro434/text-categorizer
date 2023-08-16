from resanter_logger.re_logger import ReLogger

from reddit_data_collector import RedditDataCollector

from timer.timer import Timer
from globals import SUBBREDDIT_LIST

for subreddit_name in SUBBREDDIT_LIST:
    reddit_logger = ReLogger(subreddit_name)
    reddit_timer = Timer(reddit_logger)

    RedditDataCollector(reddit_timer, reddit_logger).save_subreddit_data(subreddit_name, 10000)

