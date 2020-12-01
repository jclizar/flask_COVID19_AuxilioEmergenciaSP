
from flask import Flask, render_template, session, redirect
from functools import wraps
import pymongo
from os import environ
from myMap import buildMap
#from api.modulesApi import API

app = Flask(__name__)

app.secret_key = environ.get('SECRET_KEY')
#print(os.urandom(16))

#database - colocar no mongoDb Compass mongodb://127.0.0.1:27017/ (vc acha mongo.exe na pasta C:\Program Files\MongoDB\Server\4.4\bin)
#iniciar serviço ctrlshift+esc (ver se o mongo tá em execução)

client = pymongo.MongoClient(environ.get('CONNECTION_DB_URL'))
db = pymongo.database.Database(client, 'user_login_system')


#Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap

#Rotas
from user import routes
from api import routesAPI

@app.route("/menu/")
@login_required
def menu():
    #buildMap(db)
    return render_template('menu.html')

@app.route("/dados-municipio/")
def dadosMunicipio():
    #LISTA MUNICIPIOS
    municipios = list(db.beneficioDataAPI.find())
   
    return render_template('dadosMunicipio.html', municipios = municipios)

@app.route("/sobre/")
def sobre():
    return render_template('sobreEquipe.html')

@app.route("/fale-conosco/")
def faleConosco():
    return render_template('faleConosco.html')

@app.route("/database/")
def database():
    return render_template('tabelas.html')

@app.route("/configuracao/")
def configuracao():
    return render_template('configuracao.html')

#-----------------------------------------------------------#

@app.route("/") 
def home():
    return render_template('login.html')

@app.route("/cadastro/")
def cadastro():
    return render_template('cadastro.html')


@app.route("/esqueci-senha/")
def esqueciSenha():
    return render_template('esqueciSenha.html')


if __name__ == "__main__":
    app.run(debug=True)# debug = True permiete alterações sem ter que restartar o servidor




