from flask import Flask, jsonify, request, session, redirect, send_file
from bson.json_util import dumps
from passlib.hash import pbkdf2_sha256
import uuid
from app import db

import smtplib
from email.mime.text import MIMEText

import json
import os


class User:
                                    
    def start_session(self, user):
        del user['password']
        session['logged_in']=True
        session['user']=user
        return jsonify(user), 200

    def signup(self):
        #print(request.form)

        #create user object
        user={
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "type": "user",
            "ativo": True,
            "email": request.form.get('email'),
            "password": request.form.get('password'), 
        }

        if request.form.get('confirm_password') != user['password']:
            return jsonify({"error" : "Senhas diferentes!"}),400
            
        # Encriptar password
        user['password'] = pbkdf2_sha256.encrypt(user['password'])

        #Check existing email
        if db.users.find_one({"email": user['email']}):
            return jsonify({"error" : "Email cadastrado!"}),400

        if db.users.insert_one(user):#users nome da tabela
            return  self.start_session(user)#jsonify(user),200

        return jsonify({"error": "Falha ao logar"}),400 #200 certo, 400 deu errado

    def signout(self):
        session.clear()
        return redirect('/')

    def login(self):
        user = db.users.find_one({
            "email": request.form.get('email'),
            "ativo": True
        })

        #check password verifica se o encrepitado == decrepitado
       
        if user != None:
            check_password = pbkdf2_sha256.verify(request.form.get('password'), user['password'])
        

        if user and check_password:
            return self.start_session(user)
        
        return jsonify({"error": "Login inválido"}), 401
 
    def mail(self, msg, EMAIL_SUBJECT, user_email, n):
        #https://blog.mailtrap.io/send-emails-with-gmail-api/
        #https://learndataanalysis.org/how-to-use-gmail-api-to-send-an-email-in-python/
        #

        SMTP_SERVER = "smtp.mail.yahoo.com"
        SMTP_PORT = 587
        SMTP_USERNAME = os.environ.get('USER_EMAIL')
        SMTP_PASSWORD = os.environ.get('PASSWORD_EMAIL')

         #EMAIL_SUBJECT = "Redefinir senha"

        if n == 0: #fale-conosco
            EMAIL_FROM = SMTP_USERNAME
            EMAIL_TO = SMTP_USERNAME

        else: #Reeviar senha
            EMAIL_FROM = SMTP_USERNAME
            EMAIL_TO = user_email

        template = f'''
            <html>
            <head></head>
            <body>
                <p>{msg}</p>
            </body>
            </html>'''
        
        msg = MIMEText(msg, 'html')
        msg['Subject'] = EMAIL_SUBJECT
        msg['From'] = EMAIL_FROM 
        msg['To'] = EMAIL_TO
        debuglevel = True

        mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        mail.set_debuglevel(debuglevel)
        mail.starttls()
        mail.login(SMTP_USERNAME, SMTP_PASSWORD)
        mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        mail.quit()

        
    def esqueciSenha(self):
        user = db.users.find_one({
            "email": request.form.get('email')
        })

        if user == None:
            return jsonify({"msg": "Email não cadastrado"}), 500
        else:
            msg=f'''Olá {user['name']}!<br><br>
                    Clique no link abaixo para redefinir sua senha:<br>
                    <a href="http://127.0.0.1:80/nova-senha/{user['_id']}">Link para redefinir senha</a>'''

            self.mail(msg, 'Redefinir senha', user['email'],1)

        return jsonify({"msg": "As instruções para recuperar sua senha foram enviadas"}), 200

    def configSave(self):
        if (request.form.get('password') == "" or request.form.get('confirm_password') == "" or request.form.get('name') == ""):
            return jsonify({"msg" : "Campos inválido!"}),400            

        if(request.form.get('password') == request.form.get('confirm_password')):
            updated_user = {
                'name': request.form.get('name'),
                'password': request.form.get('password'),
            }

            updated_user['password'] = pbkdf2_sha256.encrypt(updated_user['password'])
            myquery = {'_id': session['user']['_id']}
            update_data_user = { '$set': updated_user}
            result = db.users.update_one(myquery, update_data_user)


            if result.modified_count == 0:
                return jsonify({"msg" : "Erro ao atualizar o usuário!"}),400
            else:
                user = db.users.find_one({
                    "_id": session['user']['_id']
                })
                self.start_session(user)
                return jsonify({"msg" : "Usuário atualizado com sucesso!"}),200

        else:
            return jsonify({"msg" : "Senhas diferentes!"}),400

        

    def configDelete(self):   
        result = db.users.delete_one({
            "_id": session['user']['_id']
        })

        if result.deleted_count != 0:
            return jsonify({}), 200
        else:
            return jsonify({"error":"Erro ao deletar usuário"}), 500

    def novaSenha(self):
        if(request.form.get('password') == request.form.get('confirm_password')):

            updated_user = {
                'password': request.form.get('password'),
            }

            updated_user['password'] = pbkdf2_sha256.encrypt(updated_user['password'])

            myquery = {'_id': request.form.get('user_id')}

            update_data_user = { '$set': updated_user}
            
            result = db.users.update_one(myquery, update_data_user)

            if result.modified_count == 0:
                return jsonify({"error" : "Erro ao atualizar a senha!"}),400
            else:
                user = db.users.find_one(myquery)
                self.start_session(user)
                return jsonify({}),200
        else:
            return jsonify({"error" : "Senhas diferentes!"}),400

    def faleConosco(self):
        
        email_msg = request.form.get('mensagem')
        assunto = request.form.get('assunto')

        msg = f'''<strong>DADOS USER:</strong><br><br>
        Name: {session['user']['name']}<br>
        Email: {session['user']['email']}<br><br>
        
        <strong>MENSAGEM:</strong><br><br>
        {email_msg}
        '''
        
        self.mail(msg, assunto, session['user']['email'], 0)

        return jsonify({"msg" : "Mensagem enviada com sucesso!"}),200

    def tabelaUser(self):
        search = request.args.get('search')
        limit = int(request.args.get('limit'))
        offset = int(request.args.get('offset'))

        # a query vai buscar por usuários que tenha o valor search para os campos name, email e type e que estejam ativos 
        query = { 
                    '$or': [ 
                        {'name' : {'$regex' : search}},
                        {'email' : {'$regex' : search}}, 
                        {'type' : {'$regex' : search}}                           
                    ]
                } 

        # executa a query limitando a quantidade  e retornando apartir de um número de resultado
        users = db.users.find(query).limit(limit).skip(offset)

        response_bootstrap_table = {
                                        'rows': list(users), 
                                        'total': users.count()
                                    }
        
        return jsonify(response_bootstrap_table),200
    
    def tornarAdmin(self):
        myquery = {'_id': request.form.get('user_id')}

        updated_user = {
            'type': request.form.get('tipo'),
        }

        update_data_user = { '$set': updated_user}

        result = db.users.update_one(myquery, update_data_user)

        if result.modified_count == 0:
            return jsonify({"msg" : "Erro ao atualizar o usuário!"}),400
        else:
            return jsonify({"msg" : "Usuário atualizado com sucesso!"}),200

    def desativar(self):
        myquery = {'_id': request.form.get('user_id')}

        ativo = True if request.form.get('ativo') == 'true' else False

        updated_user = {
            'ativo': ativo,
        }

        update_data_user = { '$set': updated_user}

        result = db.users.update_one(myquery, update_data_user)

        if result.modified_count == 0:
            return jsonify({"msg" : "Erro ao desativar o usuário!"}),400
        else:
            return jsonify({"msg" : "Usuário desativado com sucesso!"}),200

    
    def export(self, colecao):

        data_collection= db[colecao]
        documents = data_collection.find()

        if(documents != None):
            response = []
            for document in documents:
                response.append(document)

            filename=colecao+'.json'

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(response, f, ensure_ascii=False, indent=4)
            
        
            return jsonify({"filename": filename }),200
        else:
            return jsonify({"msg": "Falha ao exportar os dados" }),500











        