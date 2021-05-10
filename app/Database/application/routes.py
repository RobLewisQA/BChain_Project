import random
import pandas as pd
from flask import Flask, redirect, request, url_for,render_template, Response, jsonify
from application import app#, data
import requests
import json

@app.route('/database_router', methods=['GET','POST']) 
def database_router():
    if request.method == 'POST':
        try:
            current_data = pd.read_csv('data.csv')
        except:
            current_data = pd.DataFrame(columns=['username','password','mnemonic'])
        raw = request.data.decode('UTF-8')
        content = str(raw)
        df1 = pd.read_json(raw).T
        df = current_data.append(df1)[['username','password','mnemonic']]
        df.to_csv('data.csv')

        #return str(type(json.dumps(raw)))
        return df.to_json()
    else:
        try:
            return pd.read_csv('data.csv').iloc[:,1:].to_json()
        except:
            return "no data"

        # df1 = pd.read_json(content,orient='columns')
        # try:
        #     df2 = pd.read_csv('./application/usn_pwd.csv')
        #     df = df2.append(df1)
        #     df.to_csv('./application/usn_pwd.csv')
        # except:
        #     df1.to_csv('./application/usn_pwd.csv')

        # return df1.to_html()#series.to_json()