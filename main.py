from utils.source import twitter_links  
from utils.appify import twitter_scrapper
import json
from utils.chroma import ChromaDBUtil
import hashlib


def get_tweets():
    """
    Scrape tweet data from provided Twitter/X links using Apify actor.
    
    Args:
        links (list): List of Twitter/X URLs to scrape
        
    Returns:
        list: List of tweet data dictionaries returned by the actor
    """
    
    # urls_with_method = []
    # for url in twitter_links:
    #     urls_with_method.append({
    #         "url": url,
    #         "method": "GET"
    #     })
    # tweet_data = twitter_scrapper(
    #     start_urls=urls_with_method
    # )
   
    # with open("tweet_data.json", "w") as f:
    #     json.dump(tweet_data, f, indent=4)
    # return tweet_data


def embed_tweets():
    db_util = ChromaDBUtil(collection_name="tweet_collection")

    with open("tweet_data.json", "r") as f:
        tweet_data = json.load(f)
    
    processed_ids = set()
    for tweet in tweet_data:
        text = tweet.get("text")
        if text:
            tweet_id = hashlib.sha256(text.encode()).hexdigest()
            if tweet_id not in processed_ids:
                db_util.add_to_collection(id=tweet_id, text=text, metadata={"username": tweet.get("username", "")})
                processed_ids.add(tweet_id)
        
        if tweet.get("replyToTweet"):
            reply_text = tweet.get("replyToTweet").get("text")
            if reply_text:
                reply_id = hashlib.sha256(reply_text.encode()).hexdigest()
                if reply_id not in processed_ids:
                    db_util.add_to_collection(id=reply_id, text=reply_text, metadata={"username": tweet.get("replyToTweet", {}).get("username", "")})
                    processed_ids.add(reply_id)

def get_enhanced_prompt(query_text, top_k=5):
    """
    Query the ChromaDB collection for tweets similar to the input text.
    
    Args:
        query_text (str): Text to find similar tweets for
        top_k (int): Number of similar tweets to return (default 10)
        
    Returns:
        dict: Dictionary containing matched tweets with their IDs, text content, metadata and distances
    """
    db_util = ChromaDBUtil(collection_name="tweet_collection")
    results = db_util.query_similar(query_text=query_text, top_k=top_k)
    prompt = f"""
You are given user query: {query_text}

Below are some relevant thoughts and perspectives that may help answer this query. Here are the most similar responses from other people, ordered by relevance:
"""
    for i, result in enumerate(results[0], 1):
        prompt += f"{i}. {result}\n"
        
    prompt += """
Based on these responses, please:
1. Focus ONLY on the information provided in the above responses - do not add external knowledge
2. Identify the key themes and insights that appear in multiple responses
3. Structure your response to directly address the user's original query"
4. When quoting specific responses, use code formatting like this: `relevant quote here`
5. Synthesize the insights while maintaining accuracy to the source material
6. If none of the responses seem relevant to the query, skip quoting them and provide a direct response using your general knowledge

"""
    return prompt