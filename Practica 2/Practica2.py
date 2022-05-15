# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

import numpy
import sklearn
from sklearn import linear_model, tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import export_graphviz, plot_tree
import graphviz
import Practica1
import json
import sqlite3
import pandas as pd
import plotly.graph_objects as go
import urllib
from subprocess import call


def sql_UsuariosCriticosGrafico(numero,porcentaje):
    df_ranking_vulnerable=Practica1.sql_UsuariosCriticos(numero)
    if(porcentaje==0):
        fig = go.Figure(
            data=[go.Table(header=dict(values=['Usuario','N de clicks', 'Emails recibidos','Porcentaje']),
                           cells=dict(values=[df_ranking_vulnerable['nombre'],df_ranking_vulnerable['clicados'], df_ranking_vulnerable['totales'], df_ranking_vulnerable['Porcentaje']]))]
        )
    else:
        if (porcentaje == 1):
            df_mask_menos50=df_ranking_vulnerable['Porcentaje']<0.50
            df_ranking_vulnerable = df_ranking_vulnerable[df_mask_menos50]

            fig = go.Figure(
                data=[go.Table(header=dict(values=['Usuario', 'N de clicks', 'Emails recibidos','Porcentaje']),
                               cells=dict(values=[df_ranking_vulnerable['nombre'], df_ranking_vulnerable['clicados'], df_ranking_vulnerable['totales'], df_ranking_vulnerable['Porcentaje']]))]
            )
        else:
            df_mask_mas50 = df_ranking_vulnerable['Porcentaje'] >0.50
            df_ranking_vulnerable = df_ranking_vulnerable[df_mask_mas50]

            fig = go.Figure(
                data=[go.Table(header=dict(values=['Usuario', 'N de clicks', 'Emails recibidos','Porcentaje']),
                               cells=dict(values=[df_ranking_vulnerable['nombre'], df_ranking_vulnerable['clicados'], df_ranking_vulnerable['totales'], df_ranking_vulnerable['Porcentaje']]))]
            )
    return fig


def sql_WebVulnerables(numero):
    #APARTADO: 2
    df_politicas=pd.DataFrame(conn.execute('SELECT web,cookies, aviso, proteccion_de_datos , creacion FROM Legal'), columns=['web','cookies','aviso','proteccion_de_datos','creacion'])
    df_politicas['politicas_actualizadas']=df_politicas['cookies']+df_politicas['aviso']+df_politicas['proteccion_de_datos']
    df_ranking_politicas = df_politicas.nsmallest(n=int(numero), columns=['politicas_actualizadas'])

    fig = go.Figure(
        data=[go.Table(header=dict(values=['Web', 'N Politicas desactualizadas']),
                       cells=dict(values=[df_ranking_politicas['web'], df_ranking_politicas['politicas_actualizadas']]))]

    )
    return fig


def sql_cve():
    url = "https://cve.circl.lu/api/last"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    lista = []
    for line in data:
        lista.append(line['id'])
    lista.sort(reverse=True)

    df_listaCVE = pd.DataFrame(lista, columns=['ID'])
    df_listaCVE = df_listaCVE.head(10)
    fig = go.Figure(
        data=[go.Table(header=dict(values=['TOP 10 ULTIMAS CVE']),
                       cells=dict(
                           values=[df_listaCVE['ID']]))]
    )
    return fig


def prediction_criticalUserLR():
    users_X = []
    users_y = []
    with open("users_IA_clases.json", 'r') as f:
        data = json.load(f)
        for line in data['usuarios']:
            total = line['emails_phishing_recibidos']
            clicado = line['emails_phishing_clicados']
            vulnerable=line['vulnerable']
            if total==0:
                total=0.01
            users_X.append([float(clicado)/float(total)])
            users_y.append(vulnerable)

    X_train=users_X[:-10]
    X_test=users_X[-10:]
    y_train=users_y[:-10]
    y_test=users_y[-10:]
    X_train, X_test, y_train, y_test = train_test_split(users_X, users_y, test_size=0.3, random_state=0)
    regr = linear_model.LinearRegression()
    regr.fit(X_train, y_train)
    Y_pred = regr.predict(X_test)

    resultado_y_pred=[]
    for i in range(0,len(Y_pred)):
        if(i>0.5):
            resultado_y_pred.append(1)
        else:
            resultado_y_pred.append(0)

    # Plot outputs
    plt.scatter(X_test, y_test, color="black")
    #m*x+b
    #m pendiente -> slope
    #b intercept
    plt.plot(numpy.array(regr.coef_)*numpy.array(X_test)+regr.intercept_,X_test, color="blue", linewidth=3)
    plt.xticks(())
    plt.yticks(())
    plt.savefig("static/ModeloRegresion.png")
    plt.show()
    with open('users_IA_predecir.json') as file:
        data = json.load(file)

    users_X_predict = []

    for line in data['usuarios']:
        total = line['emails_phishing_recibidos']
        clicado = line['emails_phishing_clicados']
        if total == 0:
            total = 0.01
        users_X_predict.append([float(clicado) / float(total)])

    users_y_predict = regr.predict(users_X_predict)
    vulnerables = 0
    noVulnerables = 0
    for i in range(len(users_y_predict)):
        if(users_y_predict[i] < 0.5):
            users_y_predict[i] = 0
            vulnerables += 1
        else:
            users_y_predict[i] = 1
            noVulnerables += 1

    print("Prediccion LR: ",vulnerables," vulnerables y ",noVulnerables," no vulnerables")
    return plt


