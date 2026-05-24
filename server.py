from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from x3dh import User, x3dh_sender, x3dh_recipient
from ratchet import DoubleRatchet
import json

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

alice = User("Alice")
bob   = User("Bob")

bob_bundle = bob.get_public_bundle()
alice_secret, alice_ephemeral = x3dh_sender(alice, bob_bundle)
bob_secret = x3dh_recipient(bob, alice.identity_key.public_key, alice_ephemeral)

alice_ratchet = DoubleRatchet(alice_secret)
bob_ratchet   = DoubleRatchet(bob_secret)

print("✓ Encrypted session established")

@app.route("/")
def home():
    return render_template("chat.html")

@socketio.on("send_message")
def handle_message(data):
    try:
        if isinstance(data, str):
            data = json.loads(data)
        sender  = data["sender"]
        message = data["message"]
    except Exception as e:
        print("Error parsing data:", data, e)
        return

    if sender == "alice":
        encrypted = alice_ratchet.encrypt(message)
        decrypted = bob_ratchet.decrypt(encrypted)
    else:
        encrypted = bob_ratchet.encrypt(message)
        decrypted = alice_ratchet.decrypt(encrypted)

    emit("receive_message", {
        "sender":    sender,
        "message":   decrypted,
        "encrypted": encrypted.hex()[:40] + "..."
    }, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", debug=True)