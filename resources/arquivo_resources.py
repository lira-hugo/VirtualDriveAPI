from flask import Flask, Response, request
from werkzeug import secure_filename
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json
from models import arquivo, usuario
from sql_alchemy import app, db
from GoogleCloud_Storage import googlecloud as gcs
from GoogleCloud_Storage import config as gcsc
from pathlib import Path
from google.cloud import storage

Arquivo = arquivo.Arquivo
# Selecionar Tudo
@app.route("/arquivos", methods=["GET"])
def seleciona_arquivos():
    arquivos_objetos = Arquivo.query.all()

    arquivos_json = [arquivo.to_json() for arquivo in arquivos_objetos]

    return gera_response(200, "arquivos", arquivos_json)

# Selecionar Individual
@app.route("/arquivo/<int:Id_arquivo>", methods=["GET"])
def seleciona_arquivo(Id_arquivo):
    arquivo_objeto = Arquivo.query.filter_by(Id_arquivo=Id_arquivo).first()
    if Id_arquivo == Arquivo.Id_usuario:
        arquivo_json = arquivo_objeto.to_json()
        bucketFolder = input('Digite o bucketFolder e arquivo a ser baixado:')
        gcs.download_file(gcs.download_file(gcs.bucketName, bucketFolder))
    else:
        return gera_response(400, "Erro ao cadastrar")

    return gera_response(200, "arquivo", arquivo_json)

# Cadastrar
@app.route("/arquivo/usuario/<int:Id_usuario>", methods=["POST"])
def cria_arquivo(Id_usuario):

    filename = '/home/sonny/Documentos/NExT/ExperienciadeTrabalho/files/sample_text.txt'

    sz = Path(filename).stat().st_size

    print(sz)

    try:
        usuario_objeto = usuario.Usuario.query.filter_by(Id_usuario=Id_usuario).first()
        if(usuario_objeto == None):
            return gera_response(422, "usuario", Id_usuario, "não encontrado")

        usuario_objeto.numero_de_arquivos += 1

        body = request.get_json()
        arquivo = Arquivo(nome=body["nome"], tamanho= body["tamanho"], tipo = body["tipo"])
        arquivo.tamanho += sz
        arquivo.Id_usuario = Id_usuario
        db.session.add(arquivo)
        db.session.add(usuario_objeto)
        db.session.commit()
        filename = input('Digite o nome do arquivo a ser enviado: ')
        gcs.upload_files(gcs.bucketName, filename)

        return gera_response(201, "arquivo", arquivo.to_json(), "Criado com sucesso")
    except Exception as e:
        db.session.rollback()
        print('Erro', e)
        return gera_response(400, "arquivo", {}, "Erro ao cadastrar")


# Deletar
@app.route("/arquivo/<int:Id_arquivo>/<int:Id_usuario>", methods=["DELETE"])
def deleta_arquivo(Id_arquivo, Id_usuario):

    try:
        arquivo_objeto = Arquivo.query.filter_by(Id_arquivo=Id_arquivo).first()
        usuario_objeto = usuario.Usuario.query.filter_by(Id_usuario=Id_usuario).first()
        usuario_objeto.numero_de_arquivos -= 1

        #arquivo_objeto -= sz tamanho do arquivo de deletado na nuvem
        #fileName = input('Digite o nome do arquivo a ser deletado: ')


        client = storage.Client()
        bucket = client.get_bucket(gcs.bucketName)
        path = 'gs://turma_mtres2022_2_next/'
        fileName = path + arquivo_objeto.name

        blob = bucket.blob(fileName)
        print(len(blob.download_as_string().decode()))
        print(blob.size)

        gcs.delete_file(gcs.bucketName, fileName)
        db.session.delete(usuario_objeto)
        db.session.delete(arquivo_objeto)
        db.session.commit()

        return gera_response(200, "usuario", arquivo_objeto.to_json(), "Deletado com sucesso")
    except Exception as e:
        db.session.rollback()
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao deletar")


#Upload de arquivo
#@app.route('/uploader', methods = ['GET', 'POST'])
#def upload_file():
#  if request.method == 'POST':
#     f = request.files['file']
#     f.save(secure_filename(f.filename))
#     return 'file uploaded successfully'

def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")


