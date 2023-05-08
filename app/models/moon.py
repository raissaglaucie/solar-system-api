from app import db

class Moon(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    size = db.Column(db.String)
    description = db.Column(db.String)
    color = db.Column(db.String)
    planet = db.relationship("Planet", back_populates="moons")  
    planet_id = db.Column(db.Integer, db.ForeignKey('Planets.id'), nullable=True)

    def to_dict(self):
        moon_dict = {
            "id": self.id,
            "size": self.size,
            "description": self.description,
            "color": self.color,
        }

        if self.planet_id:
            moon_dict["planet_id"] = self.planet_id

        return moon_dict

    @classmethod
    def from_dict(cls, planet_data):
        return cls(
            size=planet_data['size'],
            description=planet_data['description'],
            color=planet_data['color'],
        )