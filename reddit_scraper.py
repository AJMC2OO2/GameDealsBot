import praw


class RedditScraper:

    def __init__(self, config=config):
        self.reddit = praw.Reddit(client_id=REDDIT_CLIENT_ID,
                             client_secret=REDDIT_CLIENT_SECRET,
                             password=REDDIT_PASSWORD,
                             user_agent=REDDIT_USER_AGENT,
                             username=REDDIT_USERNAME)
        self.reddit.read_only = True

    def get_new_posts_in_sub(self, num_of_posts, sub_name):
        """Get the specified number of new posts from the subreddit"""
        sub = self.reddit.subreddit(sub_name)
        return sub.new(limit=num_of_posts)
