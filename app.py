import os
from flask import Flask, jsonify, make_response, render_template, request, flash, url_for, redirect, session
import cryptocode
import json
import pymongo
import bcrypt


#conexion base datos

MONGO_HOST="localhost"
MONGO_PUERTO="27017"
MONGO_TIEMPO_FUERA=1000

MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"

MONGO_BASEDATOS="preescolar"
MONGO_COLECCION="usuariosDocentes"
cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
#base de datos
baseDatos=cliente[MONGO_BASEDATOS]
#colección
coleccion=baseDatos[MONGO_COLECCION]
#Encuentra el primer documento
x=coleccion.find_one()
print(x)
#Retorna todos los documentos de la coleccion
for documento in coleccion.find():
    print(documento)

#instancia de la aplicación
app = Flask(__name__)
#clave secreta de la aplicación
app.secret_key = "luisparedez"
#rutas de la carpeta templates/static
app._static_folder = os.path.abspath("templates/static")

@app.route("/")

def login():

    return render_template("layouts/estudiante.html")

#ruta de la página principal index
@app.route("/index.html")

def index():

    return render_template("layouts/index.html")

@app.route("/evaluacion.html")

def evaluacion():

    return render_template("layouts/evaluacion.html")

@app.route("/accederalumno")

def accederalumno():
    """Retorna Login de niños"""
    return render_template("layouts/login.html")

@app.route("/logindocente.html")

def logindocente():
    """Retorna Login de docentes"""


    return render_template("layouts/logindocente.html")



@app.route("/logindocente1", methods=['POST'])

def logindocente1():
        "Retorna Login de docentes"

        login_user = coleccion.find_one({'correo' : request.form['correo']})

        if login_user:
            if bcrypt.hashpw(request.form['contrasenia'].encode('utf-8'), login_user['contrasenia'].encode('utf-8')) == login_user['contrasenia'].encode('utf-8'):
                session['correo'] = request.form['correo']
                return index()

        return 'Invalid username/password combination'

@app.route('/registroDocente', methods=['POST', 'GET'])
def registroDocente():
    if request.method == 'POST':
        c=coleccion
        existing_user =  c.find_one({'correo' : request.form['correo']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['contrasenia'].encode('utf-8'), bcrypt.gensalt())
            c.insert_one({'correo' : request.form['correo'], 'contrasenia' : hashpass})
            session['correo'] = request.form['correo']
            return index()
        
        return 'That username already exists!'

    return render_template('layouts/registrodocente.html')




#diccionario para el registro de usuarios Docentes




@app.route('/validar_usuario_Alumno',methods=['POST'])
def loginAlumno():
    if request.method=='POST':
        signup= request.form.values()
        if signup=="activo":
            return render_template('layouts/index.html')



    






if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug = True)