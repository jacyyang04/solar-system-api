
from flask import Blueprint, jsonify, make_response, request, abort
from app.models.planet import Planet
from app import db


# Global Vars
planets_bp = Blueprint("planets_bp", __name__, url_prefix="/planets")


# Helper Functions
def get_planet(planet_id):
    """Get planet by planet_id or return 404"""
    return Planet.query.get_or_404(planet_id, description="Planet does not exist.")


# Routes
@planets_bp.route("", methods=["POST"])
def create_planets():
    """Create new planet in database."""
    request_body = request.get_json()

    if request_body is None:
        return make_response("Invalid Request", 400)

    if "name" not in request_body or "description" not in request_body or "xenomorphs" not in request_body:
        return make_response("Invalid Request", 400)

    new_planet = Planet(
        name=request_body['name'],
        description=request_body['description'],
        xenomorphs=request_body['xenomorphs']
    )

    # add and commit new_planet to database
    db.session.add(new_planet)
    db.session.commit()

    return make_response(f"Your planet, {new_planet.name}, has been created.", 201)


@planets_bp.route("", methods=["GET"])
def read_all_planets():
    """Get all planets or get planets with query params"""
    name_query = request.args.get("name")
    xenomorphs_query = request.args.get("xenomorphs")
    
    ##---partial functionality; would like to discuss---##
    if name_query:
        planets = Planet.query.filter_by(name=name_query)
    elif xenomorphs_query:
        planets = Planet.query.filter_by(xenomorphs=xenomorphs_query)
    ##---END---##
    else:
        planets = Planet.query.all()

    planets_response = []

    for planet in planets:
        planets_response.append(planet.to_json())

    return jsonify(planets_response)


@planets_bp.route("/<planet_id>", methods=["GET"])
def read_a_planet(planet_id):
    """Get planet with planet_id"""
    planet = get_planet(planet_id)
    return planet.to_json()

@planets_bp.route("/<planet_id>", methods=["PATCH"])
def update_a_planet(planet_id):
    """Update data for planet with planet_id in database"""
    request_body = request.get_json()
    planet = get_planet(planet_id)

    if "id" in request_body:
        planet.id = request_body["id"]
    if "name" in request_body:
        planet.name = request_body["name"]
    if "description" in request_body:
        planet.description = request_body["description"]
    if "xenomorphs" in request_body:
        planet.xenomorphs = request_body["xenomorphs"]

    db.session.commit()
    return make_response(f"Planet {planet.id} has been updated.", 201)


@planets_bp.route("/<planet_id>", methods=["DELETE"])
def delete_a_planet(planet_id):
    """Delete planet with planet_id in database"""
    planet = get_planet(planet_id)      

    db.session.delete(planet)
    db.session.commit()
    return make_response(f"Planet #{planet_id} successfully destroyed.", 200)