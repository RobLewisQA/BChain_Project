import random
import application.words as words
import pandas as pd
from flask import Flask, redirect, request, url_for,render_template, Response, jsonify
from application import app
import hashlib

@app.route('/keys_generator', methods=['GET']) 
def keys_generator():
    wordlib = words.wordlib
    wordstr = ""
    wordlist = []

    while len(wordlist) < 12:
        word = wordlib[random.randint(0,len(wordlib)-1)]
        wordstr = wordstr + word + "_"
        wordlist = wordlist + [word]
        wordlib.remove(word)

    mnemonic = wordstr
    private_key = hashlib.sha256(mnemonic.encode()).hexdigest()
    public_key = hashlib.sha256(private_key.encode()).hexdigest()
    return pd.DataFrame([private_key,public_key,mnemonic],index=['private_key','public_key','mnemonic']).to_json()