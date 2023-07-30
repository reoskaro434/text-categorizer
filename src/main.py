import praw
CLIENT_ID = "[YOUR ID KEY HERE]"
CLIENT_SECRET = "[YOUR SECRET KEY HERE]"
USER_AGENT = "[YOUR USERNAME HERE]"
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT,
)