from core.transfer import Transfer
from core.blockchain import Block, Blockchain
from core.accounts import Keys
import time, os
from chainspec import BLOCKTIME

''' #Genesis Block Creation
Instance = Blockchain()
Instance.new()
genesis_Block = Block(None, None, None, None, None, None, [])
genesis_Block.new(None)
Instance.add_finalized_block(genesis_Block.finalize())
'''


'''
if not os.path.exists('./txpool'):
    os.mkdir('./txpool')
# 1. initialize a new, empty Blockchain instance
Instance = Blockchain()
Instance.new()
# 2. Key instance
_Keys = Keys()
# 3. Genesis Block
timestamp = time.time()
genesis_Block = Block(None, None, None, None, None, None, [])
genesis_Block.new(None)
Instance.add_finalized_block(genesis_Block.finalize())

'''
# TBD: remove this function from api.py and move it in a helper file.
def tx_chain_info():
    b = Blockchain()
    b.update()
    print(b.chain)
    h = b.chain[-1]
    l = len(b.chain)
    return (h, l)
# Conditions that have to be met:
# * time.time > last_block_time
# * effective_height = current_height + n, n!=0
# 4. Send a Transaction that is to be included in Block #1
_Keys = Keys()
info = tx_chain_info()
print(info)
print(info[0]['timestamp'])
print(info[0]['next_timestamp'])
print(info[1])

if not time.time() < int(info[0]['next_timestamp']) and not time.time() > int(info[0]['timestamp']):
    print("[Warning]: wait for chain to sync or block to be created.")

else:


    tx = Transfer('sender', 'recipient', 10, None, None, None, None, 1, _Keys)
    tx.new()
    effective_height = info[1] + 5
    tx.add_to_pool(effective_height)
    print("transaction added to pool.")

'''

# 5. Create and validate Block #1 that should hold the transfer
prev_Block_Dict = Instance.chain[0] # Genesis Block
prev_Block = Block(prev_Block_Dict['index'], prev_Block_Dict['timestamp'], prev_Block_Dict['next_timestamp'], prev_Block_Dict['block_hash'], prev_Block_Dict['next_hash'], prev_Block_Dict['prev_hash'], prev_Block_Dict['transfers'])
new_Block = Block(None, None, None, None, None, None, [])
new_Block.new(prev_Block)
# Write Block to Chain and delete temp file from txpool
Instance.add_finalized_block(new_Block.finalize())
print(Instance.chain)
print("Transaction valid: ", tx.validate())
print("Block valid: ", Instance.validate(new_Block, True))

'''
