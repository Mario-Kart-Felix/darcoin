#-*- coding: utf-8 -*-
import hashlib
import json
from datetime import datetime
from flask import Flask
from flask import jsonify
import time


class Block():

    def __init__(self, nonce, timestampt, transactions_list, prev_hash='', hash=''):
        self.nonce = 0
        self.timestampt = timestampt
        self.transactions_list = transactions_list
        self.prev_hash = prev_hash
        self.hash = self.calc_hash()
        if hash == '':
            self.hash = self.calc_hash()
        else:
            self.hash == hash

    def calc_hash(self):
        block_string = json.dumps({'nonce': self.nonce, 'timestampt': str(self.timestampt), 'transactions_list': self.transactions_list, 'prev_hash': self.prev_hash}, sort_keys=True).encode('utf-8')
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != ''.zfill(difficulty):
            self.nonce += 1
            self.hash = self.calc_hash()
        print('Блок найден:', self.hash)

    def to_dict(self):
        return {'nonce': self.nonce, 'timestampt': str(self.timestampt), 'transactions_list': self.transactions_list, 'prev_hash': self.prev_hash, 'hash': self.hash}


class BlockChain():

    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.mining_reward = 100
        self.difficulty = 4
        self.generate_genesis_block()

    def generate_genesis_block(self):
        dict_genesis_block = {'nonce': 0, 'timestampt': datetime.now(), 'transactions_list': [{'from_address': None, 'to_address': None, 'amount': 0},], 'hash': ''}
        b = Block(**dict_genesis_block)
        self.chain.append(b.to_dict())
        # return Block('01/06/2019', [Transaction(None, None, 0),])

    def get_last_block(self):
        return Block(**self.chain[-1])

    def mine_pending_transaction(self, mining_reward_address):
        block = Block(0, str(datetime.now()), self.pending_transactions)
        block.prev_hash = self.get_last_block().hash
        block.mine_block(self.difficulty)
        print('Блок найден вы получите вознаграждение в размере:', self.mining_reward)
        self.chain.append(block.to_dict())
        self.pending_transactions = [{'from_address': None, 'to_address': mining_reward_address, 'amount': self.mining_reward},]

    def create_transaction(self, from_address, to_address, amount):
        self.pending_transactions.append({'from_address': from_address, 'to_address': to_address, 'amount': amount})

    def get_balance(self, address):
        balance = 0
        for i in range(len(self.chain)):
            dict_list = self.chain[i]['transactions_list']
            for dic in dict_list:
                if dic['to_address'] == address:
                    balance += dic['amount']
                if dic['from_address'] == dic['amount']:
                    balance -= t.amount
        return balance

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            prev_block = Block(**self.chain[i-1])
            curr_block = Block(**self.chain[i])
            if curr_block.hash != curr_block.calc_hash():
                print('Не правильный блок', curr_block.prev_hash)
                return False
            if curr_block.prev_hash != prev_block.hash:
                print('Не правильная цепочка')
                return False
        return True



if __name__ == "__main__":
    DARCoin = BlockChain()
    DARCoin.create_transaction('adress_1', 'adress_2', 500)
    DARCoin.create_transaction('adress_2', 'adress_1', 15)
    DARCoin.mine_pending_transaction('adress_2')
    print(DARCoin.get_balance('adress_2'))
    print(DARCoin.validate_chain())



app = Flask(__name__)

@app.route('/mine', methods=['GET'])
def mine():
    return 'Мы собираемя майнить новый блок для новой транзакции'


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    return None


@app.route('/chain', methods=['GET'])
def display_full_chain():
   response = {
       'chain': DARCoin.chain,
       'length': len(DARCoin.chain)
   }
   return jsonify(response)


@app.route('/')
def index():
    return 'Вы на главной странице НОДЫ'



if __name__ == "__main__":
    app.run()
