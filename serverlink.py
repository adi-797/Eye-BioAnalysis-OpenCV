#INCOMPLETE | NON EXECUTABLE


import pyrebase
import csv

import requests
from bs4 import BeautifulSoup
from textblob import TextBlob
import sys  
import os
from openpyxl import load_workbook
reload(sys)  
sys.setdefaultencoding('utf8')
	
def stream_handler(message):
  
   entry_len = len(message["path"])
   entry = message["path"]
   
   if(message and message['data'] != None):

        .
        .
        .
        # load image and run Image Processing script.
        # Return a string after analysis. With cholesterol level indicated as "NORMAL", "MILD" or "HIGH"

config = {
    "apiKey": "AIzaSyARWqOWgBHqkcPWmjl8TOije-dIHN0rQFo",
    "authDomain": "irisdetection-6a42f.firebaseapp.com",
    "databaseURL": "https://irisdetection-6a42f.firebaseio.com/",
    "storageBucket": "irisdetection-6a42f.appspot.com ",
    }

firebase = pyrebase.initialize_app(config)
db = firebase.database()

st = firebase.storage()

my_stream = db.stream(stream_handler, stream_id="new_posts")
