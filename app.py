import requests
from flask import Flask, render_template, request, redirect, url_for
import re

app = Flask(__name__)


# Lista para almacenar los registros
registros = []
registros_locales = []
registros_api = []


# Función para validar el formato de la identificación
def validar_identificacion(identificacion):
    if re.match(r'^\d{4,11}$', identificacion):
        for registro in registros:
            if registro['identificacion'] == identificacion:
                return False
        return True
    return False


# Función para validar el formato del nombre completo
def validar_nombre(nombre):
    return re.match(r'^[a-zA-ZáéíóúñÁÉÍÓÚÑ\s]{1,100}$', nombre)


# Función para validar el número de teléfono
def validar_telefono(telefono):
    return re.match(r'^[36]\d{9}$', telefono)


# Función para validar el correo electrónico
def validar_correo(correo):
    return re.match(r'^[\w\.-]+@[\w\.-]+$', correo)





# Ruta para el formulario de registro
@app.route('/', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        identificacion = request.form['identificacion']
        nombre = request.form['nombre']
        genero = request.form['genero']
        telefono = request.form['telefono']
        correo = request.form['correo']

        if validar_identificacion(identificacion) and validar_nombre(nombre) and validar_telefono(
                telefono) and validar_correo(correo):
            registros.append({
                'identificacion': identificacion,
                'nombre': nombre,
                'genero': genero,
                'telefono': telefono,
                'correo': correo
            })
            if validar_identificacion(identificacion) and validar_nombre(nombre) and validar_telefono(
                    telefono) and validar_correo(correo):
                registros.append({
                    'identificacion': identificacion,
                    'nombre': nombre,
                    'genero': genero,
                    'telefono': telefono,
                    'correo': correo
                })
                mensaje = "¡Registro exitoso!"
                return render_template('formulario.html', mensaje=mensaje)

    return render_template('formulario.html')




# Ruta para ver la lista de registros
@app.route('/registros')
def lista_registros():
    return render_template('registros.html', registros=registros)




# Ruta para editar un registro
@app.route('/editar/<identificacion>', methods=['GET', 'POST'])
def editar_registro(identificacion):
    registro_editar = None
    for registro in registros:
        if registro['identificacion'] == identificacion:
            registro_editar = registro
            break

    if request.method == 'POST':
        nuevo_nombre = request.form['nombre']
        nuevo_genero = request.form['genero']
        nuevo_telefono = request.form['telefono']
        nuevo_correo = request.form['correo']

        registro_editar['nombre'] = nuevo_nombre
        registro_editar['genero'] = nuevo_genero
        registro_editar['telefono'] = nuevo_telefono
        registro_editar['correo'] = nuevo_correo

        return redirect(url_for('consultar_registros'))

    return render_template('editar.html', registro=registro_editar)


# Ruta para eliminar un registro
@app.route('/eliminar/<identificacion>', methods=['GET'])
def eliminar_registro(identificacion):
    global registros
    registros = [registro for registro in registros if registro['identificacion'] != identificacion]
    return redirect(url_for('consultar_registros'))





# Ruta para consultar los registros de la API y locales
@app.route('/consultar', methods=['GET'])
def consultar_registros():
    global registros, registros_api

    # Realizar una solicitud GET a la API
    response = requests.get('https://gorest.co.in/public/v2/users')

    if response.status_code == 200:
        data = response.json()
        registros_api = data

        return render_template('registros.html', registros_locales=registros, registros_api=registros_api)
    else:
        return 'Error al obtener los registros de la API'


if __name__ == '__main__':
    app.run(debug=True)
