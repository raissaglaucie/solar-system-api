from app import db
from app.models.planet import Planet
from flask import Blueprint, jsonify, make_response, request, abort

planet_bp = Blueprint("planet", __name__, url_prefix="/planets")


@planet_bp.route("", methods=["POST"])
def create_planet():
    request_body = request.get_json()
    planet = Planet.from_dict(request_body)
    
    db.session.add(planet)
    db.session.commit()
    
    return make_response(jsonify(f"Planet {planet.name} successfully created")), 201

@planet_bp.route("", methods=['GET'])
def get_planets():
    name_query = request.args.get("name")

    planet_query = Planet.query 

    if name_query:
        planet_query = planet_query.filter_by(name=name_query)

    planets = planet_query.all()

    planets_response = [planet.to_dict() for planet in planets]
    return jsonify(planets_response), 200



def  validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))

    return model


@planet_bp.route("/<planet_id>", methods=['GET'])
def get_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    return jsonify(planet.to_dict()), 200 

@planet_bp.route("/<planet_id>", methods=["PUT"])
def update_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    request_body = request.get_json()

    if "name" not in request_body or "description" not in \
        request_body or "diameter" not in request_body:
        return make_response("Incomplete request body", 400)
    else:
        planet.name = request_body["name"]
        planet.description = request_body["description"]
        planet.diameter = request_body["diameter"]

        db.session.commit()

        return make_response(jsonify(f"Planet #{planet.id} successfully updated"), 200)  

@planet_bp.route("/<planet_id>", methods=['DELETE'])
def delete_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    db.session.delete(planet)
    db.session.commit()
    
    return make_response(jsonify(f"Planet {planet_id} successfully deleted", 200))