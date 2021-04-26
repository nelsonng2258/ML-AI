# #####################################################
# Created by: Angeline Tan
# Created on: 10 June 2020
# Description: Context manager for the MongoDB cursor object
# #####################################################

from pymongo import MongoClient

class MongoDBClient(object):
    
    def __init__(self, host='localhost', port=27017):
        # MongoDB client
        try:
            self.client = None
            self.client = MongoClient(host, port)
            self.connected = True
        except:
            print("Error connecting to MongoDB Platform")
            self.connected = False
            
    def __enter__(self):
        return self.client
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connected:
            self.client.close()