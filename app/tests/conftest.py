import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.planet import Planet



@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def two_saved_planets(app):
    # Arrange
    mercury_planet = Planet(name="Mercury",
                            description="smallest planet",
                            diameter=3031.9)
    jupiter_planet = Planet(name="Jupiter",
                            description="biggest planet",
                            diameter=86881)

    db.session.add_all([mercury_planet, jupiter_planet])
    db.session.commit()

    return [mercury_planet, jupiter_planet]



@pytest.fixture
def one_saved_planet(app):
    planet = Planet(name="Uranus", 
                    description="furthest planet", 
                    diameter=31518 )
    db.session.add(planet)
    db.session.commit()
    return planet


