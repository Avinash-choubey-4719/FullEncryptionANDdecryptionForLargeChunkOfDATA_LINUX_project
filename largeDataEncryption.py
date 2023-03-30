import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Generate a 256-bit encryption key
encryption_key = os.urandom(32)
print(encryption_key)
# Open the input file containing the unencrypted data
with open('dataset_Kulasekharam.csv', 'rb') as input_file:

    # Open the output file to write the encrypted data
    with open('output_encrypted_file.enc', 'wb') as output_file:

        # Generate a random initialization vector (IV)
        iv = os.urandom(16)

        # Write the IV to the output file
        output_file.write(iv)

        # Create the AES cipher object with the encryption key and IV
        cipher = Cipher(algorithms.AES(encryption_key), modes.CBC(iv), backend=default_backend())

        # Generate the encryptor object from the cipher
        encryptor = cipher.encryptor()

        # Encrypt and write the data in blocks
        chunk_size = 1024*1024 # 1 MB
        while True:
            chunk = input_file.read(chunk_size)
            if len(chunk) == 0:
                break
            elif len(chunk) % 16 != 0:
                chunk += b' ' * (16 - len(chunk) % 16)
            output_file.write(encryptor.update(chunk))

        # Finalize the encryption process
        output_file.write(encryptor.finalize())
        
        
#Encryption of the Main AES key starts form here
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Generate RSA key pair
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()

# Define the encryption key
key = encryption_key

# Encrypt the key using RSA public key
encrypted_key = public_key.encrypt(
    key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("AES key :- ", encryption_key)
print("RSA private key :- ", private_key)
print("RSA public key :- ", public_key)


with open("private_key.pem", "wb") as f:
	f.write(private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ))

public_key_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open('public_key.pem', 'wb') as file:
	file.write(public_key_pem)
	

with open('encrypted_aes_key.bin', 'wb') as file:
	file.write(encrypted_key)
