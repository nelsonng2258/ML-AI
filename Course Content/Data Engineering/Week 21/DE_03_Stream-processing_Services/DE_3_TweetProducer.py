from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaConsumer, KafkaProducer

ACCESS_TOKEN = '837034976629698563-W74gJOobZEMAlfHDcDNC8ojL4aKHZza'
ACCESS_SECRET = 'fKAWAvSmXYHMEizufpVDoeOriBJB2cuIqVMnVZqbXnwlP'
CONSUMER_KEY = 'r985zZRLvQ2i2ZWDJ3AD1ZFOa'
CONSUMER_SECRET = 'V88sSIEiJSLaYGcJtxwsIZ8puOEiAW1N0jo04cEWF60dQn7PYV'

kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092')

class StdOutListener(StreamListener):
    # def on_data(self, data):
        # kafka_producer.send("trump", data.encode('utf-8')).get(timeout=10)
        # print (data)
        # return True
    
    def on_error(self, status):
        print (status)


    def on_data(self, data):
            all_data = json.loads(data)
            tweet = all_data["text"]            
            producer.send("trump", tweet.encode('utf-8'))
            print(tweet)
            return True


l = StdOutListener()
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
stream = Stream(auth, l)
stream.filter(track=["trump"])