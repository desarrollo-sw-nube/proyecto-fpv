from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


db = SQLAlchemy()


class AppUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = AppUser
        include_relationships = True
        load_instance = True
