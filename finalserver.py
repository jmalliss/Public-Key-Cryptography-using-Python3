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
	outgoing = client_key.encrypt(outgoing, 32)
	print('Client2 Encrypted:\n',outgoing)
	print('\n')
	outgoing = pickle.dumps(outgoing)
	p.send(outgoing)

def receive():
	incoming = p.recv(1024)
	incoming = pickle.loads(incoming)
	print('Client1 Encrypted:\n',incoming)
	incoming = private_key.decrypt(incoming)
	incoming = incoming.decode()
	return(incoming)

#Checking if keys exist or not
if (path.exists('public_pem.pem') and path.exists('private_pem.pem') == True):
	print('The Public and Private Keys Exists!')
else:
	print('Either Private or Public key / Both Keys are missing!!!, Generating new keys...')
	#Generating New Keys if any key isnt existing
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
se = socket(AF_INET, SOCK_STREAM)
se.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
se.bind(('', 50000))
se.listen(5)      
print ("socket is listening...")
while True:
	(p,addr) = se.accept()
	a=p.recv(1024).decode()
	print('Connected to:',a)
	p.send(public_pem)
#Exchanging Public Keys
	ClientKey=p.recv(1024)
	print('Client Key:\n',ClientKey)
	print('\n')
	with open('client_pem.pem', 'wb') as client:
    		client.write(ClientKey)
	client_key= RSA.importKey(ClientKey)
	#Chat session initializing
	print('Chat session initialized!\n')
	while True:
		incoming=receive()
		print('Client1:\n',incoming)
		print('\n')
		if incoming == 'exit':
			break 
		print('Client2:')
		outgoing = sys.stdin.readline().strip()
		if outgoing == 'exit':
			send(outgoing)
			break
		send(outgoing)
	break	
p.close()
print('Connection Terminated!\n')
os.remove("client_pem.pem")
print('Client Key File Deleted!')
	

