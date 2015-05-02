from flask import Flask
from peewee import *

app = Flask(__name__)
app.config.from_object('config')

db = SqliteDatabase('muscade.db')

from app import views, models

