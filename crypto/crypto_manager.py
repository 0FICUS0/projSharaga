import base64  # для кодирования байтов в строку
import os  # для генерации случайных байт (соль и IV)
from cryptography.hazmat.primitives import hashes  # для хеширования в KDF
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC  # алгоритм KDF
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes  # для AES-шифрования
from cryptography.hazmat.backends import default_backend  # стандартный криптографический бэкенд

class CryptoManager:
    def __init__(self, password: str):
        self.password = password.encode()  # мастер-пароль в байтах
        self.backend = default_backend()  # бэкенд для криптоопераций

    def _derive_key(self, salt: bytes) -> bytes:
        # Генерация ключа из пароля и соли через PBKDF2 + SHA256
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),  # используем SHA256 как хеш-функцию
            length=32,  # длина ключа — 32 байта (256 бит)
            salt=salt,  # соль — 16 байт
            iterations=100_000,  # количество итераций для устойчивости
            backend=self.backend  # бэкенд
        )
        return kdf.derive(self.password)  # получаем ключ из пароля

    def encrypt(self, plaintext: str) -> str:
        salt = os.urandom(16)  # генерируем соль
        iv = os.urandom(16)  # генерируем IV (вектор инициализации)
        key = self._derive_key(salt)  # получаем ключ из пароля + соли
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=self.backend)  # создаем AES-шифр
        encryptor = cipher.encryptor()  # создаем объект шифрования
        ct = encryptor.update(plaintext.encode()) + encryptor.finalize()  # шифруем строку
        return base64.b64encode(salt + iv + ct).decode()  # кодируем результат (соль + iv + шифртекст) в base64

    def decrypt(self, encrypted_data: str) -> str:
        data = base64.b64decode(encrypted_data)  # декодируем base64 обратно в байты
        salt, iv, ct = data[:16], data[16:32], data[32:]  # разбираем: соль, IV, шифртекст
        key = self._derive_key(salt)  # получаем ключ по соли
        cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=self.backend)  # создаем AES-дешифратор
        decryptor = cipher.decryptor()  # объект расшифровки
        return (decryptor.update(ct) + decryptor.finalize()).decode()  # расшифровываем и переводим в строку

