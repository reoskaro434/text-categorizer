import praw
import os

CLIENT_ID = os.environ.get('R_ID_KEY')
CLIENT_SECRET = os.environ.get('R_SECRET')
USER_AGENT = os.environ.get('R_USER_AGENT')

reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
    ratelimit_seconds=70
)

subreddit = reddit.subreddit('health')

name = subreddit.display_name
id_ = subreddit.id
public_description = subreddit.public_description
created_at = subreddit.created

print((name, id_, public_description, created_at))

for submission in subreddit.hot(limit=12):
    title = submission.title
    link = submission.url
    author = submission.author_fullname
    score = submission.score
    created = submission.created
    print((title, link, author, score, created))

print('done!')
