import os, hashlib, pickle, time, base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA384
from accounts import Keys
from blockchain import Blockchain
class Transfer():
    def __init__(self, sender, recipient, amount, timestamp, tx_hash, signature, public_key_pem, height, keypair):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.timestamp = timestamp
        self.transaction_hash = tx_hash
        self.signature = signature
        self.public_key_pem = public_key_pem
        self.Keys = keypair
        self.height = height
    def new(self):
        # public_key_pem: export
        self.timestamp = time.time()
        tx = '{sender}{recipient}{amount}{timestamp}{public_key_pem}'.format(sender=self.sender, recipient=self.recipient, amount=self.amount, timestamp=self.timestamp, public_key_pem=self.Keys.public_key_pem())
        _hash = SHA384.new()
        _hash.update(tx.encode('utf-8'))
        self.transaction_hash = str(_hash.hexdigest())
        cypher = PKCS1_v1_5.new(self.Keys.private_key())
        self.signature = cypher.sign(_hash)
        signature_export = base64.b64encode(self.signature).decode('utf-8')
    def finalize(self):
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'timestamp': self.timestamp,
            'amount': self.amount,
            'public_key': self.Keys.public_key_pem(),
            'transaction_hash': self.transaction_hash,
            'signature': self.signature
        }
    def add_to_pool(self):
        is_empty_pool = False
        if not os.path.exists('./txpool/{height}.dat'.format(height=self.height)):
            is_empty_pool = True
            open('./txpool/{height}.dat'.format(height=self.height), 'x')
        # backup if not empty
        pool = []
        if is_empty_pool == False:
            with open('./txpool/{height}.dat'.format(height=self.height), 'rb') as pool_file:
                pool = pickle.load(pool_file)
        # validate first.
        pool.append(self.finalize())
        with open('./txpool/{height}.dat'.format(height=self.height), 'wb') as pool_file:
            pickle.dump(pool, pool_file)
    def validate(self):
        signature = base64.b64decode(self.signature.encode('utf-8'))
        tx = '{sender}{recipient}{amount}{timestamp}{public_key_pem}'.format(sender=self.sender, recipient=self.recipient, amount=self.amount, timestamp=self.timestamp, public_key_pem=self.Keys.public_key_pem())
        _hash = SHA384.new()
        _hash.update(tx.encode('utf-8'))
        cypher = PKCS1_v1_5.new(RSA.importKey(self.public_key_pem))
        # check signature
        return cypher.verify(_hash, signature)

def tests():
    tx = Transfer('sender', 'recipient', 10, None, None, None, None)
    tx.new()
    tx.add_to_pool()
    print(tx.finalize())
#tests()
