import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from crypto.encryption import *

password = "my_super_password"
salt = generate_salt()
key = derive_key(password, salt)

text = "Привет, это секретная заметка"

ciphertext = encrypt_note(text, key)
print("Зашифрованный текст:", ciphertext)

# Проверим расшифровку
key2 = derive_key(password, salt)
plaintext = decrypt_note(ciphertext, key2)
print("Расшифровка:", plaintext)