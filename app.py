
import os
from flask import Flask, jsonify, make_response, render_template, request, flash, url_for, redirect, session
from werkzeug.utils import secure_filename
import cryptocode
import json
from numpy import delete
import pymongo

from flask_bcrypt import Bcrypt 


#conexion base datos

MONGO_HOST="localhost"
MONGO_PUERTO="27017"
MONGO_TIEMPO_FUERA=1000

MONGO_URI="mongodb://"+MONGO_HOST+":"+MONGO_PUERTO+"/"

MONGO_BASEDATOS="preescolar"
MONGO_COLECCION="usuarios"
MONGO_COLECCIONPERMISOS="permisos"
MONGO_COLECCIONROLES="rols"
MONGO_COLECCIONMATERIA="materia"
MONGO_COLECCIONPARALELO="paralelo"
MONGO_COLECCIONHORARIO="horario"
MONGO_COLECCIONNOTAS="notas"

cliente=pymongo.MongoClient(MONGO_URI,serverSelectionTimeoutMS=MONGO_TIEMPO_FUERA)
#base de datos
baseDatos=cliente[MONGO_BASEDATOS]
#colección 
coleccionUsuarios=baseDatos[MONGO_COLECCION]
coleccionRoles=baseDatos[MONGO_COLECCIONROLES]
coleccionPermisos=baseDatos[MONGO_COLECCIONPERMISOS]
coleccionHorario=baseDatos[MONGO_COLECCIONHORARIO]
coleccionMateria=baseDatos[MONGO_COLECCIONMATERIA]
coleccionParalelo=baseDatos[MONGO_COLECCIONPARALELO]
coleccionNota=baseDatos[MONGO_COLECCIONNOTAS]
#Encuentra el primer documento
x=coleccionRoles.find_one()
print(x)

#instancia de la aplicación
app = Flask(__name__)
#clave secreta de la aplicación
app.secret_key = "luisparedez"
#rutas de la carpeta templates/static
app._static_folder = os.path.abspath("templates/static")

UPLOAD_FOLDER = 'templates/static/imagenes'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

bcrypt = Bcrypt(app)
#página principal del aplicativo
@app.route("/",methods=['POST', 'GET'])

def login():

    imagen=coleccionUsuarios.find()
    query={"rol":{"$eq":"estudiante"}}
    nombre=coleccionUsuarios.find(query)

    return render_template("layouts/estudiante.html", coleccionUsuarios=imagen, nombres=nombre)

#ruta de la página de enseñanza del aplicativo
@app.route("/index.html", methods=['POST', 'GET'])

def index():

    return render_template("layouts/index.html")

@app.route("/evaluacion.html")

#retorna la página del juego
def evaluacion():

    return render_template("layouts/evaluacion.html")
@app.route("/puntaje.html")

#retorna la página de calificación de la app
def puntaje():

    return render_template("layouts/puntaje.html")

#Permite acceder a la página inicial del aplicativo
@app.route("/estudiante.html")

def estudiante():
    """Retorna a inicio"""
    imagen=coleccionUsuarios.find()


    return render_template("layouts/estudiante.html", coleccionUsuarios=imagen)

#Permite acceder a la página de asignación de parámetros a docente
@app.route("/asignacion.html", methods=['POST', 'GET'])

def accederAsignacion():
    """Retorna pagina de asignacion"""
    materia=coleccionMateria.find()
    paralelo=coleccionParalelo.find()
    horarioInicio=coleccionHorario.find()
    horarioFin=coleccionHorario.find()
    query={"rol":{"$eq":"docente"}}
    docente=coleccionUsuarios.find(query)

    return render_template("layouts/asignacion.html", coleccionMateria=materia, coleccionParalelo=paralelo, coleccionHorarioInicio=horarioInicio, coleccionHorarioFin=horarioFin,coleccionUsuarios=docente)


#Permite acceder a la página de registro de un nuevo usuario
@app.route("/registrousuario.html", methods=['POST', 'GET'])

def accederRegistroUsuario():
    """Retorna pagina de Regsitro Docente"""
    roles=coleccionRoles.find()
    permisos=coleccionPermisos.find()
    return render_template("layouts/registrousuario.html", coleccionRoles=roles, coleccionPermisos=permisos)

