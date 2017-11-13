from Crypto.PublicKey import RSA
from Crypto.Hash import SHA512
import requests
import datetime
import Crypto
import json
import threading

f = open('key.pem')
key = RSA.import_key(f.read())
f.close()
publicExponent = key.publickey().n
res = requests.get('https://gw.kaist.ac.kr/broadcast/get?reverse=1&&limit=100')
res = res.json()
nonce = 0
diff = int(json.loads(res[0]['block'])['difficulty'])

block = {'type': 'block', 'transactions': [], 'timestamp': str(datetime.datetime.utcnow()), 'reward': hex(key.publickey().n)[2:], 'difficulty':'9', 'nonce':'', 'parent': res[0]['hash']}


def find_hash_index(hash_, blocks):
    for i in range(len(blocks)):
        if hash_ == blocks[i]['hash']:
            return i
    return -1

def find_chain_length(hash_, blocks):
    length_ = 0
    index = find_hash_index(hash_, blocks)
    while(index > -1):
        length_ += 1
        index = find_hash_index(json.loads(blocks[index]['block'])['parent'], blocks)
    return length_



# returns the end of longest chain
def build_chain():
    global block
    res = requests.get('https://gw.kaist.ac.kr/broadcast/get?reverse=1&&limit=200')
    res = res.json()
    for i in range(len(res)):
        a = find_chain_length(res[i]['hash'], res)
        if a > 50:
            block = {'type': 'block', 'transactions': [], 'timestamp': str(datetime.datetime.utcnow()), 'reward': hex(key.publickey().n)[2:], 'difficulty':'9', 'nonce':'', 'parent': res[i]['hash']}
            return (block, json.loads(res[i]['block'])['difficulty'])

def findnonce(block, init, diff, dd):
    nonce = init
    block['difficulty'] = str(dd)
    while(True):
        hash512 = SHA512.new()
        block['nonce'] = format(nonce, '064x')
        block['timestamp'] = str(datetime.datetime.utcnow())
        # block['timestamp'] = str(datetime.datetime.utcnow())
        J = json.dumps((block))
        hash512.update(str.encode(J))
        # print('\r' + hash512.hexdigest()[:10],'\t\t' , nonce, end='')
        if int(hash512.hexdigest(), 16) < 2 ** (492 - 4):
            print('\r',hash512.hexdigest())
            if int(hash512.hexdigest(), 16) < 2 ** (492 - int(dd)):
                print(hash512.hexdigest())
                my_block = {'hash': hash512.hexdigest(), 'type': 'block_hash', 'block': J}
                r = requests.post('https://gw.kaist.ac.kr/broadcast/post', json = my_block)
                print('done!!\n\n')
                return True
        nonce += diff
        if nonce > 100000:
            # print(block)
            return True

def findnonce_np(block, init, diff, dd):
    nonce = init
    while(True):
        hash512 = SHA512.new()
        block['nonce'] = str(hex(nonce))[:2]
        block['timestamp'] = str(datetime.datetime.utcnow())
        block['difficulty'] = dd
        hash512.update(str.encode(json.dumps(block)))
        # print('\r' + hash512.hexdigest()[:10],'\t\t' , nonce, end='')
        if int(hash512.hexdigest(), 16) < 2 ** (492):
            print('\r',hash512.hexdigest())
            if int(hash512.hexdigest(), 16) < 2 ** (492 - dd):
                # print(hash512.hexdigest())
                my_block = {'hash': hash512.hexdigest(), 'type': 'block_hash', 'block': json.dumps(block)}
                r = requests.post('https://gw.kaist.ac.kr/broadcast/post', json = my_block)
                print('done!!\n\n')
                return True
        nonce += diff

while(True):
    counter = 0
    block, diff = build_chain()
    print('\r', "new hash: ", block['parent'][:12], '\t', diff)
    findnonce(block, 0, 1, diff)
