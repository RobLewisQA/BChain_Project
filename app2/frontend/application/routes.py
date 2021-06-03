import pandas as pd
from flask import Flask, redirect, request, url_for,render_template, Response, jsonify
from application import app
import requests
import hashlib
import json

@app.route('/') 
@app.route('/home') 
def home():
    return render_template('homepage.html')+('<br><br> <a href="/signup_home" type="button">Create an account</a> </br>')


@app.route('/login', methods=['GET','POST']) 
def login():
    return render_template('login.html')


@app.route('/signup_home', methods=['GET','POST']) 
def signup_home():
    return '<h1>Create a new BChain account</h1><br>'+ render_template('signup.html')#,title='add_item')#+('<br><br> <a href="/products" type="button">Return to Products home</a> </br>')


@app.route('/signup', methods=['GET','POST']) 
def signup():
    if request.method == 'POST':

        keypair = requests.get('http://keypair-generator:5001/keys_generator').json()
        creds = requests.get('http://credentials:5002/accounts_database').json()
        current_data = pd.DataFrame.from_dict(creds,orient='index')
        data = {"private_key": keypair['private_key'], "public_key":keypair['public_key'],"alias":request.form['alias']}
        
        if len(current_data) == 0:
            # data = {"private_key": keypair['private_key'], "public_key":keypair['public_key'],"alias":request.form['alias']}
            requests.post('http://credentials:5002/accounts_database', json = data)
            data.update({"mnemonic": keypair['mnemonic']})
            return pd.DataFrame.from_dict(data,orient='index').to_html()
        else:
            if (keypair['public_key'] in current_data.T.public_key.to_list()) | (keypair['private_key'] in current_data.T.private_key.to_list()) | (request.form['alias'] in current_data.T.alias.to_list()):
                return 'Sorry, your credentials need to be unique! Try again '+ ('<a href="/signup_home" type="button">here</a> </p>')
            else:
                # data = {"private_key": keypair['private_key'], "public_key":keypair['public_key'],"alias":request.form['alias']}
                requests.post('http://credentials:5002/accounts_database', json = data)
                data.update({"mnemonic": keypair['mnemonic']})
                return pd.DataFrame.from_dict(data,orient='index').to_html()
    else:
        return '<p>Looks like you forgot to add an alias. Try again ' + ('<a href="/signup_home" type="button">here</a> </p>')


@app.route('/account', methods=['GET']) 
def account():
    return render_template('account.html')


@app.route('/mine', methods=['GET']) 
def mine():
    response = requests.get('http://blockchain-engine:5003/mine_block')
    return response.text # render_template('mine.html')


@app.route('/view_chain', methods=['GET']) 
def view_chain():
    response = requests.get('http://blockchain-engine:5003/get_chain').json()
    return pd.DataFrame.from_dict(response['chain']).to_html()


@app.route('/status', methods=['GET']) 
def status():
    response = requests.get('http://blockchain-engine:5003/valid')
    return response.text


@app.route('/transact', methods=['GET','POST']) 
def transact():
    return render_template('transact.html')


@app.route('/addresses', methods=['GET']) 
def addresses():
    db = requests.get('http://credentials:5002/accounts_database')
    try:
        return pd.DataFrame.from_dict(db.json())[['alias','public_key']].to_html() #db.json() #pd.DataFrame.from_dict(db,orient='index').to_html()
    except:
        return "no addresses yet!"


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
    


