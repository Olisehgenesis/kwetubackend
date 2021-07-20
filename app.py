import json
import pymongo
from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


#connecting database
client = pymongo.MongoClient("mongodb+srv://admin:admin@kwetu.ig6hf.mongodb.net/users?retryWrites=true&w=majority")
db = client['users']
collection = db['kwetu']


@app.route('/login', methods=['POST'])
def checkuser():
    body = request.get_json()
    email = body.get('email')
    password = body.get('password')
    if collection.count_documents({"email": email , "password" : password}) > 0:
        return jsonify(
            success= 1 ,
            data = {'email': email,
            'password' : password}
        )
    else:
        return jsonify(
            success= 0 ,
            error_message = "invalid creditials")

@app.route('/signup', methods=['POST'])
def insertUser():
    user = request.get_json()
    x = collection.insert_one(user)
    return jsonify(
        success = 0,
        data = {'id' : x.inserted_id}
    )

    
if __name__ == '__main__':
    app.run()
