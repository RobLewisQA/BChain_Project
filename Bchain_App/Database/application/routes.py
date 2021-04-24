import random
import application.BChain_WordList as bwords
import pandas as pd
from flask import Flask, redirect, request, url_for,render_template, Response, jsonify
from application import app
import requests

@app.route('/r', methods=['GET','POST']) 
def r():

    return 'hello'#series.to_json()