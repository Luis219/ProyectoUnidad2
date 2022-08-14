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
MONGO_COLECCION="usuarios"
MONGO_COLECCIONPERMISOS="permisos"
MONGO_COLECCIONROLES="rols"
MONGO_COLECCIONMATERIA="materia"
MONGO_COLECCIONPARALELO="paralelo"
MONGO_COLECCIONHORARIO="horario"

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
coleccion=baseDatos[MONGO_COLECCION1]
coleccion2=baseDatos[MONGO_COLECCION2]
coleccion3=baseDatos[MONGO_COLECCION3]
coleccion4=baseDatos[MONGO_COLECCION4]
#Encuentra el primer documento
x=coleccionRoles.find_one()
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

@app.route("/estudiante.html")

def estudiante():
    """Retorna a inicio"""
    imagen=coleccionUsuarios.find()


    return render_template("layouts/estudiante.html", coleccionUsuarios=imagen)

@app.route("/accederalumno")

def accederalumno():
    """Retorna Login de niños"""
    return render_template("layouts/login.html")

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



@app.route("/registrousuario.html", methods=['POST', 'GET'])

def accederRegistroUsuario():
    """Retorna pagina de Regsitro Docente"""
    roles=coleccionRoles.find()
    permisos=coleccionPermisos.find()
    return render_template("layouts/registrousuario.html", coleccionRoles=roles, coleccionPermisos=permisos)

@app.route("/loginusuario.html")
def usuario():
    """Retorna Login de docentes"""


    return render_template("layouts/loginusuario.html")

@app.route("/registroestudiante.html")
def accederestudiante():
    """Retorna Registro Estudiantes"""
    materia=coleccionMateria.find()
    roles=coleccionRoles.find()


    return render_template("layouts/registroestudiante.html", coleccionMateria=materia, coleccionRoles=roles)

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

@app.route("/loginusuario",  methods=['POST'])

def loginusuario():
        "Validar Login de usuarios"

        login_usuario = coleccionUsuarios.find_one({'correo' : request.form['correo']})

        if login_usuario:
            if bcrypt.hashpw(request.form['contrasenia'].encode('utf-8'), bcrypt.gensalt()) == login_usuario['contrasenia']:
                session['correo'] = request.form['correo']
                return reporte()
            else:
                 return usuario()


        return render_template("layouts/logindocente.html")





@app.route("/logindocente1",  methods=['POST'])

def logindocente1():
        "Validad Login de docentes"

        login_usuario = coleccion.find_one({'correo' : request.form['correo']})

        if login_usuario:
            if bcrypt.hashpw(request.form['contrasenia'].encode('utf-8'), bcrypt.gensalt()) == login_usuario['contrasenia']:
                session['correo'] = request.form['correo']
                return reporte()
            else:
                 return loginusuario()


        return render_template("layouts/logindocente.html")

@app.route("/validaLoginAdmin", methods=['POST', 'GET'])

def validaLoginAdmin():
    """Valida Login de admin"""

    query={"rol":{"$eq":"administrador"}}
    login_usuarioAdmin = coleccionUsuarios.find_one(query,{'correo' : request.form['correo']})

    if login_usuarioAdmin is True:
            if request.form['contrasenia'].encode('utf-8') == login_usuarioAdmin['contrasenia'].encode('utf-8'):
                session['correo'] = request.form['correo']
                return accederRegistroUsuario()
            else:
   
                return loginadmin()


    return loginadmin()

@app.route('/registroUsuario', methods=['POST', 'GET'])
def registroUsuario():
    if request.method == 'POST':
        
        existe_usuario =  coleccionUsuarios.find_one({'correo' : request.form['correo']})

        if existe_usuario is None:
            rol=request.form['menuRoles']
            if rol=="docente":
                queryPermiso={"_id":{"$in":[1,2]}}
            
                permisosDocente=list(coleccionPermisos.find(queryPermiso))

                hashpass = bcrypt.hashpw(request.form['contrasenia'].encode('utf-8'), bcrypt.gensalt())
                coleccionUsuarios.insert_one({'nombre':request.form['nombre'],'apellido':request.form['apellido'],'telefono':request.form['telefono'],'rol':request.form['menuRoles'],'permiso':permisosDocente,  'correo' : request.form['correo'], 'contrasenia' : hashpass})
                session['nombre'] = request.form['nombre']
                session['apellido'] = request.form['apellido']
                session['telefono'] = request.form['telefono']
                session['correo'] = request.form['correo']
                session['rol']=request.form['menuRoles']
                session['permiso']=permisosDocente
                return reporte()

            elif rol=="administrador":
                queryPermiso={"_id":{"$in":[3,4,5,6,7,8]}}
            
                permisosAdministrador=list(coleccionPermisos.find(queryPermiso))

                hashpass = bcrypt.hashpw(request.form['contrasenia'].encode('utf-8'), bcrypt.gensalt())
                coleccionUsuarios.insert_one({'nombre':request.form['nombre'],'apellido':request.form['apellido'],'telefono':request.form['telefono'],'rol':request.form['menuRoles'],'permiso':permisosAdministrador,  'correo' : request.form['correo'], 'contrasenia' : hashpass})
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

