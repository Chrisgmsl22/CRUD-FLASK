from flask import Flask, render_template, request, url_for, redirect
from flask_migrate import Migrate
from database import db
from forms import PersonaForm
from models import Persona

app = Flask(__name__)

# Configuracion de la base de datos
USER_DB = 'postgres'
PASS_DB = 'admin'
URL_DB = 'localhost'
NAME_DB = 'sap_flask_db'
FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

# Configuracion para la conexion a la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
# Configuracion para que no salga un warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializamos nuestro objeto db de SQLAlchemy
# db = SQLAlchemy(app)
db.init_app(app)

# Configuracion de flask-migrate
migrate = Migrate()
migrate.init_app(app, db) # Le pasamos la app y la base de datos

# Configuracion de flask-wtf
app.config['SECRET_KEY'] = 'llave_secreta'




@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    # Recuperamos los objetos de tipo persona
    personas = Persona.query.order_by('id')
    total_personas = Persona.query.count()
    # Ordenamos las personas por id
    app.logger.debug(f'Listado de personas: {personas}')
    app.logger.debug(f'Numero de personas: {total_personas}')

    return render_template('index.html', personas=personas, total_personas=total_personas)

@app.route('/ver/<int:id>')
def ver_detalle(id):
    # Recuperamos la persona por id
    persona = Persona.query.get_or_404(id)
    app.logger.debug(f'Ver persona: {persona}')
    return render_template('detalle.html', persona=persona)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    persona = Persona()
    personaForm = PersonaForm(obj=persona) # Le pasamos el objeto persona
    if request.method == 'POST': # Es metodo post?
        if personaForm.validate_on_submit(): # Es valido el formulario?
            personaForm.populate_obj(persona) # Llenamos el objeto persona con los datos del form
            app.logger.debug(f'Persona a insertar: {persona}')
            # Usamos sqlalchemy para agregar la persona a la base de datos
            db.session.add(persona) # Agregamos la persona a la base de datos
            db.session.commit() # Guardamos los cambios
            return redirect(url_for('index'))

    return render_template('agregar.html', forma=personaForm) # Le pasamos la form

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    persona = Persona.query.get_or_404(id)
    personaForm = PersonaForm(obj=persona)
    if request.method == 'POST':
        if personaForm.validate_on_submit():
            personaForm.populate_obj(persona)
            app.logger.debug(f'Persona a editar: {persona}')
            db.session.commit()
            return redirect(url_for('index'))

    return render_template('editar.html', forma=personaForm)


@app.route('/eliminar/<int:id>')
def eliminar(id):
    persona = Persona.query.get_or_404(id)
    app.logger.debug(f'Persona a eliminar: {persona}')
    db.session.delete(persona)
    db.session.commit()
    return redirect(url_for('index'))