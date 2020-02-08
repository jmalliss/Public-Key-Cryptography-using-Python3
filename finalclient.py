import select, string, sys
import os.path
import pickle
import os
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from binascii import hexlify
from socket import *
from os import path

def send(outgoing):
	outgoing = outgoing.encode()
	outgoing = server_key.encrypt(outgoing, 32)
	print('Client1 Encrypted:\n',outgoing)
	print('\n')
	outgoing = pickle.dumps(outgoing)
	cl.send(outgoing)

def receive():
	incoming = cl.recv(1024)
	incoming = pickle.loads(incoming)
	print('Client2 Encrypted:\n',incoming)
	incoming = private_key.decrypt(incoming)
	incoming = incoming.decode()
	return(incoming)

#Checking if keys exist or not
if (path.exists('public_pem.pem') and path.exists('private_pem.pem') == True):
	print('The Public and Private Keys Exists!')
else:
	print('Either Private or Public key / Both Keys are missing!!!, Generating new keys...')
	#Generating New Keys if any key isn't existing
	private_key = RSA.generate(1024)
	public_key = private_key.publickey()
	private_pem = private_key.exportKey()
	public_pem = public_key.exportKey()
	with open('private_pem.pem', 'wb') as private:
    		private.write(private_pem)
	with open('public_pem.pem', 'wb') as public:
    		public.write(public_pem)

#Opening keys from stored file if they exist
print('Loading Keys...\n')
with open('private_pem.pem', 'rb') as private:
    		private_pem = private.read()
with open('public_pem.pem', 'rb') as public:
    		public_pem = public.read()
print('Private Key in Bytes form:\n',private_pem)
print('\n')
print('Public Key in Bytes form:\n',public_pem)
print('\n')
private_key = RSA.importKey(private_pem)
public_key = RSA.importKey(public_pem)
print('Private Key in RSAobj form:\n',private_key)
print('\n')
print('Public Key in RSAobj form:\n',public_key)
print('\n')

#Establishing Socket Connection
print('Establishing Socket Connection...')
cl = socket(AF_INET, SOCK_STREAM)
cl.connect(('10.110.194.211',50000))
a='Client'
cl.send(a.encode())

#Exchanging Public Keys
ServerKey=cl.recv(1024)
print('Server Key:\n',ServerKey)
print('\n')
with open('server_pem.pem', 'wb') as server:
	server.write(ServerKey)
server_key= RSA.importKey(ServerKey)
cl.send(public_pem) 
#Chat session initializing
print('Chat session initialized!\n')
while True:
	print('Client1:')
	outgoing = sys.stdin.readline().strip()
	if outgoing == 'exit':
		send(outgoing) 
		break
	send(outgoing)
	incoming=receive()
	print('Client2:\n',incoming)
	print('\n')
	if incoming == 'exit':
		break
cl.close()
print('Connection Terminated!\n')
os.remove("server_pem.pem")
print('Server Key File Deleted!')
