from flask import Flask, render_template, redirect, request, url_for, flash
from forms import PersonaForm
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#necesario para wtforms
app.config['SECRET_KEY'] = 'tu-clave-secreta-aqui'

# Configuración de la base de datos
USER_DB = 'admin'
PASS_DB = 'Q51s&1ck#P7c^6prXHf5'
URL_DB = 'localhost'
PORT = '5432'
NAME_DB = 'sap_flask_db'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}:{PORT}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicialización de SQLAlchemy y Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelo Persona
class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    apellido = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)

    def __str__(self):
        return (
            f'Id:{self.id}, '
            f'nombre:{self.nombre}, '
            f'apellido:{self.apellido}, '
            f'email:{self.email}'
        )

# Rutas
@app.route('/')
@app.route('/index')
def index():
    personas = Persona.query.order_by(Persona.id).all()
    total_personas = Persona.query.count()
    app.logger.debug(f'Listado Personas : {personas}')
    app.logger.debug(f'Total Personas : {total_personas}')
    return render_template('index.html', personas=personas, total_personas=total_personas)

@app.route('/view/<int:id>')
def view(id):
    persona = Persona.query.get_or_404(id)
    return render_template('view.html', persona=persona)

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = PersonaForm()
    if form.validate_on_submit():
        nueva_persona = Persona(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            email=form.email.data
        )
        db.session.add(nueva_persona)
        db.session.commit()
        flash('Persona creada correctamente.', 'success')
        return redirect(url_for('index'))
    return render_template('create.html', form=form)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    persona = Persona.query.get_or_404(id)
    form = PersonaForm(obj=persona)  # Aquí cargas los datos actuales en el formulario

    if form.validate_on_submit():
        # Actualizas los datos con lo que el usuario envió
        persona.nombre = form.nombre.data
        persona.apellido = form.apellido.data
        persona.email = form.email.data
        db.session.commit()
        flash('Persona actualizada correctamente.', 'success')
        return redirect(url_for('index'))

    # Cuando es GET, renderizas el formulario con los datos ya cargados
    return render_template('edit.html', form=form)



@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    persona = Persona.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(persona)
        db.session.commit()
        flash('Persona eliminada correctamente.', 'success')
        return redirect(url_for('index'))
    return render_template('delete.html', persona=persona)


# Ejecutar con debug
if __name__ == '__main__':
    app.run(debug=True)
