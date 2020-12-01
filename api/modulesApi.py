from flask import Flask, jsonify, request, session, redirect
from passlib.hash import pbkdf2_sha256
import uuid

from app import db

import requests as req
import json

import numpy as np

#from user.modules import User

class API:
    '''def insertData(self):
        #create user object
        municipio={
            "_id": uuid.uuid4().hex,
            "name": request.form.get('name'),
            "type": "user",
            "email": request.form.get('email'),
            "password": request.form.get('password'), 
        }

        if db.beneficioDataAPI.insert_one(municipio):#users nome da tabela
            return jsonify(municipio),200
        else:
            return jsonify({"error": "Falha ao logar"}),400 #200 certo, 400 deu errado'''


    '''def todos_municiopios(self):
      return  list(db.beneficioDataAPI.find())'''
    
    def municipio_mes(self, id_IBGE):

        query = {
            '_id': int(id_IBGE)
        }


        municipio = db.beneficioDataAPI.find_one(query)

        if municipio != None:
            lista_muni=[]
            for mes in municipio['mesRef']:
                lista_muni.append(municipio['mesRef'][mes]['quantidadeBeneficiados'])
            
            
            media = np.mean([i for i in lista_muni if i != 0])
                
            return jsonify({'beneficiados_por_mes': lista_muni,'media_beneficiados': [ media, municipio['populacao']-media]}),200
        else:
            return jsonify({'beneficiados_por_mes': [0,0],'media_beneficiados': [0,0]}),400

