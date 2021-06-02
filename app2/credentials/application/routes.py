import random
#import application.accounts_credentials as db
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
            current_data = pd.DataFrame(columns=['private_key_hashed','public_key'])
        
        request_data = request.json
        hashed_pk = request_data["private_key"]
        pubkey = request_data['public_key']
        new_data = pd.DataFrame([hashed_pk,pubkey]).T
        new_data.columns = current_data.columns
        df = current_data.append(new_data)

        df.to_csv('accounts_credentials.csv',index=False)
        return "" #df.to_json()
    
    elif request.method == 'GET':
        try:
            return pd.read_csv('accounts_credentials.csv').to_json()
        except:
            return "no data"

    # if request.method=='POST':
    #     content = request.json
    #     # public_key = content["public_key"]
    #     # private_key = content['private_key']
    #     # private_key_hashed = private_key = hashlib.sha256(private_key.encode()).hexdigest()
    #     # df = pd.DataFrame(db.credentials_database,columns=['private_key_hashed','public_key'])
    #     # new_entry = [private_key_hashed,public_key]
    #     # db.credentials_database = df.append(new_entry).to_json()
    #     return content #pd.DataFrame([private_key,public_key,mnemonic],index=['private_key','public_key','mnemonic']).to_json()
    # elif request.method == 'GET':
    #     return jsonify(db.credentials_database)