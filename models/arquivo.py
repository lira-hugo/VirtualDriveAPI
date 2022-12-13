from sql_alchemy import db, app
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, Table

class Arquivo(db.Model):
    __tablename__ = 'Arquivos'

    Id_arquivo = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(100), nullable=False)
    tamanho = db.Column(db.BigInteger, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    Id_usuario  = db.Column(db.Integer, db.ForeignKey('Usuarios.Id_usuario'), nullable=False)

    def to_json(self):
        return {
            'Id_arquivo': self.Id_arquivo,
            'nome': self.nome,
            'tamanho': self.tamanho,
            'tipo': self.tipo,
            'Id_usuario': self.Id_usuario            
        }

    with app.app_context():
        db.create_all()