def prediction_criticalUserRF():
    users_X = []
    users_y = []
    with open("users_IA_clases.json", 'r') as f:
        data = json.load(f)
        for line in data['usuarios']:
            total = line['emails_phishing_recibidos']
            clicado = line['emails_phishing_clicados']
            vulnerable = line['vulnerable']
            if total == 0:
                total = 0.01
            users_X.append([float(clicado) / float(total)])
            users_y.append(vulnerable)

    X_train = users_X[:-20]
    X_test = users_X[-20:]
    Y_train = users_y[:-20]
    Y_test = users_y[-20:]

    clf = RandomForestClassifier(max_depth=2, random_state=0, n_estimators=4)
    clf.fit(X_train, Y_train)

    for i in range(len(clf.estimators_)):
        fig, ax = plt.subplots(figsize=(12, 5))
        plot = plot_tree(
            decision_tree=clf.estimators_[i],
            feature_names=['clicados', 'recibidos'],
            class_names=['vulnerable', 'no vulnerable'],
            filled=True,
            impurity=False,
            fontsize=9,
            precision=4,
            ax=ax
        )
        plt.savefig("static/decisionTree" + str(i) + ".png")
        plt.show()

    users_X_predict = []
    for line in data['usuarios']:
        total = line['emails_phishing_recibidos']
        clicado = line['emails_phishing_clicados']
        if total == 0:
            total = 0.01
        users_X_predict.append([float(clicado) / float(total)])

    users_y_predict = clf.predict(users_X_predict)
    vulnerables = 0
    noVulnerables = 0
    for i in range(len(users_y_predict)):
        if(users_y_predict[i] < 0.5):
            users_y_predict[i] = 0
            vulnerables += 1
        else:
            users_y_predict[i] = 1
            noVulnerables += 1

    print("Prediccion RF: ",vulnerables," vulnerables y ",noVulnerables," no vulnerables")

def prediction_criticalUserDT():
    users_X = []
    users_y = []
    with open("users_IA_clases.json", 'r') as f:
        data = json.load(f)
        for line in data['usuarios']:
            total = line['emails_phishing_recibidos']
            clicado = line['emails_phishing_clicados']
            vulnerable = line['vulnerable']
            if total == 0:
                total = 0.01
            users_X.append([float(clicado) / float(total)])
            users_y.append(vulnerable)

    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(users_X, users_y)
    # Predict
    clf_model = tree.DecisionTreeClassifier()
    clf_model.fit(users_X, users_y)
    # Print plot
    dot_data = tree.export_graphviz(clf, out_file=None)
    graph = graphviz.Source(dot_data)
    graph.render("users")
    dot_data = tree.export_graphviz(clf,
                                    out_file=None,
                                    feature_names=["probabilidad de hacer click"],
                                    class_names=["vulnerable", "noVulnerable"],
                                    filled=True, rounded=True,
                                    special_characters=True)
    graph = graphviz.Source(dot_data)
    graph.render('test.gv', view=True).replace('\\', '/')

    users_X_predict = []

    for line in data['usuarios']:
        total = line['emails_phishing_recibidos']
        clicado = line['emails_phishing_clicados']
        if total == 0:
            total = 0.01
        users_X_predict.append([float(clicado) / float(total)])

    users_y_predict = clf_model.predict(users_X_predict)
    vulnerables = 0
    noVulnerables = 0
    for i in range(len(users_y_predict)):
        if(users_y_predict[i] < 0.5):
            users_y_predict[i] = 0
            vulnerables += 1
        else:
            users_y_predict[i] = 1
            noVulnerables += 1

    print("Prediccion DT: ",vulnerables," vulnerables y ",noVulnerables," no vulnerables")




conn = sqlite3.connect('example.db', check_same_thread=False)
prediction_criticalUserLR()
prediction_criticalUserRF()
prediction_criticalUserDT()