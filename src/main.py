import requests

# URL for the Reddit API
url = "https://www.reddit.com/subreddits/popular.json"

# Send a GET request to the Reddit API
response = requests.get(
    url,
    headers={"User-agent": "Mozilla/5.0"}
)

# Parse the JSON response
data = response.json()

# Iterate over the subreddits in the response
for subreddit in data["data"]["children"]:
    # Print the name of each subreddit
    print(subreddit["data"]["display_name"])
