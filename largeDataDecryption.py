import csv
from Crypto.Cipher import AES

# Define the path to the encrypted file and the key file
encrypted_file_path = "output_encrypted_file.enc"

# Read the encrypted data from the file
with open(encrypted_file_path, "rb") as f:
    encrypted_data = f.read()


from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Load the RSA private key
with open('private_key.pem', 'rb') as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
        backend=default_backend()
    )

# Load the RSA public key
with open('public_key.pem', 'rb') as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read(),
        backend=default_backend()
    )

# Load the encrypted AES key
with open('encrypted_aes_key.bin', 'rb') as key_file:
    encrypted_key = key_file.read()

# Decrypt the AES key using the RSA private key
aes_key = private_key.decrypt(
    encrypted_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)


encryption_key = aes_key

# Decrypt the data using AES encryption
cipher = AES.new(encryption_key, AES.MODE_CBC, encrypted_data[:AES.block_size])
decrypted_data = cipher.decrypt(encrypted_data[AES.block_size:])

# Convert the decrypted data from bytes to string
decrypted_data_str = decrypted_data.decode('utf-8')

# Split the decrypted data into rows
rows = decrypted_data_str.strip().split("\n")

# Create a CSV writer object
csv_writer = csv.writer(open("decrypted_data.csv", "w"))

# Write the rows to the CSV file
for row in rows:
    csv_writer.writerow(row.split(","))
