import json
import logging
import os

import praw

CLIENT_ID = os.environ.get('R_ID_KEY')
CLIENT_SECRET = os.environ.get('R_SECRET')
USER_AGENT = os.environ.get('R_USER_AGENT')


class RedditDataCollector:
    def __init__(self, timer, logger=logging):
        self.logger = logger
        self.reddit = praw.Reddit(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            user_agent=USER_AGENT,
            ratelimit_seconds=60
        )
        self.timer = timer
        self.reddit_data_dir = './reddit_data'

    def __wait(self):
        self.timer.start_timer(60)

    def __set_up_subreddit(self, subreddit_name, submission_number, logger):
        if not os.path.exists(self.reddit_data_dir):
            os.makedirs(self.reddit_data_dir)

        subreddit = self.reddit.subreddit(subreddit_name)

        name = subreddit.display_name
        id_ = subreddit.id
        public_description = subreddit.public_description
        created_at = subreddit.created

        logger.info((name, id_, public_description, created_at))
        logger.info(f'Save {submission_number} posts from the {subreddit_name}')

        return subreddit

    def save_subreddit_data(self, subreddit_name, submission_number):
        self.logger.info(f'Initializing operation for {subreddit_name}...')

        subreddit = self.__set_up_subreddit(subreddit_name, submission_number, self.logger)
        file_path = f"{self.reddit_data_dir}/{subreddit_name}.json"

        self.__wait()  # Ensure that rate limit will not be exceeded

        counter = 0

        try:
            with open(file_path, "a") as f:
                f.write('[\n')

            for submission in subreddit.new(limit=submission_number):
                counter += 1
                try:
                    data = {
                        'title': submission.title,
                        'link': submission.url,
                        'author': submission.author_fullname,
                        'score': submission.score,
                        'created': submission.created,
                    }

                    self.logger.info(f"saving post nr: {counter} from: {subreddit_name}")

                    with open(file_path, "a") as f:
                        if counter > 1:
                            f.write(',\n')

                        json.dump(data, f, indent=2)
                except Exception as ex:
                    self.logger.error(f'Oh no! An error occurred while extracting data nr:{counter}')
                    self.logger.error(submission)
                    self.logger.error(ex)

                if counter % 100 == 0:  # API rate limits is 100 per 60 seconds
                    self.logger.warning(f'This is a {counter} post. Waiting 1 minute to continue')
                    self.__wait()
            with open(file_path, "a") as f:
                f.write('\n]')

        except Exception as ex:
            self.logger.error(f'Oh no! An error occurred while saving post nr:{counter} from {subreddit_name}')
            self.logger.error(ex)
