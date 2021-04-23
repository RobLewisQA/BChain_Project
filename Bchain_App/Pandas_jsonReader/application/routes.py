import pandas as pd
import random
from os import getenv
from flask import Flask, redirect, request, url_for,render_template, Response, jsonify
from application import app
import requests

@app.route('/json_parser', methods=['GET']) 
def json_parser():
    df = pd.DataFrame(columns= ['username','password','mnemonic'])
    w_positioner = requests.get('http://Seedphrase_Generator:5000/').text
    usn_pwd = requests.get('http://Username_Generator:5004/').text
    df_words = pd.read_json(w_positioner,orient='columns').sort_values(by='sp_order')
    df_usnpwd = pd.read_json(usn_pwd)
    try:
        user_name = usn_pwd[0] + str(random.randint(1000000000, 9999999999))
    except:
        user_name = str(random.randint(100000000000000, 999999999999999))
    print(len(user_name))
    if (len(df.loc[df.username == user_name])) == 0:
        if (len(user_name) <= 40):
    
            seedphrase = '' 
            for w in df_words.sp_words:
                seedphrase = seedphrase + w + '_'
            df_usnpwd['mnemonic'] = seedphrase
            df = df.append(df_usnpwd,ignore_index=True)
            return df.to_json()
        else:
            return 'Aww shucks! That username was too long. Try another one with fewer characters'
    else:
        return 'Aww shucks! That username is taken. Please try another one!'