import tweepy
from config.settings import settings

class TwitterScraperClient:
    def __init__(self):
        """Initializes secure authentication with the X API v2 using Tweepy client."""
        self.client = tweepy.Client(
            bearer_token=settings.X_BEARER_TOKEN,
            consumer_key=settings.X_API_KEY,
            consumer_secret=settings.X_API_SECRET,
            access_token=settings.X_ACCESS_TOKEN,
            access_token_secret=settings.X_ACCESS_TOKEN_SECRET
        )

    def fetch_top_niche_posts(self, query: str, max_results: int = 5) -> list:
        """
        Scrapes high-performing tweets based on an algorithmic query filter.
        Example query: 'solopreneurship min_retweets:50'
        """
        try:
            # Search recent tweets matching our growth query filter
            response = self.client.search_recent_tweets(
                query=f"{query} -is:retweet lang:en",
                tweet_fields=["public_metrics", "created_at"],
                max_results=max_results
            )
            
            if not response.data:
                return []

            viral_posts = []
            for tweet in response.data:
                metrics = tweet.public_metrics
                # Score them purely based on engagement metrics
                engagement_score = metrics.get("retweet_count", 0) + metrics.get("like_count", 0)
                
                viral_posts.append({
                    "text": tweet.text,
                    "engagement_score": engagement_score
                })
                
            # Sort highest performing posts to the top
            viral_posts.sort(key=lambda x: x["engagement_score"], reverse=True)
            return [post["text"] for post in viral_posts]

        except Exception as e:
            print(f"⚠️ X API Retrieval Warning: {e}")
            # Fallback mock container to allow local execution if API keys are inactive
            return [
                "Most builders spend 50 hours on 'fake work'. Here is the 3-step engine to automate distribution.",
                "The modern stack isn't about code. It is about raw execution velocity and systemic leverage loops."
            ]