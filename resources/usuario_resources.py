from flask import Flask, Response, request, jsonify
import json
from models import usuario
from sql_alchemy import app, db

Usuario = usuario.Usuario

# Selecionar Tudo

@app.route("/usuarios", methods=["GET"])
def seleciona_usuarios():
    usuario_objetos = Usuario.query.all()

    usuarios_json = [usuario.to_json() for usuario in usuario_objetos]

    return gera_response(200, "usuarios", usuarios_json)

# Selecionar Individual
@app.route("/usuario/<int:Id_usuario>", methods=["GET"])
def seleciona_usuario(Id_usuario):
    usuario_objeto = Usuario.query.filter_by(Id_usuario=Id_usuario).first()

    if Id_usuario == usuario_objeto.Id_usuario:
        usuario_json = usuario_objeto.to_json()
    else:
        return gera_response(250, "usuario", {}, "Usuario não encontrado")

    return gera_response(200, "usuario", usuario_json)

# Cadastrar
@app.route("/usuario", methods=["POST"])
def cria_usuario():
    body = request.get_json()

    try:
        usuario = Usuario(email=body["email"], nome = body["nome"], idade = body["idade"], \
        espaco=body["espaco"], plano=body["plano"], numero_de_arquivos= body["numero_de_arquivos"]
        )
        db.session.add(usuario)
        db.session.commit()
        return gera_response(201, "usuario", usuario.to_json(), "Criado com sucesso")
    except Exception as e:
        db.session.rollback()
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao cadastrar")

# Atualizar
@app.route("/usuario/<int:Id_usuario>", methods=["PUT"])
def atualiza_usuario(Id_usuario):

    usuario_objeto = Usuario.query.filter_by(Id_usuario=Id_usuario).first()
    body = request.get_json()

    try:
        if ('email' in body):
            usuario_objeto.email = body['email']
        else:
            return gera_response(422, "email", {}, "Erro ao atualizar")

        if('nome' in body):
            usuario_objeto.nome = body['nome']
        else:
            return gera_response(422, "nome", {}, "Erro ao atualizar")

        if ('idade' in body):
            usuario_objeto.idade = body['idade']
        else:
            return gera_response(422, "idade", {}, "Erro ao atualizar")

        if ('espaco' in body):
            usuario_objeto.plano = body['espaco']
        else:
            return gera_response(422, "espaco", {}, "Erro ao atualizar")

        if ('plano' in body):
            usuario_objeto.plano = body['plano']
        else:
            return gera_response(422, "plano", {}, "Erro ao atualizar")

        if ('numero_de_arquivos' in body):
            usuario_objeto.numero_de_arquivos = body['numero_de_arquivos']
        else:
            return gera_response(422, "numero de arquivos", {}, "Erro ao atualizar")
        db.session.add(usuario_objeto)
        db.session.commit()
        return gera_response(200, "usuario", usuario_objeto.to_json(), "Atualizado com sucesso")
    except Exception as e:
        db.session.rollback()
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao atualizar")

# Deletar
@app.route("/usuario/<int:Id_usuario>", methods=["DELETE"])
def deleta_usuario(Id_usuario):
    usuario_objeto = Usuario.query.filter_by(Id_usuario=Id_usuario).first()
    try:
        db.session.delete(usuario_objeto)
        db.session.commit()
        return gera_response(200, "usuario", usuario_objeto.to_json(), "Deletado com sucesso")
    except Exception as e:
        db.session.rollback()
        print('Erro', e)
        return gera_response(400, "usuario", {}, "Erro ao deletar")

def gera_response(status, nome_do_conteudo, conteudo, mensagem=False):
    body = {}
    body[nome_do_conteudo] = conteudo

    if(mensagem):
        body["mensagem"] = mensagem

    return Response(json.dumps(body), status=status, mimetype="application/json")


