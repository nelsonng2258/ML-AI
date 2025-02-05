# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 19:48:21 2021

@author: Priyanka
"""

#broadcast.py
from pyspark import SparkContext

sc = SparkContext("local", "Broadcast app")
words_new = sc.broadcast(["scala", "java", "hadoop", "spark", "akka"])

data = words_new.value
print("Stored data -> %s" % (data))

elem = words_new.value[2]
print("Printing a particular element in RDD -> %s" % (elem))
