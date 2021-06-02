import pandas as pd
from flask import Flask, redirect, request, url_for,render_template, Response, jsonify
from application import app
import requests
import hashlib
import json

@app.route('/') 
@app.route('/home') 
def home():
    return render_template('homepage.html')

@app.route('/login', methods=['GET','POST']) 
def login():
    return render_template('login.html')

@app.route('/signup', methods=['GET','POST']) 
def signup():
    keypair = requests.get('http://keypair-generator:5001/keys_generator').json()

    #data = {"hashed_private_key": hashlib.sha256(keypair['private_key'].encode()).hexdigest(), "public_key":keypair['private_key']}
    data = {"private_key": keypair['private_key'], "public_key":keypair['public_key']}
    requests.post('http://credentials:5002/accounts_database', json = data)
    
    return pd.DataFrame.from_dict(keypair,orient='index').to_html()
    #return render_template('signup.html')

@app.route('/account', methods=['GET']) 
def account():
    return render_template('account.html')

@app.route('/mine', methods=['GET','POST']) 
def mine():
    return render_template('mine.html')

@app.route('/transact', methods=['GET','POST']) 
def transact():
    return render_template('transact.html')

@app.route('/addresses', methods=['GET','POST']) 
def addresses():
    return render_template('addresses.html')

@app.route('/credentials', methods=['GET']) 
def credentials():
    db = requests.get('http://credentials:5002/accounts_database')
    try:
        return pd.DataFrame.from_dict(db.json()).to_html() #db.json() #pd.DataFrame.from_dict(db,orient='index').to_html()
    except:
        return "no data"


# @app.route('/gateway', methods=['GET','POST']) 
# def gateway():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         reg_list = requests.get('http://Database:5006/database_router').text
#         df = pd.read_json(reg_list)
#         if len(df.loc[df.username == username]) > 0:
#             if df.loc[df.username == username].password.max() == password:
#                 return df.loc[df.username == username].to_html()
#             else:
#                 return "Oops, that password wasn't correct" 
#         else:
#             return "Oops, there's no user with that username"
    


