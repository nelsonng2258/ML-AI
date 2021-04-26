# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 16:00:50 2021

@author: Priyanka
"""

from time import sleep
from json import dumps
from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))
    
    
    
    
for e in range(10):
    data = {'number' : e}
    producer.send('numtest', value=data)
    sleep(5)