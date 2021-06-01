import random
import application.BChain_WordList as bwords
import pandas as pd
from flask import Flask, redirect, request, url_for,render_template, Response, jsonify
from application import app

@app.route('/keys_generator', methods=['GET']) 
def keys_generator():
    wordlib = words.wordlib
    wordstr = ""

    while len(wordlist) < 12:
        word = wordlib[random.randint(0,len(wordlib)-1)]
        wordstr = wordstr + word + "_"
        wordlib.remove(word)

    mnemonic = wordstr
    private_key = hashlib.sha256(mnemonic.encode()).hexdigest()
    public_key = hashlib.sha256(private_key.encode()).hexdigest()
    return pd.DataFrame([private_key,public_key],index=['private_key','public_key']).to_json()