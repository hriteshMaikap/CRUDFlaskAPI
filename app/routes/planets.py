from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import Planets
from app.schemas import planet_schema, planets_schema
from app import db

planets_bp = Blueprint('planets', __name__)

@planets_bp.route('/', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    return jsonify(planets_schema.dump(planets))

@planets_bp.route('/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({"message": "Planet not found"}), 404
    return jsonify(planet_schema.dump(planet))

@planets_bp.route('/', methods=['POST'])
@jwt_required()
def add_planet():
    data = request.get_json()
    planet = Planets(**data)
    db.session.add(planet)
    db.session.commit()
    return jsonify({"message": "Planet added successfully"}), 201

@planets_bp.route('/<int:planet_id>', methods=['PUT'])
@jwt_required()
def update_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({"message": "Planet not found"}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(planet, key, value)
    db.session.commit()
    return jsonify({"message": "Planet updated successfully"})

@planets_bp.route('/<int:planet_id>', methods=['DELETE'])
@jwt_required()
def delete_planet(planet_id):
    planet = Planets.query.get(planet_id)
    if not planet:
        return jsonify({"message": "Planet not found"}), 404
    db.session.delete(planet)
    db.session.commit()
    return jsonify({"message": "Planet deleted successfully"}), 202
