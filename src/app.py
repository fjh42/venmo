import json
from flask import Flask, request
import db

DB = db.DatabaseDriver()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world!"

@app.route("/api/users/",methods=["GET"])
def get_all_users():
    """
    Get all users from the database.
    """
    return json.dumps({"users":DB.get_all_users()}),200

@app.route("/api/users/<int:user_id>/",methods=["GET"])
def get_user_by_id(user_id):
    """
    Get an specific user by their id.
    """
    user = DB.get_specific_user(user_id)
    if user is None:
        return json.dumps({"error":"User not found."}),404
    
    return json.dumps(user),200

@app.route("/api/users/",methods=["POST"])
def create_new_user():
    """
    Create a new user with 'name','username', and 'balance'. Default balance to 0 if not provided.
    """
    body = json.loads(request.data)
    name = body.get("name")
    username = body.get("username")

    if name is None or username is None:
        return json.dumps({"error":"Name or Username not provided."}),400

    balance = body.get("balance",0)

    new_user_id = DB.create_new_user(name,username,balance)
    new_user = DB.get_specific_user(new_user_id)

    return json.dumps(new_user),201

@app.route("/api/users/<int:user_id>/",methods=["DELETE"])
def delete_user(user_id):
    user = DB.get_specific_user(user_id)
    if not user:
        return json.dumps({"error":"User not found."}),404

    DB.delete_user(user_id)
    return json.dumps(user),200

@app.route("/api/send/",methods=["POST"])
def send_money():
    """
    Send money from one user to another.
    """
    body = json.loads(request.data)
    sender_id = body.get("sender_id")
    receiver_id = body.get("receiver_id")
    amount = body.get("amount")

    if sender_id is None or receiver_id is None or not isinstance(amount,int):
        return json.dumps({"error":"Transaction invalid. Must provide a sender_id, a receiver_id, and an integer amount."}),400
    
    sender = DB.get_specific_user(sender_id)
    receiver = DB.get_specific_user(receiver_id)

    if not sender or not receiver:
        return json.dumps({"error":"Sender or Receiver  not found."}),404
    
    new_sender_balance = sender.get("balance") - amount
    new_receiver_balance = receiver.get("balance") + amount
    DB.update_users_balance(sender_id,new_sender_balance,receiver_id,new_receiver_balance)

    return json.dumps({"sender_id":sender_id, "receiver_id":receiver_id,"amount": amount}),200


if __name__ == "__main__":
    DB.create_users_table()
    app.run(host="0.0.0.0", port=5000, debug=True)
