import os
from flask import Flask, jsonify, make_response, render_template, request, flash, url_for, redirect
import cryptocode
import json
import pymongo


#conexion base datos
myClient=pymongo.MongoClient("mongodb://localhost:27017")
myDb=myClient["taskapp"]

#instancia de la aplicación
app = Flask(__name__)

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



#diccionario para el registro de usuarios Docentes



diccionario_Docentes={}
@app.route('/nuevoregistrodocente',methods=['POST'])


def nuevoregistrodocente(): 
    '''función que permite guardar los datos de un nuevo docente'''
      #con path se especifica la ruta del archivo
    path, _=os.path.split(os.path.abspath(__file__))
    
       
    with open(path+'/registrodocente.json') as file:
        data_Docentes= json.load(file)

    nombreDocente= request.form.get('nombre')
    telefonoDocente= request.form.get('telefono')
    experienciaDocente= request.form.get('experiencia')
    correoDocente= request.form.get('correo')
    contraseniaDocente= request.form.get('contrasenia')
   


    #cifrado de la contraseña
    cifrado=cryptocode.encrypt(contraseniaDocente, "password")

    #validar que se ingresen datos
    if len(nombreDocente)>0 and len(telefonoDocente)>0 and len(experienciaDocente)>0 and len(correoDocente)>0 and len(contraseniaDocente)>0:
       
       
      
       
        diccionario_Docentes={'nombreDocente':nombreDocente, 'telefonoDocente':telefonoDocente,
        'experienciaDocente':experienciaDocente, 'correoDocente': correoDocente, 'contraseniaDocente':cifrado}
        
        data_Docentes.append(diccionario_Docentes)
        
 
    
         #se escribe en el archivo datos.json
        with open(path+f'/registroDocente.json','w') as file:
            json.dump(data_Docentes, file, indent=4)

     
    else:
        #alerta en caso de que existan errores
        flash('Error al ingresar los datos')
        return render_template('registroDocente.html')

#Validación de usuarios Docentes

#ruta hacia validar_usuarios_Docentes
@app.route('/validar_usuarios_Docentes',methods=['POST'])

#función que permite visualizar las tareas almacenadas
def validar_usuarios_Docentes():
    if request.method=='POST':
        correo= request.form.get("correo")
        contrasenia= request.form.get("contrasenia")

        path, _=os.path.split(os.path.abspath(__file__))
        
    #se carga el archivo registropoatulanye.json
        with open(path+'/registroDocente.json') as file:
            data= json.loads(file.read())
        
        #se recorre cada elemento del diccionario
        for elemento in range(len(data)):
            
            try:

            #descifrado de la contraseña
                descifrado= cryptocode.decrypt(data[elemento]["contraseniaPostulante"], 'password')
                if correo!=data[elemento]["correoPostulante"] and contrasenia!=data[elemento][descifrado]:
                    elemento=elemento+1
                    #retorna nuevamente la misma página
                    flash(data[elemento]["correoPostulante"])
                    return render_template('logindocente.html')
                else:
                    #si se valida retorna la página de aprendizale
                     return index()
                    
                    
            except KeyError:
                continue
    else:
        flash("Error")
        return render_template('layouts/logindocente.html')
    return  render_template('layouts/logindocente.html')

@app.route('/validar_usuario_Alumno',methods=['POST'])
def loginAlumno():
    if request.method=='POST':
        signup= request.form.values()
        if signup=="activo":
            return render_template('layouts/index.html')



    






if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug = True)