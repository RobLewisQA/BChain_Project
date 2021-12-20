from flask import Flask
from os import getenv


app = Flask(__name__)
app.secret_key = 'somesecretkey'

from application import routes