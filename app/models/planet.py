from app import db

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    diameter= db.Column(db.Float)
    moons = db.relationship("Moon", back_populates="planet", lazy=True)
    __tablename__ = "Planets"

    def to_dict(self, moons=False):
        planet_dict = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "diameter": self.diameter
        }

        if moons:
            planet_dict["moons"] = [moon.to_dict() for moon in self.moons]

        return planet_dict
    
    @classmethod
    def from_dict(cls, planet_data):
        return cls(
            name=planet_data['name'],
            description=planet_data['description'],
            diameter=planet_data['diameter']
        )