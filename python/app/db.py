import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

def getDB():
  return mysql.connector.connect(
     host=os.getenv("mariaDB"),
     user=os.getenv("root"),
     password=os.getenv("12345"),
     database=os.getenv("statTrack")
  )
