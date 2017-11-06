# ANcoin_proj
This is a CS443 project for KAIST.
If you need any clarification, please don't hesitate contacting me.
email : hyunjongL at kaist dot ac dot kr

Usage(for now Project 1-1)

I recommend you to have a virtual environment and install the requirements.

Requirements : Python3 == 3.6.1, pycryptodome == 3.4.7, requests == 2.18.4
pycryptodome for RSA keys, encryption and decoding.
requests for making http requests and opening up the

<balance.py> Code
This script depends on sig.py as it uses sig.verify() and other tools to verify a transaction.
python3 balance.py [option] [parameter] ( > balance.json)
options:
  -h : give hash block for the parameter.
       Prints the calculated balance to stdout, which you can write it to a file name.
```
python3 balance.py -h 00000000e68a9542026c1c170da06ffcc4fbb83f41911b3676f263a6ff66aafdc31793be9e631e3540a2686aa5ad891b78745b13446fbb66a77b11bad3d50635 > balance.json
```


<sig.py> Code
This script can verify or sign a message/sign according to the private key, generated by Exponent and Modulus.
python3 sig.py [option] [input json file] (< input.txt-optional)
options
  -p : write a payload file signing input.txt (or std input) with key.json(input json)
  -s : write a signature file signing input.txt (or std input) with key.json(input json)
  -v : write a verify file with payload that holds message and public key
```
python3 sig.py -s key.json < input.txt
```
* if you don't have input.txt, you have to give std input by typing a message and hitting Return/Enter.



<test.py> Testing
The codes tests using <sig.py>. You can give your own input or use the default inputs.
Warning! you must not erase ./examples directory, which holds key and payloads, wrong and correct, and input.txt when using default settings.
You can provide each files to check whether <sig.py> correctly encodes and verifies.
```
python3 test.py [MESSAGE FILE] [KEY JSON FILE] [CORRECT PAYLOAD JSON] [WRONG PAYLOAD JSON]
Default input:
python3 test.py input.txt examples/key.json examples/payload.correct.json examples/payload.wrong.json
```



<main.py> Execution
python3 main.py
It reads key.json, input.txt and payload.json. Then, it makes files named signature and verify. The signed message is saved in signature and the verified result is saved in verify.
* For this code, input.txt is not optional, please make sure you make a txt file before running a test.
* The current ZIP holds the default input.txt file.
