import os
import mysql.connector
import configparser
from sqlalchemy import create_engine

class Config:
    def __init__(self, database,host,user,password):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()

    def commit(self,query):
        self.cursor.execute(query)
        self.connection.commit()

        data = self.cursor.fetchall()
        
        if self.connection:
            self.connection.close()
            self.cursor.close()

        return data

    def commit_values(self,query,values):
        self.cursor.execute(query,values)
        self.connection.commit()

        data = self.cursor.fetchall()
        
        if self.connection:
            self.connection.close()
            self.cursor.close()

        return data

    def commit_many(self, query, values):
        self.cursor.executemany(query,values)
        self.connection.commit()

        data = self.cursor.fetchall()
        
        if self.connection:
            self.connection.close()
            self.cursor.close()

        return data
    
    def fetchall(self, query):
        self.cursor.execute(query)
        self.connection.commit()

        data = self.cursor.fetchall()
        
        if self.connection:
            self.connection.close()
            self.cursor.close()

        return data

    def fetchone(self, query):
        self.cursor.execute(query)
        self.connection.commit()

        data = self.cursor.fetchone()
        
        if self.connection:
            self.connection.close()
            self.cursor.close()

        return data
    
    def fetchmany(self, query):
        self.cursor.execute(query)
        self.connection.commit()

        data = self.cursor.fetchmany()
        
        if self.connection:
            self.connection.close()
            self.cursor.close()

        return data

