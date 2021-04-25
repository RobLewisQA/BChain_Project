import random
import pandas as pd
from flask import Flask, redirect, request, url_for,render_template, Response, jsonify
from application import app

@app.route('/random_sequence', methods=['GET']) 
def random_sequence():
    sequence = random.sample([0,1,2,3,4,5,6,7,8,9,10,11],12)
    series = pd.Series(sequence, name="sp_order").reset_index().drop(columns='index')
    return series.to_json()