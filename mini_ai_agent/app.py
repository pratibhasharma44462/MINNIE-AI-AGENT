from flask import Flask, render_template, request, jsonify, session
from tools  import generate_response
from database import init_db, create_session, save_message, get_history, clear_session
import uuid
import os
from dotenv import load_dotenv

load_dotenv()

app        = Flask(__name__)
app.secret_key = os.urandom(24)  

init_db()


def get_session_id() -> str:
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return session["session_id"]


@app.route("/", methods=["GET"])
def home():
    session_id = get_session_id()
    create_session(session_id)
    history    = get_history(session_id)
    return render_template("index.html", chats=history)


@app.route("/chat", methods=["POST"])
def chat():
    data    = request.get_json()
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Empty message"}), 400

    session_id = get_session_id()
    create_session(session_id)

    save_message(session_id, "user", message)

    history = get_history(session_id)

    reply = generate_response(history)

    save_message(session_id, "assistant", reply)

    return jsonify({"reply": reply})



@app.route("/clear", methods=["POST"])
def clear():
    session_id = get_session_id()
    clear_session(session_id)
    return jsonify({"status": "cleared"})


@app.route("/history", methods=["GET"])
def history():
    session_id = get_session_id()
    return jsonify(get_history(session_id))


if __name__ == "__main__":
    app.run(debug=True)