#Permite acceder a la página de login usuario
@app.route("/loginusuario.html")
def usuario():
    """Retorna Login de usuario"""


    return render_template("layouts/loginusuario.html")

#Permite acceder a la página de registro de estudiante
@app.route("/registroestudiante.html")
def accederestudiante():
    """Retorna Registro Estudiantes"""
    materia=coleccionMateria.find()
    roles=coleccionRoles.find()

    return render_template("layouts/registroestudiante.html", coleccionMateria=materia, coleccionRoles=roles)
#Permite acceder a la página de registro Nota
@app.route("/registronota.html")
def accederRegistroNota():
    """Retorna pagina de Registro Nota"""
    query={"rol":{"$eq":"estudiante"}}
    usuario=coleccionUsuarios.find(query)
    
    return render_template("layouts/registronota.html", coleccionUsuarios=usuario)

#Permiter acceder a la página de login admin
@app.route("/loginadmin.html")

def loginadmin():
    """Retorna Login de admin"""


    return render_template("layouts/loginadmin.html")

#Permite acceder la página para desactivar un usuario
@app.route("/desactivarusuario.html")

def removerUsuario():
    """Retorna pagina de desactivacion de docente"""

    return render_template("layouts/desactivarusuario.html")

@app.route("/reporte.html")

#Permite acceder a la página de reporte
def reporte():
    """Retorna pagina de reporte"""

    return render_template("layouts/reporte.html")


#Validación de usuario
@app.route("/loginusuario",  methods=['POST'])

def loginusuario():
        "Validar Login de usuarios"
        query={"rol":{"$eq":"docente"}}
        login_usuario = coleccionUsuarios.find_one({'correo' : request.form['correo'],'estado':"activo"})
        contrasenia=request.form['contrasenia']
        if login_usuario:
            
            if  bcrypt.check_password_hash(login_usuario['contrasenia'],contrasenia):
                session['correo'] = request.form['correo']
                return reporte()
            else:
                 return usuario()


        return render_template("layouts/loginusuario.html")


#Registra un nuevo usuario
@app.route('/registroUsuario', methods=['POST', 'GET'])
def registroUsuario():
    if request.method == 'POST':
        
        existe_usuario =  coleccionUsuarios.find_one({'correo' : request.form['correo']})

        if existe_usuario is None:
            rol=request.form['menuRoles']
            if rol=="docente":
                queryPermiso={"_id":{"$in":[1,2]}}
            
                permisosDocente=list(coleccionPermisos.find(queryPermiso))
                contrasenia=request.form['contrasenia']

               
                hashpass =bcrypt.generate_password_hash(contrasenia).decode('utf-8') 
                coleccionUsuarios.insert_one({'nombre':request.form['nombre'],'apellido':request.form['apellido'],'telefono':request.form['telefono'],'rol':request.form['menuRoles'],'permiso':permisosDocente,  'correo' : request.form['correo'], 'contrasenia' : hashpass,"estado":"activo"})
                session['nombre'] = request.form['nombre']
                session['apellido'] = request.form['apellido']
                session['telefono'] = request.form['telefono']
                session['correo'] = request.form['correo']
                session['rol']=request.form['menuRoles']
                session['permiso']=permisosDocente
                return reporte()

            elif rol=="administrador":
                numeroUsuarios=coleccionUsuarios.count_documents({})
                if numeroUsuarios==1:
                    queryPermiso={"_id":{"$in":[3,4,5,6,7,8]}}
                
                    permisosAdministrador=list(coleccionPermisos.find(queryPermiso))
                    contrasenia=request.form['contrasenia']

                
                    hashpass =bcrypt.generate_password_hash(contrasenia).decode('utf-8') 

            
                    coleccionUsuarios.insert_one({'nombre':request.form['nombre'],'apellido':request.form['apellido'],'telefono':request.form['telefono'],'rol':request.form['menuRoles'],'permiso':permisosAdministrador,  'correo' : request.form['correo'], 'contrasenia' : hashpass, "estado":"activo"})
                    session['nombre'] = request.form['nombre']
                    session['apellido'] = request.form['apellido']
                    session['telefono'] = request.form['telefono']
                    session['correo'] = request.form['correo']
                    session['rol']=request.form['menuRoles']
                    session['permiso']=permisosAdministrador
                    return reporte()
                return render_template('layouts/registrousuario.html')
            return render_template('layouts/registrousuario.html')
            
        return render_template('layouts/registrousuario.html')
    return render_template('layouts/registrousuario.html')


