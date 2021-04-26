# #####################################################
# Created by: Angeline Tan
# Created on: 9 June 2020
# Description: Context manager for the MariaDB cursor object
# #####################################################

import mariadb

class MariaDBCursor:

    def __init__(self, password, database, user="root", host="localhost", port=3306):
        # Instantiate Connection
        try:
            self.connection = mariadb.connect(
                    user=user,
                    password=password,
                    host=host,
                    port=port,
                    database=database
            )
            
            self.cursor = None
            self.connected = True
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            self.connected = False
        
        if self.connected:
            self.cursor = self.connection.cursor()
            
    def __enter__(self):
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.connected:
            self.cursor.close()
        
        if isinstance(exc_val, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
                
        self.connection.close()
