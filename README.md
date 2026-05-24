# E2E Encrypted Messenger

A working end-to-end encrypted messaging system built from scratch in Python,
implementing the same cryptographic protocols used by Signal, WhatsApp, and iMessage.

## What it does

- Two users can exchange messages that nobody else can read
- Every message uses a completely different encryption key
- Even if a key is stolen today, past messages stay safe (forward secrecy)
- Built using real cryptographic primitives — not a black box library

## Protocols implemented

**X3DH (Extended Triple Diffie-Hellman)**
Allows two users to establish a shared secret even if one is offline.
Uses four Diffie-Hellman operations combined into one master secret.

**Double Ratchet**
Every single message gets a fresh encryption key.
Old keys are deleted immediately — compromising one key reveals nothing
about past or future messages.

## Project structure

- `keys.py` — User class with identity, signed, and one-time prekeys
- `x3dh.py` — X3DH handshake, derives shared master secret
- `ratchet.py` — Double Ratchet, per-message key generation
- `chat.py` — CLI chat interface

## Run it yourself

```bash
git clone https://github.com/YourUsername/e2e-messenger.git
cd e2e-messenger
python -m venv venv
venv\Scripts\activate
pip install PyNaCl
python chat.py
```

## Tools used

- Python 3.13
- PyNaCl (libsodium bindings)

## References

- [Signal X3DH Specification](https://signal.org/docs/specifications/x3dh/)
- [Signal Double Ratchet Specification](https://signal.org/docs/specifications/doubleratchet/)