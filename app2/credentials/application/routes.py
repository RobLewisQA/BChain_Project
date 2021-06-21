import random
import pandas as pd
from flask import Flask, redirect, request, url_for,render_template, Response, jsonify
from application import app
import hashlib
import requests

@app.route('/accounts_database', methods=['GET','POST']) 
def database():
    if request.method == 'POST':
        try:
            current_data = pd.read_csv('accounts_credentials.csv')
        except:
            current_data = pd.DataFrame(columns=['private_key','public_key','alias'])
        
        request_data = request.json
        privkey = request_data["private_key"]
        pubkey = request_data['public_key']
        alias = request_data['alias']

        # if pubkey in current_data.public_key.to_list() | privkey in current_data.private_key.to_list() | alias in current_data.alias.to_list():
        #     return redirect(url_for('database'))
        # else:
        new_data = pd.DataFrame([privkey,pubkey,alias]).T
        new_data.columns = current_data.columns
        df = current_data.append(new_data)

        df.to_csv('accounts_credentials.csv',index=False)
        return ""
    
    elif request.method == 'GET':
        try:
            return pd.read_csv('accounts_credentials.csv').to_json()
        except:
            return pd.DataFrame(columns=['private_key','public_key','alias']).to_json()
