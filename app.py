import os
from flask import Flask, jsonify, make_response, render_template, request

#instancia de la aplicación
app = Flask(__name__)

#rutas de la carpeta templates/static
app._static_folder = os.path.abspath("templates/")

#ruta de la página principal index
@app.route("/")

def index():

    return render_template("layouts/index.html")

@app.route("/evaluacion/")

def evaluacion():

    return render_template("layouts/evaluacion.html")



if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug = True)