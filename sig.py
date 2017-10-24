import sys
import json
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA512

'''
Functions
1. Read key.json, payload.json
2. write a signature (-s option)
3. write a verify file (-v option)
'''

#hash object
hash_512 = SHA512.new()

#check_dict_keys
#input  : dictionary, tuple of strings
#output : boolean whether the keysets are all in the dictionary or not
#checks if json file is what we need
def check_dict_keys(dict, keyset):
    keys = dict.keys()
    for i in keyset:
        if not(i in keys):
            return False
    return True

#genPrivateKey
#input  : modulus, publicExponent, privateExponent
#output : RSA Private key
def genPrivateKey(mod, pub, priv):
    payload = (int(mod, 16), int(pub, 16), int(priv, 16))
    return RSA.construct(payload)

#genPublicKey
#input  : modulus, publicExponent
#output : RSA Public Key
def genPublicKey(mod, pub):
    payload = (int(mod.split('x')[1], 16), int(pub.split('x')[1], 16))
    return RSA.construct(payload)

#genKey
#input  : tuple of numbers
#output : RSA key public or private, according to the length of tuple
def genKey(payload):
    if len(payload) == 3:
        return genPrivateKey(payload[0], payload[1], payload[2])
    elif len(payload) == 2:
        return genPublicKey(payload[0], payload[2])

#sign
#input  : RSA Private Key, String
#output : HEX of (signed message)
def sign(sk, msg):
    hash_512.update(str.encode(msg))
    return hex(int(sk._decrypt(int(hash_512.hexdigest(), 16))))

#parse
#input  : String (file name)
#output : Dictionary of the read json file
def parse(filename):
    with open(filename) as payload:
        result = json.load(payload)
    return result

#verify
#input  : RSA Public Key, String(Message), String(HEX Signature)
def verify(pk, msg, sig):
    hash_512.update(str.encode(msg))
    if int(hash_512.hexdigest(), 16) == pk._encrypt(int(sig, 16)):
        return True
    else:
        return False

option = None
if len(sys.argv) == 3:
    #option -s : sign a message(given input) with given key.
    if sys.argv[1] == '-s':
        #parse the json
        payload = parse(sys.argv[2])
        #check if the json is what we need
        if not(check_dict_keys(payload, ('publicExponent', 'modulus', 'privateExponent'))):
            print('Wrong input file: The json file has wrong arguments')
            quit()
        #get a message as input
        txt = input()
        #sign the message
        signature = sign(genPrivateKey(payload['modulus'], payload['publicExponent'], payload['privateExponent']), txt)
        with open('signature', 'w') as outfile:
            outfile.write(signature)
            outfile.close()
    #option -p : make a payload with given input.
    elif sys.argv[1] == '-p':
        payload = parse(sys.argv[2])
        if not(check_dict_keys(payload, ('publicExponent', 'modulus', 'privateExponent'))):
            print('Wrong input file: The json file has wrong arguments')
            quit()
        txt = input()
        signature = sign(genPrivateKey(payload['modulus'], payload['publicExponent'], payload['privateExponent']), txt)
        result = {
        "message": txt,
        "sig":
            {
            "modulus" : payload['modulus'],
            "publicExponent" : payload["publicExponent"],
            "signature" : signature
            }
        }
        with open('payload.json', 'w') as outfile:
            json.dump(result, outfile)
    elif sys.argv[1] == '-v':
        payload = parse(sys.argv[2])

        if not(check_dict_keys(payload, ('message', 'sig'))):
            print('Wrong input file: The json file has wrong arguments')
            quit()
        elif not(check_dict_keys(payload['sig'], ('modulus', 'publicExponent', 'signature'))):
            print('Wrong input file: Sig in jsonfile has wrong arguments')
            quit()

        f = open('verify', 'w')
        if verify(genPublicKey(payload['sig']['modulus'], payload['sig']['publicExponent']), payload['message'], payload['sig']['signature']):
            f.write('True')
            #print("Signature is Valid")
            #Uncomment upper line to see validity in command line
        else:
            f.write('False')
        f.close()

    else:
        print('Please check the usage')
        print('python3 THISCODE.py [option] [json file] ([< INPUTFILE])')
        print('-s : To get the signature file')
        print('-p : To get the signed payload file')
        print('-v : To verity a payload\n')
        print('e.g. python3 THISCODE.py -s dir/key.json < input.txt')
elif sys.argv[1] == '-h' or sys.argv[1] == '--help':
    print('python3 THISCODE.py [option] [json file] ([< INPUTFILE])')
    print('-s : To get the signature file')
    print('-p : To get the signed payload file')
    print('-v : To verity a payload\n')
    print('python3 THISCODE.py -s dir/key.json < input.txt')
else:
    print('Please check the arguments & usage')
    print('python3 THISCODE.py [option] [json file] ([< INPUTFILE])')
    print('-s : To get the signature file')
    print('-p : To get the signed payload file')
    print('-v : To verity a payload\n')
    print('e.g. python3 THISCODE.py -s dir/key.json < input.txt')
