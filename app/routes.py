from app import db
from app.models.planet import Planet
from flask import Blueprint, jsonify, make_response, request, abort

planet_bp = Blueprint("planet", __name__, url_prefix="/planets")


@planet_bp.route("", methods=["POST"])
def create_planet():
    data = request.json
    
    planet = Planet(
        name=data['name'], 
        description=data['description'], 
        diameter=data['diameter']
    )
    
    db.session.add(planet)
    db.session.commit()
    
    return make_response(jsonify(f"Planet {planet.name} successfully created")), 201

@planet_bp.route("", methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    
    planet_list = [planet.to_dict() for planet in planets]

    return jsonify(planet_list)

def validate_planet(id):
    try:
        id = int(id)
    except:
        message = f"planet {id} is invalid"
        abort(make_response({"message": message}, 400))
        
    planet = Planet.query.get(id)
    
    if not planet:
        message = f"planet {id} not found"
        abort(make_response({"message": message}, 404))

@planet_bp.route("/<planet_id>", methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet:
        return planet.to_dict()
    else:
        return make_response(f"Planet {planet_id} not found", 404)

@planet_bp.route("/<planet_id>", methods=["PUT"])
def update_planet(planet_id):
    planet = validate_planet(planet_id)
    request_body = request.get_json()

    if "name" not in request_body or "description" not in \
        request_body or "diameter" not in request_body:
        return make_response("Incomplete request body", 400)
    else:
        planet.name = request_body["name"]
        planet.description = request_body["description"]
        planet.diameter = request_body["diameter"]

        db.session.commit()

        return make_response(jsonify(f"Planet #{planet.id} successfully updated", 200))

@planet_bp.route("/<planet_id>", methods=['DELETE'])
def delete_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return make_response(jsonify(f"Planet {planet_id} not found", 404))
    
    db.session.delete(planet)
    db.session.commit()
    
    return make_response(jsonify(f"Planet {planet_id} successfully deleted", 200))