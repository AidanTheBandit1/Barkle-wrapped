import tweepy
import twitter_credentials
import json

# Create and save images
import generate_image

# Auth credentials
bearer_token = twitter_credentials.bearer_token
consumer_key = twitter_credentials.consumer_key
consumer_secret = twitter_credentials.consumer_secret
access_token = twitter_credentials.access_token
access_token_secret = twitter_credentials.access_token_secret


# Listener class
class streamListener(tweepy.Stream):
    # overwrite on_data method
    def on_data(self, data):

        # convert it into a python object
        clean_data = json.loads(data)

        # id of user who mentioned bot
        # can also do 'name' to get username
        # if 'protected' true, then stop
        # if 'following' false, then stop

        tweet_id = clean_data['id']
        tweet_username = clean_data['user']['screen_name']  # screen_name
        tweet_text = "@" + tweet_username + " Here's your 2021 Twitter Wrapped!"

        # Call twitter api to get user data
        # Store in file and data structures
        # Generate and save images
        print("Received request from " + tweet_username + "!")
        if generate_image.main(tweet_username):

            # Reply to user with their generated images
            respondToTweet(tweet_username, tweet_text, tweet_id)
            return True

    def on_error(self, status):
        print(status)
        return True


# Get authorisation access
def setUpAuth():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth=auth, retry_count=5)
    return api


# Follow stream, listens for mentions
def followStream():
    twitter_stream = streamListener(
        consumer_key, consumer_secret, access_token, access_token_secret)
    twitter_stream.filter(track=['@TweetWrapped make'])


# Reply to the user
def respondToTweet(tweet_username, tweet_text, tweet_id):
    api = setUpAuth()

    # Get images
    filenames = ['img/outputs/highest_metrics/' + tweet_username + '.png',
                 'img/outputs/word_clouds/' + tweet_username + '.png',
                 'img/outputs/highest_metrics/' + tweet_username + '.png',
                 'img/outputs/sentiment_analysis/' + tweet_username + '.png']
    
    # To contain ID of uploaded images
    media_ids = []

    # Upload the 2 images, and get media ids in response
    for filename in filenames:
        response = api.media_upload(filename)
        media_ids.append(response.media_id)

    # Tweet response to user, with images
    api.update_status(status=tweet_text,
                      in_reply_to_status_id=tweet_id,
                      media_ids=media_ids,
                      auto_populate_reply_metadata=True)
    print("Task completed successfully!")


if __name__ == "__main__":
    followStream()
