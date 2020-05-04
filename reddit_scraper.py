import praw


class RedditScraper:

    def __init__(self, config=config):
        self.reddit = praw.Reddit(client_id="PWzL26MwPoKw_g",
                                  client_secret="9hy-8izjQxrJQErjcQ4-RwkDKlU",
                                  password="<REDDIT_PASSWORD>",
                                  user_agent="Gratisv1",
                                  username="<REDDIT_USERNAME>")
        self.reddit.read_only = True

    def get_new_posts_in_sub(self, num_of_posts, sub_name):
        """Get the specified number of new posts from the subreddit"""
        sub = self.reddit.subreddit("GameDeals")
        return sub.new(limit=num_of_posts)
