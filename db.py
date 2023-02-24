import os
from os.path import join, dirname
from dotenv import load_dotenv, find_dotenv
import mysql.connector

# Load the .env file

load_dotenv()

mydb = mysql.connector.connect(host=os.getenv("DATABASE_HOST"),user=os.getenv("DATABASE_USER"),password=os.getenv("DATABASE_PASSWORD"),database=os.getenv("DATABASE_NAME"))

cursor = mydb.cursor()
cursor.execute("select @@version")
version = cursor.fetchone()

if version:
    print('Running version: ', version)
else:
    print('Not connected.')