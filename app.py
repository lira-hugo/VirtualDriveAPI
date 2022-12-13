from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from models import usuario as vdm
from sql_alchemy import app
from models import usuario as usr
from models import arquivo as arq
from resources import usuario_resources as vdru
from resources import arquivo_resources as vdra
import mysql.connector
import json

#Usuario
usr.Usuario
vdru.seleciona_usuarios
vdru.seleciona_usuario
vdru.cria_usuario
vdru.atualiza_usuario
vdru.deleta_usuario

#Arquivos
arq.Arquivo
vdra.seleciona_arquivos
vdra.seleciona_arquivo
vdra.cria_arquivo
vdra.deleta_arquivo

app.run()