from flask import Flask, render_template, send_from_directory,send_file,current_app
from app import app #modulo do testeMondo.py
from user.modules import User #da pasta user, na subpasta model import Class User
import os

@app.route("/user/signup/", methods=['POST'])
def signup():
    return User().signup()

@app.route('/user/signout/')
def signout():
    return User().signout()

@app.route('/user/login/', methods=['POST'])
def login():
    return User().login()

@app.route('/user/esqueciSenha/', methods=['POST'])
def esqueciSenhaUser():
    return User().esqueciSenha()


@app.route('/user/configSave/', methods=['PUT'])
def configSaveUser():
    return User().configSave()

@app.route('/user/configDelete/', methods=['DELETE'])
def configDeleteUser():
    return User().configDelete()


@app.route("/nova-senha/<user_id>", methods=['GET'])
def novaSenha(user_id):
    return render_template('novaSenha.html')


@app.route('/user/nova-senha/', methods=['POST'])
def novaSenhaUser():
    return User().novaSenha()


@app.route('/user/fale-conosco/', methods=['POST'])
def faleConoscoUser():
    return User().faleConosco()

@app.route('/user/tabela-user/', methods=['GET'])
def tableUsuario():
    return User().tabelaUser()

@app.route('/user/tornar-admin/', methods=['PUT'])
def tornarAdmin():
    return User().tornarAdmin()

@app.route('/user/desativar/', methods=['PUT'])
def desativarUser():
    return User().desativar()

@app.route('/user/exporta-colecao/<colecao>', methods=['GET'])
def exportCollection(colecao):
    return User().export(colecao)


'''@app.route('/<filename>')
def return_file(filename):
    print('--------------------------------------------------',filename)
    #return send_file(os.getcwd(),attachment_filename=filename)#as_attachment=True
    send_file(filename,as_attachment=True)'''

@app.route('/download-file/<filename>')
def return_file(filename):
    return send_file(filename,as_attachment=True)