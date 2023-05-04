from app import db


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    diameter= db.Column(db.Float)
    __tablename__ = "Planets"


    @classmethod
    def from_dict(cls, data_dict):
        return cls(
        name=data_dict["name"],
        description=data_dict["description"],
        diameter=data_dict["diameter"]
        )
    

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "diameter": self.diameter
        }