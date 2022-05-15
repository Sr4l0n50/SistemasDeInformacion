# -*- coding: utf-8 -*-

import sqlite3
import hashlib
from flask import Flask, g
from flask import render_template
from flask import request
from matplotlib import pyplot as plt
import Practica1, Practica2
import json
from plotly.graph_objects import Bar, Figure
import plotly
import mpld3

app = Flask(__name__)

DATABASE = './example.db' #Ruta de la base de datos
session=0 #Variable global para el login

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


@app.route('/')
def inicio():
    return render_template('Inicio.html')

@app.route('/login',methods=['POST'])
def login():
    if request.method == 'POST':
        req = request.get_json()
        Usuario = req['User']
        Pass = req['Pass']
        Pass = hashlib.md5(Pass.encode())
        user = query_db('select * from usuario where nombre = ? AND contrasena= ?',[Usuario, Pass.hexdigest()], one=True)
        if user is None:
            return "0"
        else:
            global session
            session=1
        return "1"

@app.route('/UsuariosCriticos',methods=['POST', 'GET'])
def UsuariosCriticos():
    if session==1:
        if request.method=='POST':
            req = request.get_json()
            numero=req['numeroUsuarios']
            porcentaje=req['porcentajeUsuarios']
            fig = Practica2.sql_UsuariosCriticosGrafico(numero,int(porcentaje))
            fig.update_layout(
                autosize=False,
                width=1000,
                height=1000,
            )
            fig.update_yaxes(automargin=True)
            a = plotly.utils.PlotlyJSONEncoder
            image = json.dumps(fig, cls=a)
            return image
    else:
        return "0"

@app.route('/WebVulnerables',methods=['POST','GET'])
def WebVulnerables():
    if session==1:
        if request.method=='POST':
            req = request.get_json()
            numero = req['Webs']
            fig = Practica2.sql_WebVulnerables(numero)
            fig.update_layout(
                autosize=False,
                width=1000,
                height=1000,
            )
            fig.update_yaxes(automargin=True)
            a = plotly.utils.PlotlyJSONEncoder
            graphJSON = json.dumps(fig, cls=a)
            return graphJSON
    else:
            return "0"


@app.route('/CVEs',methods=['POST'])
def sql_cve():
    if session==1:
            fig=Practica2.sql_cve();
            fig.update_layout(
                autosize=False,
                width=1000,
                height=1000,
            )
            fig.update_yaxes(automargin=True)
            a = plotly.utils.PlotlyJSONEncoder
            graphJSON = json.dumps(fig, cls=a)
            return graphJSON
    else:
            return "0"

@app.route('/Meto2',methods=['GET','POST'])
def Meto2():
    if session == 1:
        if request.method == 'POST':
            req = request.get_json()
            Tipo=req['tipo']
            if Tipo=='Lineal Regresion':
                fig=Practica2.prediction_criticalUserLR()
                fig.savefig('/static/plot2.png')
                a = plotly.utils.PlotlyJSONEncoder
                graphJSON = json.dumps(fig, cls=a)
                return graphJSON
            elif Tipo=='Random Forest':
                Practica2.prediction_criticalUserRF()
            else:
                Practica2.prediction_criticalUserDT()
        else:
            return render_template('Metodos.html')
    else:
        return "0"

if __name__ == '__main__':
    conn = sqlite3.connect('example.db', check_same_thread=False)
    app.run(debug=True)
