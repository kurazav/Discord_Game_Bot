import os
from dotenv import load_dotenv
import mysql.connector

# Load the .env file
load_dotenv()

mydb = mysql.connector.connect(
    host=os.getenv("DATABASE_HOST"),
    user=os.getenv("DATABASE_USER"),
    password=os.getenv("DATABASE_PASSWORD"),
    database=os.getenv("DATABASE_NAME")
)

# mydb = mysql.connector.connect(
#     host='localhost',
#     user='***',
#     password='***',
#     database='***'
# )

cursor = mydb.cursor()
cursor.execute("select @@version")
version = cursor.fetchone()

if version:
    print('Running version: ', version)
else:
    print('Not connected.')