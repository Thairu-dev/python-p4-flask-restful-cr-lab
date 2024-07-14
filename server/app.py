#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        # Implement GET /plants route
        plants = Plant.query.all()
        plants_list = [plant.to_dict() for plant in plants]
        return make_response(jsonify(plants_list), 200)

    def post(self):
        # Implement POST /plants route
        data = request.get_json()
        if 'name' not in data or 'image' not in data or 'price' not in data:
            return make_response(jsonify({"error": "Missing required fields"}), 400)

        new_plant = Plant(name=data['name'], image=data['image'], price=data['price'])
        db.session.add(new_plant)
        db.session.commit()
        return make_response(jsonify(new_plant.to_dict()), 201)

class PlantByID(Resource):
    def get(self, id):
        # Implement GET /plants/:id route
        plant = Plant.query.get(id)
        if plant is None:
            return make_response(jsonify({"error": "Plant not found"}), 404)
        return make_response(jsonify(plant.to_dict()), 200)

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

