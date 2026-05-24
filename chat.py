from x3dh import User, x3dh_sender, x3dh_recipient
from ratchet import DoubleRatchet

def setup_session(alice, bob):
    bob_bundle = bob.get_public_bundle()
    alice_secret, alice_eph = x3dh_sender(alice, bob_bundle)
    bob_secret = x3dh_recipient(bob, alice.identity_key.public_key, alice_eph)
    return DoubleRatchet(alice_secret), DoubleRatchet(bob_secret)

def chat():
    print("=" * 50)
    print("   E2E Encrypted Messenger")
    print("   Built with X3DH + Double Ratchet")
    print("=" * 50)
    print()

    alice = User("Alice")
    bob   = User("Bob")

    alice_ratchet, bob_ratchet = setup_session(alice, bob)
    print("✓ Secure session established\n")

    while True:
        print("Options: 1) Alice sends  2) Bob sends  3) Quit")
        choice = input("Choice: ").strip()

        if choice == "1":
            msg = input("Alice: ").strip()
            ct  = alice_ratchet.encrypt(msg)
            print(f"[encrypted]: {ct.hex()[:40]}...")
            pt  = bob_ratchet.decrypt(ct)
            print(f"Bob sees: {pt}\n")

        elif choice == "2":
            msg = input("Bob: ").strip()
            ct  = bob_ratchet.encrypt(msg)
            print(f"[encrypted]: {ct.hex()[:40]}...")
            pt  = alice_ratchet.decrypt(ct)
            print(f"Alice sees: {pt}\n")

        elif choice == "3":
            print("Session ended.")
            break

        else:
            print("Invalid choice\n")

chat()