import sys
import os

os.system("python3 sig.py -s key.json < input.txt")
# Reads input.txt and writes a file named "signature" that holds the signature
#signed with key.json and message from input.txt.

#os.system("python3 sig.py -p key.json < input.txt")
# Upper line reads input.txt and makes a file named payload.json
#that has the message, signature and public key.

os.system("python3 sig.py -v payload.json")
# Reads the payload.json file and verifies whether the message is
#signed by the key owner.
