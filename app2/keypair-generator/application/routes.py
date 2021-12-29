import random
import application.words as words
#import pandas as pd
from flask import Flask, redirect, request, url_for,render_template, Response, jsonify
from application import app
import hashlib
import json
import requests

def seedphrase_hash(seedphrase,username):
    hash_val = hashlib.sha256(str(seedphrase).encode()).hexdigest()
    for n in range(10):
        if n != 4:
            if n > 1:
                hash_val = hashlib.sha256(str(hash_val).encode()).hexdigest()
            else: 
                hash_val = hashlib.sha256(str(hash_val).encode()).hexdigest()
                username_hash = hashlib.sha256(str(username).encode()).hexdigest()
        else:
            hash_val = hashlib.sha256(str(hash_val).encode()).hexdigest()
            password_val = hash_val
    return '!0!0!' + hash_val + username_hash[5], password_val


def password_hash(password,username):
    hashing_val = hashlib.sha256(str(password).encode()).hexdigest()
    for n in range(4):
        if n > 1:
            hashing_val = hashlib.sha256(str(hashing_val).encode()).hexdigest()
        else: 
            hashing_val = hashlib.sha256(str(hashing_val).encode()).hexdigest()
            username_hashing = hashlib.sha256(str(username).encode()).hexdigest()
    return '!0!0!' + hashing_val + username_hashing[5]




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
    
    return json.dumps({'private_key': private_key, 'public_key': public_key, 'mnemonic': mnemonic})


@app.route('/keys_handler', methods=['GET']) 
def keys_handler():
    if request.method == 'GET':
        keypair = requests.get('http://keypair-generator:5001/keys_generator').json()
        raw_privateKey = keypair['private_key']
        raw_publicKey = keypair['public_key']
        seedphrase = keypair['mnemonic']
        alias = request.args.get('alias')

        privateKey = seedphrase_hash(seedphrase,alias)[1]
        publicKey = password_hash(privateKey,alias)

        keys = json.dumps({"private_key":privateKey, "public_key":publicKey, "alias":alias, "seedphrase":seedphrase})
        stored_creds = {"private_key":privateKey, "public_key":publicKey, "alias":alias}

        requests.post('http://credentials:5002/accounts_database', json = stored_creds)
        return keys


