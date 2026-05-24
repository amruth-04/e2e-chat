import hmac
import hashlib
from nacl.secret import SecretBox

def kdf(key, input_bytes):
    return hmac.new(key, input_bytes, hashlib.sha256).digest()

class DoubleRatchet:
    def __init__(self, shared_secret):
        self.root_key       = shared_secret[:32]
        self.send_chain_key = shared_secret[32:64]
        self.recv_chain_key = shared_secret[32:64]

    def encrypt(self, plaintext):
        msg_key             = kdf(self.send_chain_key, b"message_key")
        self.send_chain_key = kdf(self.send_chain_key, b"chain_key")
        box                 = SecretBox(msg_key)
        return box.encrypt(plaintext.encode())

    def decrypt(self, ciphertext):
        msg_key             = kdf(self.recv_chain_key, b"message_key")
        self.recv_chain_key = kdf(self.recv_chain_key, b"chain_key")
        box                 = SecretBox(msg_key)
        return box.decrypt(ciphertext).decode()

from x3dh import User, x3dh_sender, x3dh_recipient

alice = User("Alice")
bob   = User("Bob")

bob_bundle   = bob.get_public_bundle()
alice_secret, alice_ephemeral_pub = x3dh_sender(alice, bob_bundle)
bob_secret   = x3dh_recipient(bob, alice.identity_key.public_key, alice_ephemeral_pub)

alice_ratchet = DoubleRatchet(alice_secret)
bob_ratchet   = DoubleRatchet(bob_secret)

messages = [
    "Hey Bob!",
    "This is fully encrypted",
    "Every message uses a different key",
]

print("--- Alice sending messages ---\n")
ciphertexts = []
for msg in messages:
    ct = alice_ratchet.encrypt(msg)
    ciphertexts.append(ct)
    print(f"Original:  {msg}")
    print(f"Encrypted: {ct.hex()[:40]}...")
    print()

print("--- Bob decrypting messages ---\n")
for ct in ciphertexts:
    pt = bob_ratchet.decrypt(ct)
    print(f"Decrypted: {pt}")