from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)

socketio = SocketIO(app)

@app.route("/")
def home():
    return render_template("chat.html")

@socketio.on("send_message")
def handle_message(message):

    print("Message:", message)

    emit("receive_message", message, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)