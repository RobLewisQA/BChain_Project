import pandas as pd
import random
from flask import Flask, redirect, request, url_for,render_template, Response, jsonify
from application import app
import requests

@app.route('/usn_pwd', methods=['GET']) 
def usn_pwd():
    user_name = str(random.randint(1000000000, 9999999999))
    get_data = requests.get('http://Password_Generator:5003/password_engine').text

    password = pd.read_json(get_data).iloc[:,0][0]
    df = pd.DataFrame.from_dict({'username':user_name,'password': password},orient='index').T
    return df.to_json()