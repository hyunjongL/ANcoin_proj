import requests
import json
import sig
import types


# Make a list for the Blockchain
def blockchain_init():
    return list()


# input: string hash, list chain
# Find a node with node.hash == hash
def find_parent(hash, chain):
    end = len(chain)
    for i in range(end):
        if chain[end-1-i].hash == hash:
            return chain[end-1-i]
    return -1


# input: string hash, list chain
# Find the index where chain[index].hash == hash
def find_hash(hash, chain):
    end = len(chain)
    for i in range(end):
        if chain[end-1-i].hash == hash:
            return end-i-1
    return -1


# input: int num, list chain
# Traverse chain from index = num to root(ancestors)
# It is used to check if the chain is successfully built
# You may add prints or other methods to validate/check the chain
def traverse_chain(num, chain):
    node = chain[num]
    while(node.parent != -1):
        if node.transaction_num > 0:
            print (node.transaction[0]['transaction']['from'])
        node = node.parent


# input: block_node node, list chain
# Calculated the balance of all users till the given node.
def calcuate_balance(node, chain):
    balance = {}
    while(node.parent != -1):
        if node.transaction_num > 0:
            for i in range(node.transaction_num):
                transaction_json = json.loads(node.transaction[i]['transaction'])
                to_key = transaction_json['to']
                from_key = transaction_json['from']
                amount = transaction_json['amount']
                if to_key in balance:
                    balance[to_key] += amount
                else:
                    balance[to_key] = amount
                if from_key in balance:
                    balance[from_key] -= amount
                else:
                    balance[from_key] = 0 - amount
        if node.reward in balance:
            balance[node.reward] += 1000
        else:
            balance[node.reward] = 1000
        node = node.parent
    return balance


class block_node:

    def __init__(self, block, chain):
        if(block['type'] == 'transaction_sign'):
            return
        block_json = json.loads(block['block'])
        self.enchain(block_json['reward'], block['hash'],
                     block_json['transactions'],
                     block_json['parent'], chain)

    # input: String Reward, String Hash, String Transaction, List Chain
    def enchain(self, reward, hash, transaction, parent, chain):
        self.hash = hash
        self.reward = reward
        # this loads a list of transaction blocks
        # to access a transaction,
        # json.loads(transaction[i]['transaction'])['from']
        # json.loads(transaction[i]['transaction'])['to']
        self.transaction = transaction
        self.transaction_num = len(self.transaction)
        self.parent = find_parent(parent, chain)
        chain.append(self)
        return self

    def __str__():
        return self.hash


# Get the Size
def get_Size():
    curr_index = 1
    total_length = 0
    counter = 1000
    while(counter == 1000):
        URL = ('http://gw.kaist.ac.kr/broadcast/get?start_at='
               + str(curr_index))
        response = requests.get(URL)
        counter = len(response.json())
        total_length += counter
        curr_index += counter
        if(counter == 0):
            return total_length
    total_length += len(response.json())
    return total_length


# Gets a String formatted json 'Transaction'
# Returns True or False according to verify result
def verify_transaction(block, hash_512):
    transaction = json.loads(block['transaction'])
    pub_key = sig.genPublicKey(transaction['from'], '10001')
    return sig.verify(pub_key, block['transaction'], block['sign'], hash_512)


# Verify a block or a transaction
def block_verify(block):
    if not isinstance(block, dict):
        return False
    if 'type' in block:
        pass
    else:
        return False
    type_ = block["type"]
    hash_512 = sig.hash_init()
    if(type_ == 'block_hash'):
        given_hash = int(block["hash"], 16)
        hash_512.update(str.encode(block["block"]))
        calculated_hash = int(hash_512.hexdigest(), 16)
        difficulty = int(json.loads(block["block"])['difficulty'])
        return ((given_hash == calculated_hash) and
                (given_hash < 2 ** (512 - difficulty)))
    elif (type_ == "transaction_sign"):
        return verify_transaction(block, hash_512)


if __name__ == "__main__":
    # block_chain_size = get_Size()
    # print(block_chain_size)
    counter = 0
    get_length = 1000
    index_counter = 0
    blockchain = blockchain_init()
    while(get_length == 1000):
        res = requests.get('http://gw.kaist.ac.kr/broadcast/get?start_at='
                           + str(1000 * index_counter))
        block_json = res.json()
        get_length = len(block_json)
        for i in range(get_length):
            if not block_verify(block_json[i]):
                counter += 1
            else:
                block_node(block_json[i], blockchain)
        index_counter += 1
    # print(blockchain)
    traverse_chain(300, blockchain)