from kafka import KafkaConsumer
import json
import rnn_model
import csv
import numpy as np

topic_name = 'space'
categories = ['soc.religion.christian', 'sci.space', 'sci.electronics', 'talk.religion.misc', 'rec.motorcycles']

# Open/create a file to append data to
csvFile = open('space_tweets_predictions.csv', 'a')

# Use csv writer
csvWriter = csv.writer(csvFile)

consumer = KafkaConsumer(
     topic_name,
     bootstrap_servers=['localhost:9092'],
     group_id =None,
     auto_offset_reset='earliest')

# consumer = KafkaConsumer(
#     topic_name,
#      bootstrap_servers=['localhost:9092'],
#      auto_offset_reset='latest',
#      enable_auto_commit=True,
#      auto_commit_interval_ms =  5000,
#      fetch_max_bytes = 128,
#      max_poll_records = 100,
#      value_deserializer=lambda x: json.loads(x.decode('utf-8')))

rnn_model_for_consumer = rnn_model.get_rnn_model()

for i, message in enumerate(consumer):
    tweet = message.value.decode('utf-8')
    print(f"The tweet is: {message.value}")

    predicted_categories = rnn_model_for_consumer.predict(rnn_model.get_processed_tweet(tweet))
    predicted_category = categories[np.squeeze(np.argmax(predicted_categories, axis = -1))]
    print(f"The predicted category is: {predicted_category}")

    csvWriter.writerow([i, message.value, predicted_category])
    
# consumer = KafkaConsumer(
#      topic_name,
#      bootstrap_servers=['localhost:9092'],
#      group_id =None,
#      auto_offset_reset='earliest')

# for message in consumer:
#     print(message.value)