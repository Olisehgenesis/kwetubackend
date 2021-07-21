from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow 
import os

# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

# User Class/Model
class User(db.Model):
  __tablename__ = 'User'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(100), unique=True)
  email = db.Column(db.String(200))
  district = db.Column(db.String(200))
  phone = db.Column(db.String(20))
  password = db.Column(db.String(30))

  def __init__(self, username, email, district, phone, password):
    self.username = username
    self.email = email
    self.district = district
    self.phone = phone
    self.password = password

# User Schema
class ProductSchema(ma.Schema):
  class Meta:
    fields = ('id', 'username', 'email', 'district', 'phone' , 'password')

# Init schema
product_schema = ProductSchema(strict=True)
products_schema = ProductSchema(many=True, strict=True)

# Create a User
@app.route('/user', methods=['POST'])
def add_product():
  username = request.json['username']
  email = request.json['email']
  district = request.json['district']
  phone = request.json['phone']
  password = request.json['password']

  new_product = User(username, email, district, phone , password)

  db.session.add(new_product)
  db.session.commit()

  return product_schema.jsonify(new_product)

# Get All Products
@app.route('/user', methods=['GET'])
def get_products():
  all_products = User.query.all()
  result = products_schema.dump(all_products)
  return jsonify(result.data)

# Get Single Products
@app.route('/user/<id>', methods=['GET'])
def get_product(id):
  user = User.query.get(id)
  return product_schema.jsonify(user)

# Update a User
@app.route('/user/<id>', methods=['PUT'])
def update_product(id):
  user = User.query.get(id)

  username = request.json['username']
  email = request.json['email']
  district = request.json['district']
  phone = request.json['phone']

  user.username = username
  user.email = email
  user.district = district
  user.phone = phone

  db.session.commit()

  return product_schema.jsonify(user)

# Delete User
@app.route('/user/<id>', methods=['DELETE'])
def delete_product(id):
  user = User.query.get(id)
  db.session.delete(user)
  db.session.commit()

  return product_schema.jsonify(user)
db.create_all()


@app.route('/api/v2/login', methods=['POST'])
def login():
  #body= request.body.json()
  email = request.json['email']
  password = request.json ['password']
  exists = db.session.query(User.email).filter_by(email=email).first()
  if exists is not None:
        return jsonify('sucessful' , 200)
  else:
        return jsonify('unsucessful', 201)

      


# Run Server
if __name__ == '__main__':
  app.run()
