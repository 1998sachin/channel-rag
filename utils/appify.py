import os
from apify_client import ApifyClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
token = os.getenv('APIFY_TOKEN')
       

def twitter_scrapper(start_urls=None, actor_id="VsTreSuczsXhhRIqa"):
    """
    Call an Apify actor and return its output.
    
    Args:
        actor_id (str): ID of the Apify actor to run (defaults to Twitter scraper actor)
        start_urls (list, optional): List of starting URLs for the actor
        
    Returns:
        list: Output data from the actor run
    """
    # Get token from env if not provided
    if token is None:
        raise ValueError("Apify token not provided and APIFY_TOKEN env var not set")

    # Initialize client
    client = ApifyClient(token)
    
    if not start_urls:
        return []
    
    # Prepare the Actor input
    run_input = {
        "startUrls": start_urls,
        "handles": [],
        "userQueries": [],
        "tweetsDesired": 500,
        "profilesDesired": 100,
        "withReplies": True,
        "includeUserInfo": True,
        "proxyConfig": { "useApifyProxy": True },
    }
    
    # Run the Actor and wait for it to finish
    run = client.actor(actor_id).call(run_input=run_input)

    # Fetch and return Actor results from the run's dataset (if there are any)
    output = []
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        output.append(item)
    return output
