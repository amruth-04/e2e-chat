from nacl.public import PrivateKey

class User:
    def __init__(self, name):
        self.name = name
        self.identity_key  = PrivateKey.generate()
        self.signed_prekey = PrivateKey.generate()
        self.onetime_prekey = PrivateKey.generate()

    def get_public_bundle(self):
        return {
            "identity_key":   self.identity_key.public_key,
            "signed_prekey":  self.signed_prekey.public_key,
            "onetime_prekey": self.onetime_prekey.public_key,
        }

alice = User("Alice")
bob   = User("Bob")

bob_bundle = bob.get_public_bundle()

print(f"Bob's public bundle:")
for key_name, key_value in bob_bundle.items():
    print(f"  {key_name}: {bytes(key_value).hex()[:32]}...")