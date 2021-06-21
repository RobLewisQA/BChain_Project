import pandas as pd
from flask import Flask, redirect, request, url_for,render_template, Response, jsonify, Blueprint, session, g
from application import app
import requests
import hashlib
import json


class Users:
    def __init__(self, alias, private_key, public_key):
        self.alias = alias
        self.private_key = private_key
        self.public_key = public_key

# main = Blueprint('main', __name__)
# auth = Blueprint('auth', __name__)



@app.route('/') 
@app.route('/home') 
def home():
    return render_template('homepage.html')+('<br><br> <a href="/signup_home" type="button">Create an account</a> </br>')

@app.before_request
def before_request():
    if 'alias' in session:
        accounts = requests.get('http://credentials:5002/accounts_database').json()
        accounts_df = pd.DataFrame.from_dict(creds,orient='index').T
        user = [x for x in accounts_df[-1] if x == session['alias']][0]
        g.user = user

@app.route('/login', methods=['GET','POST']) 
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    elif request.method == 'POST':
        session.pop('alias', None)
        creds = requests.get('http://credentials:5002/accounts_database').json()
        if creds == {}:
            
        current_data = pd.DataFrame.from_dict(creds,orient='index').T
        #data = {"private_key": keypair['private_key'], "public_key":keypair['public_key'],"alias":request.form['alias']}

        privkey = hashlib.sha256((request.form['mnemonic']).encode()).hexdigest()

        try:
            if request.form['alias'] in current_data.alias.to_list():
                if hashlib.sha256((request.form['mnemonic']).encode()).hexdigest() == current_data.loc[current_data.alias == request.form['alias']].private_key.max():
                    session['alias'] = request.form['alias']
                    return redirect(url_for('account'))
                else:
                    return 'incorrect alias/mnemonic pair'
            else:
                return 'alias not known'
        except:
            return "oops, that didn't work!"





    #     if len(current_data) == 0:
    #         # data = {"private_key": keypair['private_key'], "public_key":keypair['public_key'],"alias":request.form['alias']}
    #         requests.post('http://credentials:5002/accounts_database', json = data)
    #         data.update({"mnemonic": keypair['mnemonic']})
    #         return pd.DataFrame.from_dict(data,orient='index').to_html()
    #     else:
    #         if (keypair['public_key'] in current_data.T.public_key.to_list()) | (keypair['private_key'] in current_data.T.private_key.to_list()) | (request.form['alias'] in current_data.T.alias.to_list()):
    #             return 'Sorry, your credentials need to be unique! Try again '+ ('<a href="/signup_home" type="button">here</a> </p>')
    #         else:
    #             # data = {"private_key": keypair['private_key'], "public_key":keypair['public_key'],"alias":request.form['alias']}
    #             requests.post('http://credentials:5002/accounts_database', json = data)
    #             data.update({"mnemonic": keypair['mnemonic']})
    #             return pd.DataFrame.from_dict(data,orient='index').to_html()
    # else:
    #     return

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
#@login_required
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
    


