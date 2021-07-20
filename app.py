import json
import pymongo
from flask import Flask
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
    if collection.count_documents({"email": email }) > 0:
        return ('Email Verified', 201 )
    else:
        return ('Email Not Found', 202 )

@app.route('/signup', methods=['POST'])
def insertUser():
    user = request.get_json()
    collection.insert_one(user).inserted_id
    return ('Successfully Registered', 200 )

if __name__ == '__main__':
    app.run()
