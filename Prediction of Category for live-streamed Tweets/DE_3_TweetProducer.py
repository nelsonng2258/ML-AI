from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaConsumer, KafkaProducer
import json
import csv

ACCESS_TOKEN = '837034976629698563-W74gJOobZEMAlfHDcDNC8ojL4aKHZza'
ACCESS_SECRET = 'fKAWAvSmXYHMEizufpVDoeOriBJB2cuIqVMnVZqbXnwlP'
CONSUMER_KEY = 'r985zZRLvQ2i2ZWDJ3AD1ZFOa'
CONSUMER_SECRET = 'V88sSIEiJSLaYGcJtxwsIZ8puOEiAW1N0jo04cEWF60dQn7PYV'

kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Open/create a file to append data to
csvFile = open('space_tweets.csv', 'a')

# Use csv writer
csvWriter = csv.writer(csvFile)

class StdOutListener(StreamListener):
    # def on_data(self, data):
        # kafka_producer.send("space", data.encode('utf-8')).get(timeout=10)
        # print (data)
        # return True

    def __init__(self):
        super().__init__()
        self.line_counter = 0
    
    def on_error(self, status):
        print (status)

    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data["text"]            
        kafka_producer.send("space", tweet.encode('utf-8'))
        csvWriter.writerow([f"{self.line_counter}", tweet.encode('utf-8')])
        self.line_counter += 1 # Increment line counter
        print(tweet)
        return True


l = StdOutListener()
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
stream = Stream(auth, l)
stream.filter(track=["space"])