from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship
from sql_alchemy import db, app

class Usuario(db.Model):
    __tablename__ = 'Usuarios'

    Id_usuario = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    espaco = db.Column(db.BigInteger, nullable=False)
    plano = db.Column(db.Integer, nullable=False)
    numero_de_arquivos = db.Column(db.Integer, nullable=False)
    arquivos = relationship("Arquivo")

    def to_json(self):
        return {
            'Id_usuario': self.Id_usuario,
            'email': self.email,
            'nome': self.nome,
            'idade': self.idade,
            'espaco': self.espaco,
            'plano': self.plano,
            'numero_de_arquivos': self.numero_de_arquivos,
        }

    with app.app_context():
        db.create_all()


   
