import os
from flask import Flask, jsonify, make_response, render_template, request, flash, url_for, redirect, session
import cryptocode
import json
from numpy import delete
import pymongo
import bcrypt


#conexion base datos

MONGO_HOST="localhost"
MONGO_PUERTO="27017"
MONGO_TIEMPO_FUERA=1000

MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"

MONGO_BASEDATOS="preescolar"
MONGO_COLECCION1="usuariosDocentes"
MONGO_COLECCION2="usuariosAdmin"
MONGO_COLECCION3="alumnos"
MONGO_COLECCION4="reporte"
cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
#base de datos
baseDatos=cliente[MONGO_BASEDATOS]
#colección
coleccion=baseDatos[MONGO_COLECCION1]
coleccion2=baseDatos[MONGO_COLECCION2]
coleccion3=baseDatos[MONGO_COLECCION3]
coleccion4=baseDatos[MONGO_COLECCION4]
#Encuentra el primer documento
x=coleccion3.find_one()
print(x)
#Retorna todos los documentos de la coleccion
for documento in coleccion4.find():
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
@app.route("/puntaje.html")

def puntaje():

    return render_template("layouts/puntaje.html")

@app.route("/accederalumno")

def accederalumno():
    """Retorna Login de niños"""
    return render_template("layouts/login.html")

@app.route("/accederRegistroDocente")

def accederRegistroDocente():
    """Retorna pagina de Regsitro Docente"""
    return render_template("layouts/registrodocente.html")

@app.route("/logindocente.html")

def logindocente():
    """Retorna Login de docentes"""


    return render_template("layouts/logindocente.html")

@app.route("/loginadmin.html")

def loginadmin():
    """Retorna Login de admin"""


    return render_template("layouts/loginadmin.html")

@app.route("/eliminardocente.html")

def removerDocente():
    """Retorna pagina de eliminacion de Docente"""

    return render_template("layouts/eliminardocente.html")

@app.route("/reporte.html")

def reporte():
    """Retorna pagina de reporte"""

    return render_template("layouts/reporte.html")




@app.route("/logindocente1", methods=['POST'])

def logindocente1():
        "Validad Login de docentes"

        login_usuario = coleccion.find_one({'correo' : request.form['correo']})

        if login_usuario:
            if bcrypt.hashpw(request.form['contrasenia'].encode('utf-8'), login_usuario['contrasenia'].encode('utf-8')) == login_usuario['contrasenia'].encode('utf-8'):
                session['correo'] = request.form['correo']
                return reporte()

        return render_template("layouts/logindocente.html")

@app.route("/validaLoginAdmin", methods=['POST'])

def validaLoginAdmin():
    """Valida Login de admin"""
    login_usuarioAdmin = coleccion2.find_one({'correo' : request.form['correo']})

    if login_usuarioAdmin :
            if request.form['contrasenia'].encode('utf-8') == login_usuarioAdmin['contrasenia'].encode('utf-8'):
                session['correo'] = request.form['correo']
                return accederRegistroDocente()
            else:
                flash('Usuario/Contraseña inválidos')
                return loginadmin()


    return flash('Usuario/Contraseña inválidos') ,loginadmin()


@app.route('/registroDocente', methods=['POST', 'GET'])
def registroDocente():
    if request.method == 'POST':
        c=coleccion
        existe_usuario =  c.find_one({'correo' : request.form['correo']})

        if existe_usuario is None:
            hashpass = bcrypt.hashpw(request.form['contrasenia'].encode('utf-8'), bcrypt.gensalt())
            c.insert_one({'nombre':request.form['nombre'],'apellido':request.form['apellido'],'telefono':request.form['telefono'],'correo' : request.form['correo'], 'contrasenia' : hashpass})
            session['nombre'] = request.form['nombre']
            session['apellido'] = request.form['apellido']
            session['telefono'] = request.form['telefono']
            session['correo'] = request.form['correo']
            return index()
        return render_template('layouts/registrodocente.html')
        
    
    return render_template('layouts/registrodocente.html')
@app.route('/eliminarDocente', methods=['POST', 'GET'])
def eliminarDocente():
    if request.method == 'POST':
        c=coleccion
       

        
        c.delete_one({'correo' : request.form['correo']})
        return 'eliminado'
        

    return render_template('layouts/eliminardocente.html')








@app.route('/loginAlumno',methods=['POST', 'GET'])
def loginAlumno():
    if request.method=='POST':
        """Validación de login alumno"""
       
        c3=coleccion3
        query={}
        docente=coleccion.find_one(query,{'correo':1})
        c3.insert_one({'nombreAlumno' : request.form['alumno1'],'correoDocente':docente})
       
        
        c3.find_one()
        return evaluacion()
    return evaluacion()
@app.route('/loginAlumno2',methods=['POST', 'GET'])
def loginAlumno2():
    """Validación de login alumno"""
    if request.method=='POST':
       
        c3=coleccion3
        query={}
        docente=coleccion.find_one(query,{'correo':1})
      
        c3.insert_one({'nombreAlumno' : request.form['alumno2'],'correoDocente':docente})
 
        c3.find_one()
        return evaluacion()
    return evaluacion()
@app.route('/loginAlumno3',methods=['POST', 'GET'])
def loginAlumno3():
    """Validación de login alumno"""
    if request.method=='POST':
       
        c3=coleccion3
        query={}
        docente=coleccion.find_one(query,{'correo':1})
      
        c3.insert_one({'nombreAlumno' : request.form['alumno3'],'correoDocente':docente})
    
        c3.find_one()
        return evaluacion()
    return evaluacion()
@app.route('/loginAlumno4',methods=['POST', 'GET'])
def loginAlumno4():
    """Validación de login alumno"""
    if request.method=='POST':
       
        c3=coleccion3
        query={}
        docente=coleccion.find_one(query,{'correo':1})

        c3.insert_one({'nombreAlumno' : request.form['alumno4'],'correoDocente':docente})
        
        c3.find_one()
        return evaluacion()
    return evaluacion()

@app.route('/obtenerDatos')
def obtenerDatos():
    
    
        
    puntaje=5
   
    valoracion = request.form.get("num")

    coleccion4.insert_one({'puntaje':puntaje,'valoracion':valoracion})
    datosC3=coleccion3.find()
    datosC4=coleccion4.find()
   
    
    

    return render_template("layouts/reporte.html", coleccion3=datosC3, coleccion4=datosC4)
  


       



    






if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug = True)