from functools import reduce
from math import pi

from flask import Flask, redirect, render_template, request, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Set a secret key for session security
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

# Initialize Bootstrap for your app
Bootstrap(app)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///history.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Define the database model
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    forma = db.Column(db.String(10), nullable=False)
    material = db.Column(db.String(15), nullable=False)
    measures = db.Column(db.String(10), nullable=False)
    mm_inch = db.Column(db.String(5), nullable=False)
    result = db.Column(db.String(35), nullable=False)


# Create the database tables
db.create_all()


@app.route('/',  methods=['GET', 'POST'])
def get_result():
    # Process form data and save to the database
    lista = request.form.getlist('measure')
    forma = request.form.get('forma')
    material = request.form.get('material')
    mm_inch = request.form.get('mm_inch', 'inch')

    good_list = []
    for i in lista:
        if i == '':
            i = float(0)
        else:
            i = float(i)
        good_list.append(i)

    # Calculate volume and mass
    # Get ro
    ro = 0
    if material == 'Alum':
        ro = 2.7
    elif material == 'Stl№45':
        ro = 7.8
    elif material == 'Stless':
        ro = 7.9

    # Get V
    v = 0
    if forma == "block":
        v = reduce(lambda x, y: x * y, good_list, 1)
    elif forma == "cylinder":
        v = pi * (good_list[0] ** 2) * good_list[1]
    elif forma == "tube":
        v = pi / 4 * (2 * (good_list[1] ** 2) -
                      2 * (good_list[0] ** 2)) * good_list[2]
    elif forma == "ball":
        v = 4 / 3 * pi * (good_list[0] ** 3)

    if mm_inch == "mm":
        v = v / 1000
    elif mm_inch == "inch":
        v = v * 16.387064

    # Get M
    m = ro * v / 1000  # kg
    m_kg = round(m, 4)
    m_lbs = round(m * 2.2046226218, 4)

    if request.method == 'POST':
        note = History(
            forma=forma.capitalize(),
            material=material,
            measures=', '.join(lista),
            mm_inch=mm_inch,
            result=f'{m_kg} kg / {m_lbs} lbs',
        )
        db.session.add(note)
        db.session.commit()

    notes = db.session.query(History).all()
    return render_template("index.html", result=f'{m_kg} kg / {m_lbs} lbs', notes=notes[-9:])


@app.route("/delete")
def delete():
    # Delete a note by ID
    note_id = request.args.get('id')
    note = History.query.get(note_id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('get_result'))


@app.route("/delete_all")
def delete_all():
    # Delete all notes
    db.session.query(History).delete()
    db.session.commit()
    return redirect(url_for('get_result'))


if __name__ == "__main__":
    app.run(debug=True)
