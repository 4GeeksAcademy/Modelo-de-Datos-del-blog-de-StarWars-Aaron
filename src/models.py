from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Float, Date, ForeignKey, Table, Column, Text
from datetime import date

db = SQLAlchemy()

user_character = Table(
    'user_character',
    db.Model.metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('character_id', ForeignKey('character.id'), primary_key=True)
)

user_planet = Table(
    'user_planet',
    db.Model.metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('planet_id', ForeignKey('planet.id'), primary_key=True)
)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(String(120), nullable=False)
    apellido = db.Column(String(120), nullable=False)
    email = db.Column(String(120), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    fecha_suscripcion = db.Column(Date(), nullable=False, default=date.today)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    favoritos_personajes = db.relationship(
        'Character',
        secondary=user_character,
        back_populates='usuarios_favoritos'
    )

    favoritos_planetas = db.relationship(
        'Planet',
        secondary=user_planet,
        back_populates='usuarios_favoritos'
    )

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "fecha_suscripcion": self.fecha_suscripcion.isoformat() if self.fecha_suscripcion else None,
            "is_active": self.is_active,
            "favoritos_personajes": [c.serialize() for c in self.favoritos_personajes],
            "favoritos_planetas": [p.serialize() for p in self.favoritos_planetas]
        }


class Planet(db.Model):
    __tablename__ = 'planet'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(String(120), nullable=False)
    diametro = db.Column(Float(), nullable=False)
    clima = db.Column(String(120), nullable=False)
    gravedad = db.Column(Float(), nullable=False)
    descripcion = db.Column(Text(), nullable=False)

    personajes = db.relationship('Character', back_populates='planeta_origen')

    usuarios_favoritos = db.relationship(
        'User',
        secondary=user_planet,
        back_populates='favoritos_planetas'
    )

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "diametro": self.diametro,
            "clima": self.clima,
            "gravedad": self.gravedad,
            "descripcion": self.descripcion,
            "personajes": [p.serialize() for p in self.personajes]
        }


class Character(db.Model):
    __tablename__ = 'character'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(String(120), nullable=False)
    altura = db.Column(Float(), nullable=False)
    peso = db.Column(Float(), nullable=False)
    color_pelo = db.Column(String(50), nullable=False)
    color_ojos = db.Column(String(50), nullable=False)

    planeta_origen_id = db.Column(ForeignKey('planet.id'), nullable=False)
    planeta_origen = db.relationship('Planet', back_populates='personajes')

    usuarios_favoritos = db.relationship(
        'User',
        secondary=user_character,
        back_populates='favoritos_personajes'
    )

    def serialize(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "altura": self.altura,
            "peso": self.peso,
            "color_pelo": self.color_pelo,
            "color_ojos": self.color_ojos,
            "planeta_origen_id": self.planeta_origen_id,
            "planeta_origen": self.planeta_origen.serialize() if self.planeta_origen else None
        }
