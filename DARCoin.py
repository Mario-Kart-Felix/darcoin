#-*- coding: utf-8 -*-
import hashlib
import json


class Block():

    def __init__(self, nonce, timestampt, transactions, prev_hash=''):
        self.nonce = nonce
        self.timestampt = timestampt
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.hash = self.calc_hash()

    def calc_hash(self):
        block_string = json.dumps({'nonce': self.nonce, 'timestampt': self.timestampt, 'transactions': self.transactions, 'prev_hash': self.prev_hash}, sort_keys=True).encode('utf-8')
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != ''.zfill(difficulty):
            self.nonce += 1
            self.hash = self.calc_hash()
        print('Блок найден:', self.hash)

    def __str__(self):
        string = 'nonce: ' + str(self.nonce) + ', \n'
        string += 'timestampt: ' + str(self.timestampt) + ', \n'
        string += 'transactions: ' + str(self.transactions) + ', \n'
        string += 'prev_hash: ' + str(self.prev_hash) + ', \n'
        string += 'hash: ' + str(self.hash) + ', \n'
        return string



class BlockChain():

    def __init__(self):
        self.chain = [self.generate_genesis_block(),]
        self.difficulty = 6

    def generate_genesis_block(self):
        return Block(0, '01/06/2019', 'Genesis Block')

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.prev_hash = self.get_last_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

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




if __name__ == "__main__":
    DARCoin = BlockChain()
    print('Добавлен первый блок')
    DARCoin.add_block(Block(1, '20/05/2019', 100))

    DARCoin.add_block(Block(2, '25/05/2019', 50))
    print('Добавлен второй блок')
    DARCoin.chain[2].transactions = 777
    DARCoin.chain[2].hash = DARCoin.chain[2].calc_hash()


