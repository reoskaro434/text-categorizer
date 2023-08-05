import datetime
import json
import os
import logging
import time

import praw

CLIENT_ID = os.environ.get('R_ID_KEY')
CLIENT_SECRET = os.environ.get('R_SECRET')
USER_AGENT = os.environ.get('R_USER_AGENT')
REDDIT = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
    ratelimit_seconds=70
)


def __configure_logger(subreddit_name):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime('%Y_%m_%d__%H:%M:%S')

    log_file_name = f"./logs/{subreddit_name}-{formatted_datetime}.log"

    with open(log_file_name, 'a') as f:
        f.write('')

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file_name),
            logging.StreamHandler()
        ]
    )


def __set_up_subreddit(subreddit_name, submission_number):
    subreddit = REDDIT.subreddit(subreddit_name)

    name = subreddit.display_name
    id_ = subreddit.id
    public_description = subreddit.public_description
    created_at = subreddit.created

    logging.info((name, id_, public_description, created_at))
    logging.info(f'Save {submission_number} posts from the {subreddit_name}')

    return subreddit


def save_subreddit_data(subreddit_name, submission_number):
    __configure_logger(subreddit_name)
    subreddit = __set_up_subreddit(subreddit_name, submission_number)
    file_path = f"./reddit_data/{subreddit_name}.json"
    counter = 0

    try:
        with open(file_path, "a") as f:
            f.write('[\n')

        for submission in subreddit.new(limit=submission_number):
            counter += 1

            data = {
                'title': submission.title,
                'link': submission.url,
                'author': submission.author_fullname,
                'score': submission.score,
                'created': submission.created,
            }

            logging.info(f"saving post nr: {counter} from: {subreddit_name}")

            with open(file_path, "a") as f:
                if counter > 1:
                    f.write(',\n')

                json.dump(data, f, indent=2)

            if counter % 100 == 0:  # API rate limits is 100 per 60 seconds
                logging.warning(f'This is a {counter} waiting about 1 minute to continue')
                time.sleep(60)
        with open(file_path, "a") as f:
            f.write('\n]')

    except Exception as ex:
        logging.error(f'Oh no! An error occurred while saving post nr:{counter} from {subreddit_name}')
        logging.error(ex)
