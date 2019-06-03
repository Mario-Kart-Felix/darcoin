#-*- coding: utf-8 -*-
import hashlib
import json
from datetime import datetime


class Block():

    def __init__(self, timestampt, transactions_list, prev_hash=''):
        self.nonce = 0
        self.timestampt = timestampt
        self.transactions_list = transactions_list
        self.prev_hash = prev_hash
        self.hash = self.calc_hash()

    def calc_hash(self):
        block_string = json.dumps({'nonce': self.nonce, 'timestampt': str(self.timestampt), 'transactions_list': self.transactions_list[0].amount, 'prev_hash': self.prev_hash}, sort_keys=True).encode('utf-8')
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != ''.zfill(difficulty):
            self.nonce += 1
            self.hash = self.calc_hash()
        print('Блок найден:', self.hash)

    def __str__(self):
        string = 'nonce: ' + str(self.nonce) + ', \n'
        string += 'timestampt: ' + str(self.timestampt) + ', \n'
        string += 'transactions_list: ' + str(self.transactions_list) + ', \n'
        string += 'prev_hash: ' + str(self.prev_hash) + ', \n'
        string += 'hash: ' + str(self.hash) + ', \n'
        return string



class BlockChain():

    def __init__(self):
        self.chain = [self.generate_genesis_block(),]
        self.pending_transactions = []
        self.mining_reward = 100
        self.difficulty = 4

    def generate_genesis_block(self):
        return Block('01/06/2019', [Transaction(None, None, 0),])

    def get_last_block(self):
        return self.chain[-1]

    def mine_pending_transaction(self, mining_reward_adress):
        block = Block(datetime.now(), self.pending_transactions)
        block.mine_block(self.difficulty)
        print('Блок найден вы получите вознаграждение в размере:', self.mining_reward)
        self.chain.append(block)
        self.pending_transactions = [Transaction(None, mining_reward_adress, self.mining_reward)]

    def create_transaction(self, Transaction):
        self.pending_transactions.append(Transaction)

    def get_balance(self, adress):
        balance = 0
        for b in self.chain:
            for t in b.transactions_list:
                if t.to_adress == adress:
                    balance += t.amount
                if t.from_adress == adress:
                    balance -= t.amount
        return balance

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            prev_block = self.chain[i-1]
            curr_block = self.chain[i]
            if curr_block.hash != curr_block.calc_hash():
                print('Не правильный блок', curr_block.prev_hash)
                return False
            if curr_block.prev_hash != prev_block.hash:
                print('Не правильная цепочка')
                return False
        return True


class Transaction():
    def __init__(self, from_adress, to_adress, amount):
        self.from_adress = from_adress
        self.to_adress = to_adress
        self.amount = amount




if __name__ == "__main__":
    DARCoin = BlockChain()
    DARCoin.create_transaction(Transaction('adress_1', 'adress_2', 500))
    DARCoin.create_transaction(Transaction('adress_2', 'adress_1', 15))
