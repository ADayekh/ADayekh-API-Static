"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

John = {
    "first_name": "John",
    "age": 33,
    "lucky_numbers": [7, 13, 22]
}

Jane = {
    "first_name": "Jane",
    "age": 35,
    "lucky_numbers": [10, 14, 3]
}

Jimmy = {
    "first_name": "Jimmy",
    "age": 5,
    "lucky_numbers": [1]
}

jackson_family.add_member(John)
jackson_family.add_member(Jane)
jackson_family.add_member(Jimmy)



# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_members():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    if members is not None:
        return jsonify(members), 200
    else:
        return "Not members found", 404



@app.route('/member/<int:id>', methods=['GET'])
def obtain_member(id):
    member = jackson_family.get_member(id)
    if member is not None:
        return jsonify(member), 200
    else:
        return "Not member found", 404

@app.route('/member', methods=['POST'])
def add_member():
    member = request.get_json()
    if 'first_name' not in member :
        return "No name", 400
    if 'age' not in member:
        return "No age", 400
    if 'lucky_numbers' not in member:
        return "No numbers", 400
    print("Member added", member)
    jackson_family.add_member(member)
    if member is not None:
        return "Member created", 200



@app.route('/member/<int:id>', methods=['DELETE'])
def delete_member(id):
    jackson_family.delete_member(id)
    return "Member deleted", 200



if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
