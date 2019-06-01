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

    def print_hashes(self):
        print('Предыдущий HASH:', self.prev_hash)
        print('HASH:', self.hash)


class BlockChain():

    def __init__(self):
        self.chain = [self.generate_genesis_block(),]

    def generate_genesis_block(self):
        return Block(0, '01/06/2019', 'Genesis Block')

    def get_last_block():
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.prev_hash = self.get_last_block().hash
        new_block.hash = new_block.calc_hash()
        self.chain.append(new_block)







if __name__ == "__main__":
    block = Block(1, '01/06/2019', 100)
    block.print_hashes()
