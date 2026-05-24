from nacl.public import PrivateKey, Box

class User:
    def __init__(self, name):
        self.name        = name
        self.identity_key   = PrivateKey.generate()
        self.signed_prekey  = PrivateKey.generate()
        self.onetime_prekey = PrivateKey.generate()

    def get_public_bundle(self):
        return {
            "identity_key":   self.identity_key.public_key,
            "signed_prekey":  self.signed_prekey.public_key,
            "onetime_prekey": self.onetime_prekey.public_key,
        }

def x3dh_sender(sender, recipient_bundle):
    ephemeral_key = PrivateKey.generate()

    dh1 = Box(sender.identity_key,  recipient_bundle["signed_prekey"]).shared_key()
    dh2 = Box(ephemeral_key,        recipient_bundle["identity_key"]).shared_key()
    dh3 = Box(ephemeral_key,        recipient_bundle["signed_prekey"]).shared_key()
    dh4 = Box(ephemeral_key,        recipient_bundle["onetime_prekey"]).shared_key()

    master_secret = dh1 + dh2 + dh3 + dh4
    return master_secret, ephemeral_key.public_key

def x3dh_recipient(recipient, sender_identity_pub, sender_ephemeral_pub):
    dh1 = Box(recipient.signed_prekey,  sender_identity_pub).shared_key()
    dh2 = Box(recipient.identity_key,   sender_ephemeral_pub).shared_key()
    dh3 = Box(recipient.signed_prekey,  sender_ephemeral_pub).shared_key()
    dh4 = Box(recipient.onetime_prekey, sender_ephemeral_pub).shared_key()

    master_secret = dh1 + dh2 + dh3 + dh4
    return master_secret

alice = User("Alice")
bob   = User("Bob")

bob_bundle = bob.get_public_bundle()

alice_secret, alice_ephemeral_pub = x3dh_sender(alice, bob_bundle)
bob_secret = x3dh_recipient(bob, alice.identity_key.public_key, alice_ephemeral_pub)

print(f"Alice's secret: {alice_secret.hex()[:32]}...")
print(f"Bob's secret:   {bob_secret.hex()[:32]}...")
print(f"\nDo they match? {alice_secret == bob_secret}")