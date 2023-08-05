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


def save_subreddit_data(subreddit_name, submission_number):
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
    logging.basicConfig(
        level=logging.DEBUG,  # Set the logging level
        filename=f'app_{formatted_datetime}.log',  # Specify the filename for the log file
        filemode='a',  # 'a' means append mode
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    subreddit = REDDIT.subreddit(subreddit_name)

    name = subreddit.display_name
    id_ = subreddit.id
    public_description = subreddit.public_description
    created_at = subreddit.created

    logging.info((name, id_, public_description, created_at))
    logging.info(f'Save {submission_number} posts from the {subreddit_name}')

    counter = 0
    try:
        with open(f"{subreddit_name}.json", "a") as file:
            file.write('[\n')
            for submission in subreddit.new(limit=submission_number):
                counter += 1

                title = submission.title
                link = submission.url
                author = submission.author_fullname
                score = submission.score
                created = submission.created

                data = {
                    'title': title,
                    'link': link,
                    'author': author,
                    'score': score,
                    'created': created,
                }

                logging.info(f"saving post nr: {counter} from: {subreddit_name}")

                if counter > 1:
                    file.write(',\n')

                json.dump(data, file, indent=2)

                if counter % 100 == 0:  # API rate limits is 100 per 60 seconds
                    logging.warning(f'This is a {counter} waiting about 1 minute to continue')
                    time.sleep(60)
            file.write('\n]')

    except Exception as ex:
        logging.error(f'Oh no! An error occurred while saving post nr:{counter} from {subreddit_name}')
        logging.error(ex)
