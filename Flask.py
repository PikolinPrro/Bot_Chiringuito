from flask import Flask
import subprocess

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello from Flask!'

@app.route('/bot_cierra', methods=['POST'])
def bot_cierra():
  subprocess.run(['python', 'Api_cierra.py'])

  return 'comando bot está en linea'

@app.route('/bot_compra', methods=['POST'])
def bot_compra():
  subprocess.run(['python', 'Api_compra.py'])

  return 'comando bot está en linea'

@app.route('/acumulador', methods=['POST'])
def acumulador():
  subprocess.run(['python', 'acumulador.py'])

  return 'el archivo de texto se ha modificado'