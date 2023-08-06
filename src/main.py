from reddit_data_collector import RedditDataCollector
from logger.logger import Logger
from timer.timer import Timer

subreddit_list = [
    'health',
    'medicine',
    'science',
    'Arttips',
    'cultureshare',
    'education',
    'business',
    'economy',
    'religion',
    'philosophy',
    'politics',
    'community',
    'Relax',
    'environment',
    'ecology',
    'history',
    'Archaeology',
    'Cooking',
    'literature',
    'musictheory',
    'Astronomy',
    'travel',
    'geography',
    'photography',
    'fashion',
    'FIlm',
    'psychology',
    'GYM',
    'technology',
    'Military',
    'relationships'
]

for subreddit_name in subreddit_list:
    reddit_logger = Logger(subreddit_name)
    reddit_timer = Timer(reddit_logger)

    RedditDataCollector(reddit_timer, reddit_logger).save_subreddit_data(subreddit_name, 4)

