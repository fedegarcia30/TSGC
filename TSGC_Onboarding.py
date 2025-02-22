from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    licencia = request.form['licencia']
    nombre_apellidos = request.form['nombre_apellidos']
    correo_electronico = request.form['correo_electronico']
    return f"Licencia: {licencia}, Nombre y Apellidos: {nombre_apellidos}, Correo Electrónico: {correo_electronico}"

if __name__ == '__main__':
    app.run(debug=True)