@app.route("/validaLoginAdmin", methods=['POST', 'GET'])

#Valida un usuario con el rol administrador
def validaLoginAdmin():
    """Valida Login de admin"""

    query={"rol":{"$eq":"administrador"}}
    login_usuarioAdmin = coleccionUsuarios.find_one(query,{'correo' : request.form['correo'],'contrasenia':request.form['contrasenia']})
    contrasenia=request.form['contrasenia']

    if login_usuarioAdmin:
            
            if  bcrypt.check_password_hash(login_usuarioAdmin['contrasenia'],contrasenia):
                session['correo'] = request.form['correo']
                return accederRegistroUsuario()
            else:
   
                return loginadmin()
    else:
        return loginadmin()

    

#Registro de asignacion de materia, aula y horario a un docente
@app.route('/registroAsignacion', methods=['POST', 'GET'])
def registroAsignacion():
    if request.method == 'POST':
        existe_usuario =  coleccionUsuarios.find_one({'nombre' : request.form['menuDocentes']})
        print(existe_usuario)

        if existe_usuario:
            actualizacion={ "$set":{'materia': request.form['menuMaterias'],'aula': request.form['menuParalelos'],'hora inicio': request.form['menuHorarioInicio'], 'hora fin': request.form['menuHorarioFin']}}
            coleccionUsuarios.update_one(existe_usuario,actualizacion)
            return reporte()
        return render_template('layouts/asignacion.html')

#Registro de estudiante
@app.route('/registroEstudiante', methods=['POST', 'GET'])
def registroEstudiante():
    if request.method == 'POST':
        existe_usuario =  coleccionUsuarios.find_one({'cedula' : request.form['cedula']})
        edad=request.form['edad']
        imagen=request.files['imagen']
        filename = secure_filename(imagen.filename)
       
        if existe_usuario is None and int(edad)>=3 and int(edad)<=5:
            imagen.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            coleccionUsuarios.insert_one({'imagen':imagen.filename,'cedula' : request.form['cedula'],'nombre':request.form['nombre'],'apellido':request.form['apellido'],'telefono':request.form['telefono'],'edad':request.form['edad'],'materia':request.form['menuMateria'],'rol':request.form['menuRoles'],'correo':request.form['correo'],'contrasenia':request.form['contrasenia'],'estado':"activo"})
           
            return reporte()
        return render_template('layouts/registroestudiante.html')


#Registro de Nota
@app.route('/registroNota', methods=['POST', 'GET'])
def registroNota():
    if request.method == 'POST':
        
        nota=request.form['calificacion']
        if int(nota)>=1 and int(nota)<=5:
            coleccionNota.insert_one({'cedula' : request.form['menuCedula'],'calificacion':request.form['calificacion']})
            return reporte()
        return render_template('layouts/registroestudiante.html')

#Sirve para desactivar un usuario
@app.route('/desactivarUsuario', methods=['POST', 'GET'])
def desactivarUsuario():
    if request.method == 'POST':
        query={"rol":{"$ne":"administrador"}}
        existe_usuario =  coleccionUsuarios.find_one(query,{'correo' : request.form['correo']})
        actualizacion={"$set":{"estado":"inactivo"}}
        coleccionUsuarios.update_one(existe_usuario, actualizacion)
        return 'desactivado'
        

    return render_template('layouts/desactivarusuario.html')


#Función para generar el reporte de calificaciones
@app.route('/obtenerDatos')
def obtenerDatos():
    """Obtención de datos estudiante"""  

    cedula=coleccionNota.find()
    calificacion=coleccionNota.find()
   
   
    return render_template("layouts/reporte.html", cedulas=cedula,  calificaciones=calificacion)
  


       



    






if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug = True)