from app import db
from app.models.planet import Planet
from flask import Blueprint, jsonify, make_response, request

planet_bp = Blueprint("planet", __name__, url_prefix="/planets")




























# @planet_bp.route("", methods=["POST"])
# def create_planet():
#     request_body = request.get_json()
#     new_planet = Planet(name=request_body["name"],
#                     description=request_body["description"],
#                     diameter=request_body["diameter"])

#     db.session.add(new_planet)
#     db.session.commit()

#     return make_response(f"Planet {new_planet.name} successfully created", 201)

# @planet_bp.route("", methods=["GET"])
# def read_all_planets():
#     planets_response = []
#     planets = Planet.query.all()
#     for planet in planets:
#         planets_response.append(
#             {
#                 "id": planet.id,
#                 "title": planet.name,
#                 "description": planet.description,
#                 "diameter": planet.diameter
#                 }
#         )
#     return jsonify(planets_response)








# class Planet:
#     def __init__(self, id, name, description, diameter):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.diameter = diameter

#     def make_dict(self):
#         return dict(
#             id=self.id,
#             name=self.name,
#             description=self.description,
#             diameter=self.diameter
#         )


# planets = [
#     Planet(1, "Mercury", "smallest planet", 3031.9),
#     Planet(2, "Venus", "hottest planet", 7520.8),
#     Planet(3, "Earth", "home planet", 7917.5),
#     Planet(4, "Mars", "red planet", 4212.3),
#     Planet(5, "Jupiter", "biggest planet", 86881),
#     Planet(6, "Saturn", "ringed planet", 72367),
#     Planet(7, "Neptune", "blue planet", 30599),
#     Planet(8, "Uranus", "furthest planet", 31518)
# ]

# planet_bp = Blueprint("planet", __name__, url_prefix="/planets")

# @planet_bp.route("", methods=["GET"])
# def read_planets():
#     planet_list = [planet.make_dict() for planet in planets]
#     return jsonify(planet_list)

# @planet_bp.route("/<planet_id>", methods=["GET"])
# def handle_planet(planet_id):
#     planet = validate_planet(planet_id)
#     return planet

# def validate_planet(planet_id):
#     try:
#         planet_id = int(planet_id)
#     except ValueError:
#         abort(make_response({"message": f"planet {planet_id} invalid"}, 400))

#     for planet in planets:
#         if planet_id == planet.id:
#             return planet.make_dict()

#     abort(make_response({"message": f"planet {planet_id} not found"}, 404))