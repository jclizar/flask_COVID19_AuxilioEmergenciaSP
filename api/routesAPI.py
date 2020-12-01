from flask import Flask, render_template
from app import app #modulo do testeMondo.py
from api.modulesApi import API #da pasta api

@app.route("/api/municipio/<id_IBGE>", methods=['GET'])
def municipio(id_IBGE):
    return API().municipio_mes(id_IBGE)