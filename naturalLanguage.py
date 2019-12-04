import pymongo
import numpy as np 
import pandas as pd 
import re
import nltk 
import matplotlib.pyplot as plt

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["twitter"]
mycol = mydb["junk"]