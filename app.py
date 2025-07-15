from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

#congiguraciondb
USER_DB= 'admin'
PASS_DB= 'Q51s&1ck#P7c^6prXHf5'
URL_DB= 'localhost'
PORT= '5432'
NAME_DB = 'sap_flask_db'
FULL_URL_DB =f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}:{PORT}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI']=FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#inicializaciondel objeto db sqlalchemy
db = SQLAlchemy(app)

#configurar flask-migrate
migrate =Migrate()
migrate.init_app(app,db)

class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    apellido = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)

def __str__(self):
    return (
        f'Id:{self.id},'
        f'nombre:{self.nombre},'
        f'apellido:{self.apellido},'
        f'email:{self.email},'
    )

@app.route('/')
def index():
    return "Conexión exitosa a PostgreSQL con SQLAlchemy"

if __name__ == '__main__':
    app.run(debug=True)