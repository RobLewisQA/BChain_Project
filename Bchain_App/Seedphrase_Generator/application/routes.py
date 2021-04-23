#import WordList_Reader as words
#import WordList_Parser as positions
import pandas as pd
from flask import Flask, redirect, request, url_for,render_template, Response, jsonify
from application import app
import requests

@app.route('/', methods=['GET','POST']) 
def word_positioner():
    sp = requests.get('http://WordList_Reader:5001/mnemonic_generator').json()
    #indeces = requests.get('http://WordList_Parser:5000/random_sequence').json()

    #df1 = pd.read_json(sp,orient='columns')
    #df2 = pd.read_json(indeces,orient='columns').sort_index()
    #df = pd.merge(df1,df2,how='right',left_index=True, right_index=True).sort_values(by='sp_order')
    return sp #df.to_json()

