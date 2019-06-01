import hashlib
import json


class Block():

    def __init__(self, nonce, timestampt, transactions, prev_hash=''):
        self.nonce = nonce
        self.timestampt = timestampt
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.hash = self.calcHash()

    def calcHash(self):
        block_string = json.dumps({'nonce': self.nonce, 'timestampt': self.timestampt, 'transactions': self.transactions, 'prev_hash': self.prev_hash}, sort_keys=True).encode('utf-8')
        return hashlib.sha256(block_string).hexdigest()

    def printHashes(self):
        print('Предыдущий HASH:', self.prev_hash)
        print('HASH:', self.hash)


class BlockChain():

    def __init__(self):
        self.chain = [self.generateGenesisBlock(),]

    def generateGenesisBlock(self):
        return Block(0, '01/06/2019', 'Genesis Block')





if __name__ == "__main__":
    block = Block(1, '01/06/2019', 100)
    block.printHashes()
