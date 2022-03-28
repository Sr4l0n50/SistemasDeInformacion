import hashlib
import json
import sqlite3
import pandas as pd
import altair as alt



def sql_create_table_user(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS Usuario (nombre text, telefono int, contrasena text, provincia text, permisos int, total int," 
                  "phishing int, clicados int)")
    conn.execute("CREATE TABLE IF NOT EXISTS Fechas (id int, usuario text, fecha text )")
    conn.execute("CREATE TABLE IF NOT EXISTS IPS (id int,usuario text, ip text )")
    conn.commit()

def sql_delete_table_user(conn):
    conn.execute('drop table if exists Usuario')
    conn.execute('drop table if exists Fechas')
    conn.execute('drop table if exists IPS')
    conn.commit()


def sql_create_table_legal(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS Legal (web text, cookies int, aviso int, proteccion_de_datos int, creacion int)")
    conn.commit()


def sql_delete_table_legal(conn):
    conn.execute('drop table if exists Legal')
    conn.commit()


def sql_introducir_datos_user(conn):
    idFecha=0
    idIPS=0
    with open("users.json",'r') as f:
        data = json.load(f)
        for line in data['usuarios']:
            name=list(line.keys())[0]
            telefono=line[name]['telefono']
            contrasena = line[name]['contrasena']
            provincia = line[name]['provincia']
            permisos = line[name]['permisos']
            phishing=line[name]['emails']['phishing']
            total = line[name]['emails']['total']
            clicado = line[name]['emails']['cliclados']
            fechas=line[name]['fechas']
            for linea in fechas:
                conn.execute("INSERT INTO Fechas (id, usuario, fecha)VALUES (?, ?, ?)",(idFecha, name, linea))
                idFecha+=1
            ips = line[name]['ips']
            for linea in ips:
                conn.execute("INSERT INTO IPS (id, usuario, ip)VALUES (?, ?, ?)", (idIPS, name, linea))
                idIPS+=1
            conn.execute("INSERT INTO Usuario (nombre, telefono, contrasena,provincia, permisos, total, phishing, clicados)"
                         "VALUES (?, ?, ?,?, ?, ?, ?, ?)",(name, telefono, contrasena,provincia, permisos, total, phishing, clicado))
    conn.commit()

def sql_introducir_datos_legal(conn):

    with open("legal.json",'r') as f:
        data = json.load(f)
        for line in data['legal']:
            web=list(line.keys())[0]
            cookies=line[web]['cookies']
            aviso = line[web]['aviso']
            proteccion_de_datos = line[web]['proteccion_de_datos']
            creacion = line[web]['creacion']

            conn.execute("INSERT INTO Legal (web, cookies, aviso, proteccion_de_datos, creacion)"
                 "VALUES (?, ?, ?,?, ?)", (web, cookies, aviso, proteccion_de_datos, creacion))
    conn.commit()

def sql_dataframes(conn):
    df_muestras=pd.DataFrame(conn.execute('SELECT * FROM Usuario'))
    df_fechas=pd.DataFrame(conn.execute('SELECT  count(fecha) FROM Fechas GROUP BY usuario'), columns=['numeroFechas'])
    df_ips = pd.DataFrame(conn.execute('SELECT  count(ip) FROM IPS GROUP BY usuario'), columns=['numeroIPS'])
    df_emails =pd.DataFrame(conn.execute('SELECT  total FROM Usuario'), columns=['emailsRecibidos'])


    df_fecha2=pd.DataFrame()
    df_ips2=pd.DataFrame()
    df_emails2=pd.DataFrame()

    df_muestra2=pd.DataFrame(columns=['cantidad'])
    df_muestra2.loc['muestras']={'cantidad':len(df_muestras)}


    df_fecha2['MinFechas'] = df_fechas.min()
    df_fecha2['MaxFechas'] = df_fechas.max()
    df_fecha2['MediaFechas'] = df_fechas.mean()
    df_fecha2['DesviacionFechas'] = df_fechas.std()

    df_emails2['MinEmails'] = df_emails.min()
    df_emails2['MaxEmails'] = df_emails.max()
    df_emails2['MediaEmails'] = df_emails.mean()
    df_emails2['DesviacionEmails'] = df_emails.std()

    df_ips2['MediaIPS'] = df_ips.mean()
    df_ips2['DesviacionIPS'] = df_ips.std()

    print("####### EJERCICIO 2 ####### ")
    print(df_muestra2)
    print(df_fecha2)
    print(df_ips2)
    print(df_emails2)
    print("####### FIN EJERCICIO 2 #######\n\n ")
    conn.commit()

def sql_permisos(conn):

    df_usuario = pd.DataFrame(
        conn.execute('SELECT permisos,total,phishing FROM Usuario WHERE permisos=0 '),
        columns=['permisos', 'totales', 'phishing'])
    df_administrador = pd.DataFrame(
        conn.execute('SELECT permisos,total,phishing FROM Usuario WHERE permisos=1'),
        columns=['permisos', 'totales', 'phishing'])
    df_agrupUsuario = pd.DataFrame()
    df_agrupUsuario['NumObservaciones<200'] = df_usuario[df_usuario['totales'] < 200].sum()
    df_agrupUsuario['Min<200'] = df_usuario[df_usuario['totales'] < 200].min()
    df_agrupUsuario['Max<200'] = df_usuario[df_usuario['totales'] < 200].max()
    df_agrupUsuario['Ausentes<200'] = df_usuario[df_usuario['phishing'] == 0].count()
    df_agrupUsuario['Media<200'] = df_usuario[df_usuario['totales'] < 200].mean()
    df_agrupUsuario['Mediana<200'] = df_usuario[df_usuario['totales'] < 200].mean()
    df_agrupUsuario['Varianza<200'] = df_usuario[df_usuario['totales'] < 200].std()
    df_agrupUsuario['NumObservaciones>200'] = df_usuario[df_usuario['totales'] < 200].sum()
    df_agrupUsuario['Min>200'] = df_usuario[df_usuario['totales'] > 200].min()
    df_agrupUsuario['Max>200'] = df_usuario[df_usuario['totales'] > 200].max()
    df_agrupUsuario['Ausentes>200'] = df_usuario[df_usuario['phishing'] > 200].count()
    df_agrupUsuario['Media>200'] = df_usuario[df_usuario['totales'] > 200].mean()
    df_agrupUsuario['Mediana>200'] = df_usuario[df_usuario['totales'] > 200].mean()
    df_agrupUsuario['Varianza>200'] = df_usuario[df_usuario['totales'] > 200].std()
    df_agrupUsuario = df_agrupUsuario.drop(['permisos','totales'], axis=0)

    df_agrupAdmin = pd.DataFrame()
    df_agrupAdmin['NumObservaciones<200'] = df_administrador[df_administrador['totales'] < 200].sum()
    df_agrupAdmin['Min<200'] = df_administrador[df_administrador['totales'] < 200].min()
    df_agrupAdmin['Max<200'] = df_administrador[df_administrador['totales'] < 200].max()
    df_agrupAdmin['Ausentes<200'] = df_administrador[df_administrador['phishing'] == 0].count()
    df_agrupAdmin['Media<200'] = df_administrador[df_administrador['totales'] < 200].mean()
    df_agrupAdmin['Mediana<200'] = df_administrador[df_administrador['totales'] < 200].mean()
    df_agrupAdmin['Varianza<200'] = df_administrador[df_administrador['totales'] < 200].std()
    df_agrupAdmin['NumObservaciones>200'] = df_administrador[df_administrador['totales'] < 200].sum()
    df_agrupAdmin['Min>200'] = df_administrador[df_administrador['totales'] > 200].min()
    df_agrupAdmin['Max>200'] = df_administrador[df_administrador['totales'] > 200].max()
    df_agrupAdmin['Ausentes>200'] = df_administrador[df_administrador['phishing'] > 200].count()
    df_agrupAdmin['Media>200'] = df_administrador[df_administrador['totales'] > 200].mean()
    df_agrupAdmin['Mediana>200'] = df_administrador[df_administrador['totales'] > 200].mean()
    df_agrupAdmin['Varianza>200'] = df_administrador[df_administrador['totales'] > 200].std()
    df_agrupAdmin = df_agrupAdmin.drop(['permisos','totales'], axis=0)

    print("####### EJERCICIO 3 ####### ")
    print("\nUsuarios (permiso 0):\n")
    print(df_agrupAdmin)
    print("\nAdministradores (permiso 1):\n")
    print(df_agrupUsuario)

    print("####### FIN EJERCICIO 3 #######\n\n ")

def sql_password(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS CONTRASENA (hash text)")
    conn.commit()
    with open("realhuman_phill.txt", 'r') as f:
        data = f.read()
        for line in data:
            hash= hashlib.new("amd5",line)
            conn.execute("INSERT INTO CONTRASENA(hash)"
                         "VALUES (?)", (hash))

def sql_hashesh():

    fichero=open('500-worst-passwords.txt')
    df_muestras=pd.DataFrame(conn.execute('SELECT nombre, contrasena, phishing, clicados FROM Usuario'), columns=['nombre','contrasena','phishing','clicados'])
    df_muestras['vulnerable']='0'
    contador=-1
    for line in df_muestras['contrasena']:
        fichero = open('500-worst-passwords.txt')
        contador+=1
        for linea in fichero:
            linea=linea.replace('\n','')
            if (hashlib.md5(linea.encode()).hexdigest() == line):
                df_muestras.at[contador,'vulnerable']='1'

    df_mask=df_muestras['vulnerable']=='1'
    df_mask_noVulnerable=df_muestras['vulnerable']=='0'
    df_vulnerable=df_muestras[df_mask]
    df_noVulnerable=df_muestras[df_mask_noVulnerable]



    #APARTADO 1:
    df_ranking_vulnerable = pd.DataFrame()
    df_ranking_vulnerable = df_vulnerable.nlargest(n=10, columns=['clicados'])
    #alt.Chart(df_ranking_vulnerable).mark_bar().encode(x='nombre', y='clicados').show()

    #APARTADO: 2
    df_politicas=pd.DataFrame(conn.execute('SELECT web,cookies, aviso, proteccion_de_datos , creacion FROM Legal'), columns=['web','cookies','aviso','proteccion_de_datos','creacion'])
    df_politicas['politicas_actualizadas']=df_politicas['cookies']+df_politicas['aviso']+df_politicas['proteccion_de_datos']

    df_ranking_politicas = pd.DataFrame()
    df_ranking_politicas = df_politicas.nsmallest(n=5, columns=['politicas_actualizadas'])
    alt.Chart(df_ranking_politicas).mark_bar().encode(x='web', y='politicas_actualizadas').show()

    #APARTADO: 3
    df_fechas = pd.DataFrame(conn.execute('SELECT  usuario ,count(fecha) FROM Fechas GROUP BY usuario'),
                             columns=['usuario', 'numeroFechas'])
    df_fechas = pd.merge(df_fechas, df_muestras, left_on='usuario', right_on='nombre')

    df_compararConexiones=pd.DataFrame(columns=['vulnerables','noVulnerables'])
    df_mask=df_fechas['vulnerable']=='1'
    df_mask_noVulnerable=df_fechas['vulnerable']=='0'

    df_conexionesVulnerables=df_fechas[df_mask]
    df_conexionesNoVulnerables=df_fechas[df_mask_noVulnerable]

    df_compararConexiones.loc['media']={'vulnerables':0, 'noVulnerables':0}
    df_compararConexiones['noVulnerables']=df_conexionesNoVulnerables['numeroFechas'].mean()
    df_compararConexiones['vulnerables']=df_conexionesVulnerables['numeroFechas'].mean()


    df_resultados=pd.DataFrame()
    df_resultados['media']=df_compararConexiones.mean()
    print("####### EJERCICIO 4 ####### ")
    print("Apartado c:")
    print(df_resultados)
    #alt.Chart(df_compararConexiones).mark_bar().encode(x='tipo', y='media').show()


    #APARTADO: 4
    #print(df_vulnerable)
    #print(df_politicas)
    ##df_mask_3=df_creacion[df_creacion['politicas_actualizadas']==3]
    ##df_mask_0=df_creacion[df_creacion['politicas_actualizadas']==0]
    ##df_creacion['creacion']=df_creacion[df_mask_3]
    ##df_creacion['creacion'] = df_creacion[df_mask_0]

    df_mask_3=df_politicas[df_politicas['politicas_actualizadas']==3]
    df_mask_0=df_politicas[df_politicas['politicas_actualizadas']<3]
    df_aux=df_mask_0.groupby(['creacion']).count()
    #print(df_mask_3.groupby(['creacion']).count())
    #print(df_aux)



    #APARTADO: 5
    df_comparacion=pd.DataFrame()
    df_comparacion['ContrasenasComprometidas']=df_vulnerable.apply(len)
    df_comparacion['ContrasenasNOComprometidas']=df_noVulnerable.apply(len)
    df_comparacion = df_comparacion.drop(['nombre','vulnerable','phishing','clicados'], axis=0)
    print("\nApartado e:")
    print(df_comparacion)
    print("####### FIN EJERCICIO 4 ####### ")






conn = sqlite3.connect('example.db')
sql_delete_table_user(conn)
sql_create_table_user(conn)
sql_delete_table_legal(conn)
sql_create_table_legal(conn)
sql_introducir_datos_user(conn)
sql_introducir_datos_legal(conn)
sql_dataframes(conn)
sql_permisos(conn)
sql_hashesh()
