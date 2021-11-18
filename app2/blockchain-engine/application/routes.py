#import pandas as pd
from application import app
import requests
import datetime  
import hashlib  
import json 
from flask import Flask, jsonify 

###################
##    GfG code   ##
###################

# add header attribute
# change nonce to nonce
# add data attribute to add transactions to a block
# change mining function

class Blockchain:
	
	# This function is created to create the very first block and set it's hash to "0"
	def __init__(self):
		self.chain = []
		self.create_block(nonce=1, previous_hash='0')

	# This function is created to add further blocks into the chain
	def create_block(self, nonce, previous_hash):
		block = {'index': len(self.chain) + 1,
				'timestamp': str(datetime.datetime.now()),
				'nonce': nonce,
				'previous_hash': previous_hash}
		self.chain.append(block)
		return block
		
	# This function is created to display the previous block
	def print_previous_block(self):
		return self.chain[-1]
		
	# This is the function for nonce of work and used to successfully mine the block
	def proof_of_work(self, previous_nonce):
		new_nonce = 1
		check_nonce = False

		while check_nonce is False:
			hash_operation = hashlib.sha256(
				(self.hash(self.chain[-1]) +str(new_nonce)).encode()).hexdigest()
			if hash_operation[0] == '0':
				check_nonce = True
			else:
				new_nonce += 1
		return new_nonce

	def hash(self, block):
		encoded_block = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(encoded_block).hexdigest()

	def chain_valid(self, chain):
		previous_block = chain[0]
		block_index = 1
		
		while block_index < len(chain):
			block = chain[block_index]
			if block['previous_hash'] != self.hash(previous_block):
				return False
				
			previous_nonce = previous_block['nonce']
			nonce = block['nonce']
			hash_operation = hashlib.sha256(
				(self.hash(self.chain[-1]) +str(new_nonce)).encode()).hexdigest()
			
			if hash_operation[0] != '0':
				return False
			previous_block = block
			block_index += 1
		
		return True


# Create the object of the class blockchain
blockchain = Blockchain()

# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
	previous_block = blockchain.print_previous_block()
	previous_nonce = previous_block['nonce']
	nonce = blockchain.proof_of_work(previous_nonce)
	previous_hash = blockchain.hash(previous_block)
	block = blockchain.create_block(nonce, previous_hash)
	
	response = {'message': 'A block is MINED',
				'index': block['index'],
				'timestamp': block['timestamp'],
				'nonce': block['nonce'],
				'previous_hash': block['previous_hash']}
	
	return jsonify(response), 200

# Display blockchain in json format
@app.route('/get_chain', methods=['GET'])
def display_chain():
	response = {'chain': blockchain.chain,
				'length': len(blockchain.chain)}
	return jsonify(response), 200

# Check validity of blockchain
@app.route('/valid', methods=['GET'])
def valid():
	valid = blockchain.chain_valid(blockchain.chain)
	
	if valid:
		response = {'message': 'The Blockchain is valid.'}
	else:
		response = {'message': 'The Blockchain is not valid.'}
	return jsonify(response), 200

