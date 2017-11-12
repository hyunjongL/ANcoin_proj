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
res = requests.get('https://gw.kaist.ac.kr/broadcast/get?reverse=1&&limit=10')
res = res.json()
nonce = 0
diff = int(json.loads(res[0]['block'])['difficulty'])

block = {'type': 'block', 'transactions': [], 'timestamp': str(datetime.datetime.utcnow()), 'reward': hex(key.publickey().n)[2:], 'difficulty':'9', 'nonce':'', 'parent': res[0]['hash']}


def findnonce(block, init, diff, dd):
    nonce = init
    while(True):
        hash512 = SHA512.new()
        block['nonce'] = str(hex(nonce))[:2]
        block['timestamp'] = str(datetime.datetime.utcnow())
        hash512.update(str.encode(json.dumps(block)))
        print('\r' + hash512.hexdigest()[:10],'\t\t' , nonce, end='')
        if int(hash512.hexdigest(), 16) < 2 ** (492 - 4):
            print('\r',hash512.hexdigest())
            if int(hash512.hexdigest(), 16) < 2 ** (492 - dd):
                print(hash512.hexdigest())
                my_block = {'hash': hash512.hexdigest(), 'type': 'block_hash', 'block': json.dumps(block)}
                r = requests.post('https://gw.kaist.ac.kr/broadcast/post', json = my_block)
                print('done!!\n\n')
                return True
        nonce += diff

def findnonce_np(block, init, diff, dd):
    nonce = init
    while(True):
        hash512 = SHA512.new()
        block['nonce'] = str(hex(nonce))[:2]
        block['timestamp'] = str(datetime.datetime.utcnow())
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

# findnonce(block, 0, 1)

findnonce(block, 0, 1, 9)
