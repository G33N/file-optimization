import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

# Load environment variables from .env file
load_dotenv()

class DatabaseRepository:
    def __init__(self):
        self.connection_params = {
            'host': os.getenv('DATABASE_HOST'),
            'port': os.getenv('DATABASE_PORT'),
            'user': os.getenv('DATABASE_USER'),
            'password': os.getenv('DATABASE_PASSWORD'),
            'database': os.getenv('DATABASE_NAME')
        }
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect(**self.connection_params)
            self.cursor = self.connection.cursor()
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")

    def execute_query(self, query, params=None):
        if not self.connection:
            raise Exception("Database connection not established.")
        
        try:
            print(f"Executing query: {query}")
            print(f"With params: {params}")
            
            self.cursor.execute(query, params)
            
            self.connection.commit()

            results = self.cursor.fetchall()
            
            return results
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            self.connection.rollback()
            return None

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