#Registro de asignacion
@app.route('/registroAsignacion', methods=['POST', 'GET'])
def registroAsignacion():
    if request.method == 'POST':
        existe_usuario =  coleccionUsuarios.find_one({'nombre' : request.form['menuDocentes']})
        print(existe_usuario)

        if existe_usuario:
            actualizacion={ "$set":{'materia': request.form['menuMaterias'],'paralelo': request.form['menuParalelos'],'hora inicio': request.form['menuHorarioInicio'], 'hora fin': request.form['menuHorarioFin']}}
            coleccionUsuarios.update_one(existe_usuario,actualizacion)
            return reporte()
        return render_template('layouts/asignacion.html')

#Registro de estudiante
@app.route('/registroEstudiante', methods=['POST', 'GET'])
def registroEstudiante():
    if request.method == 'POST':
        existe_usuario =  coleccionUsuarios.find_one({'cedula' : request.form['cedula']})
        edad=request.form['edad']
       
       
        if existe_usuario is None and int(edad)>=3 and int(edad)<=5:
            coleccionUsuarios.insert_one({'imagen':request.files['imagen'],'cedula' : request.form['cedula'],'nombre':request.form['nombre'],'apellido':request.form['apellido'],'telefono':request.form['telefono'],'edad':request.form['edad'],'materia':request.form['menuMateria'],'rol':request.form['menuRoles'],'correo':request.form['correo'],'contrasenia':request.form['contrasenia']})
            return reporte()
        return render_template('layouts/registroestudiante.html')



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
            return reporte()
        return render_template('layouts/registrodocente.html')
        
    
    return render_template('layouts/registrodocente.html')
@app.route('/eliminarDocente', methods=['POST', 'GET'])
def eliminarDocente():
    if request.method == 'POST':
        

        
        coleccion.delete_one({'correo' : request.form['correo']})
        return 'eliminado'
        

    return render_template('layouts/eliminardocente.html')








@app.route('/loginAlumno',methods=['POST', 'GET'])
def loginAlumno():
    if request.method=='POST':
        """Validación de login alumno"""
       
        
        query={}
        docenteCorreo=coleccion.find_one(query,{'correo':1})
        docenteNombre=coleccion.find_one(query,{'nombre':1})
        docenteApellido=coleccion.find_one(query,{'apellido':1})
        docenteTelefono=coleccion.find_one(query,{'telefono':1})
        coleccion3.insert_one({'nombreAlumno' : request.form['alumno1'],'correoDocente':docenteCorreo,'nombreDocente':docenteNombre,'apellido':docenteApellido,'DocenteTelefono': docenteTelefono})
       
        
        coleccion3.find_one()
        return index()
    return evaluacion()

@app.route('/loginAlumno2',methods=['POST', 'GET'])
def loginAlumno2():
    """Validación de login alumno"""
    if request.method=='POST':
       
       
        query={}
        docente=coleccion.find_one(query,{'correo':1})
      
        coleccion3.insert_one({'nombreAlumno' : request.form['alumno2'],'correoDocente':docente})
 
        coleccion3.find_one()
        return evaluacion()
    return evaluacion()
@app.route('/loginAlumno3',methods=['POST', 'GET'])
def loginAlumno3():
    """Validación de login alumno"""
    if request.method=='POST':
       
        
        query={}
        docente=coleccion.find_one(query,{'correo':1})
      
        coleccion3.insert_one({'nombreAlumno' : request.form['alumno3'],'correoDocente':docente})
    
        coleccion3.find_one()
        return evaluacion()
    return evaluacion()

@app.route('/loginAlumno4',methods=['POST', 'GET'])
def loginAlumno4():
    """Validación de login alumno"""
    if request.method=='POST':
       
        
        query={}
        docente=coleccion.find_one(query,{'correo':1})

        coleccion3.insert_one({'nombreAlumno' : request.form['alumno4'],'correoDocente':docente})
        
        coleccion3.find_one()
        return evaluacion()
    return evaluacion()

@app.route('/obtenerDatos')
def obtenerDatos():
    """Obtención de datos estudiante"""  
    puntaje=5
   
    valoracion = request.form.get("num")

    coleccion4.insert_one({'puntaje':puntaje,'valoracion':valoracion})
    datosC3=coleccion3.find()
    datosC4=coleccion4.find()
   
    return render_template("layouts/reporte.html", coleccion3=datosC3, coleccion4=datosC4)
  


       



    






if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug = True)