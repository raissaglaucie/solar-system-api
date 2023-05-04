from app import db
from app.models.planet import Planet
from flask import Blueprint, jsonify, make_response, request, abort
from sqlalchemy.exc import DataError

planet_bp = Blueprint("planet", __name__, url_prefix="/planets")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        message = f"{cls.__name__} {model_id} invalid"
        abort(make_response({"message": message}, 400))

    model = cls.query.get(model_id)

    if not model:
        message = f"{cls.__name__} {model_id} not found"
        abort(make_response({"message": message}, 404))

    return model

@planet_bp.route("", methods=["POST"])
def create_planet():
    request_body = request.get_json()

    try:
        new_planet = Planet.from_dict(request_body)
        db.session.add(new_planet)
        db.session.commit()

        message = f"Planet {new_planet.name} successfully created"
        return make_response(jsonify(message)), 201
    except KeyError as e:
        expected_keys = ["name", "description", "diameter"]
        missing_keys = [key for key in expected_keys if key not in request_body]

        message = 'missing required values'
        error_dict = {"message": message, "missing_values": missing_keys}

        abort(make_response(error_dict, 400))
    except (TypeError, DataError) as e:
        error_dict = {
            "message": "Invalid request body",
            "error": str(e)
            }
        abort(make_response(jsonify(error_dict), 400))

@planet_bp.route("", methods=['GET'])
def get_all_planets():
    name_query = request.args.get("name")
    if name_query:
        planets = Planet.query.filter_by(name=name_query)
    else:
        planets = Planet.query.all()

    planet_list = [planet.to_dict() for planet in planets]
    return jsonify(planet_list)

@planet_bp.route("/<planet_id>", methods=['GET'])
def get_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    return jsonify(planet.to_dict()), 200 

@planet_bp.route("/<planet_id>", methods=["PUT"])
def replace_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    request_body = request.get_json()

    try: 
        planet.name = request_body["name"]
        planet.description = request_body["description"]
        planet.diameter = request_body["diameter"]
        db.session.commit()
        message = f"Planet #{planet.id} successfully updated"
        return make_response(jsonify(message)), 200
    except KeyError as e:
        expected_keys = ["name", "description", "diameter"]
        missing_keys = [key for key in expected_keys if key not in request_body]

        message = 'missing required values'
        error_dict = {"message": message, "missing_values": missing_keys}

        abort(make_response(error_dict, 400))
    except (TypeError, DataError) as e:
        error_dict = {
            "message": "Invalid request body",
            "error": str(e)
            }
        abort(make_response(jsonify(error_dict), 400))

@planet_bp.route("/<planet_id>", methods=["PATCH"])
def update_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    request_body = request.get_json()

    try:
        for key in request_body:
            setattr(planet, key, request_body[key])
        db.session.commit()
        message = f"Planet #{planet.id} successfully updated"
        return make_response(jsonify(message)), 200
    except (TypeError, KeyError, DataError) as e:
        error_dict = {
            "message": "Invalid request body",
            "error": str(e)
            }
        abort(make_response(jsonify(error_dict), 400))

@planet_bp.route("/<planet_id>", methods=['DELETE'])
def delete_planet(planet_id):
    planet = validate_model(Planet, planet_id)
    
    db.session.delete(planet)
    db.session.commit()
    
    message = f"Planet #{planet.id} {planet.name} successfully deleted" 
    return make_response(jsonify(message)), 200