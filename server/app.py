from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/')
def index():
    return 'Hello, World!'

# Define a controller class for your routes
class Plants(Resource):
    def get(self):
        # Implement the Index Route
        plants = Plant.query.all()
        return jsonify([plant.to_dict() for plant in plants])

    def post(self):
        # Implement the Create Route
        data = request.get_json()
        name = data.get('name')
        image = data.get('image')
        price = data.get('price')

        if not name or not image or price is None:
            return make_response(jsonify({'error': 'Missing data'}), 400)

        new_plant = Plant(name=name, image=image, price=price)
        db.session.add(new_plant)
        db.session.commit()

        # Create a dictionary with the response data
        response_data = {
            'id': new_plant.id,
            'name': new_plant.name,
            'image': new_plant.image,
            'price': new_plant.price
        }

        return jsonify(response_data), 201

class PlantByID(Resource):
    def get(self, id):
        # Implement the Show Route
        plant = Plant.query.get(id)
        if not plant:
            return make_response(jsonify({'error': 'Plant not found'}), 404)

        return jsonify(plant.to_dict())

# Add routes to the API
api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
