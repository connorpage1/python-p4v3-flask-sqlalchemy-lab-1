# server/app.py
#!/usr/bin/env python3
from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_earthquake_by_id(id):
    earthquake = db.session.get(Earthquake, id)
    
    if earthquake:
        response_body = earthquake.to_dict()
        response_code = 200
    else:
        response_body = {'message': f'Earthquake {id} not found.'}
        response_code = 404
    
    return make_response(response_body, response_code)

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquake_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    quakes = [quake.to_dict() for quake in earthquakes]
    
    response_body = {'count' : len(quakes), 'quakes': quakes}
    
    return make_response(response_body, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
