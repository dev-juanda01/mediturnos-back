# importar paquete
from flask import Flask

# crear instancia
app = Flask(__name__)

# correr aplicacion
if "__main__" == __name__:
    app.run(debug=True, port=5000)