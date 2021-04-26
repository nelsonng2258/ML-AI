# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 19:49:23 2021

@author: Priyanka
"""

# =============================================================================
# class pyspark.Broadcast (
#   sc = None,
#   value = None,
#   pickle_registry = None,
#   path = None
# )
# =============================================================================


#accumulator.py
from pyspark import SparkContext

sc = SparkContext("local", "Accumulator app")
accum = sc.accumulator(10)

def countFun(x):
    global accum
    accum+=x

rdd = sc.parallelize([1,2,3,4,5])
rdd.foreach(countFun) # executed on the workers

final = accum.value # driver program
print("Accumulated value is -> %i" % (final))
