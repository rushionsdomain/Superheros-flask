from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)

@app.route('/')
def index():
    return '<h1>Code Challenge API</h1>'

# API Resource for Heroes
class HeroResource(Resource):
    def get(self, hero_id=None):
        if hero_id:
            hero = Hero.query.get_or_404(hero_id)
            return make_response(hero.to_dict(), 200)
        
        # Retrieve all heroes if no ID is provided
        heroes = Hero.query.all()
        return make_response(jsonify([hero.to_dict() for hero in heroes]), 200)

    def post(self):
        data = request.get_json()

        # If the request body is a list, insert multiple heroes
        if isinstance(data, list):
            new_heroes = [Hero(name=hero['name'], super_name=hero['super_name']) for hero in data]
            db.session.add_all(new_heroes)
        else:
            # Insert a single hero if data is not a list
            new_hero = Hero(name=data['name'], super_name=data['super_name'])
            db.session.add(new_hero)

        db.session.commit()
        return make_response({"message": "Heroes added successfully"}, 201)

api.add_resource(HeroResource, '/heroes', '/heroes/<int:hero_id>')

# API Resource for Powers
class PowerResource(Resource):
    def get(self, power_id):
        power = Power.query.get_or_404(power_id)
        return make_response(power.to_dict(), 200)

    def post(self):
        data = request.get_json()
        new_power = Power(name=data['name'], description=data['description'])
        db.session.add(new_power)
        db.session.commit()
        return make_response(new_power.to_dict(), 201)

api.add_resource(PowerResource, '/powers', '/powers/<int:power_id>')

# API Resource for HeroPower
class HeroPowerResource(Resource):
    def get(self, hero_power_id):
        hero_power = HeroPower.query.get_or_404(hero_power_id)
        return make_response(hero_power.to_dict(), 200)

    def post(self):
        data = request.get_json()
        new_hero_power = HeroPower(
            strength=data['strength'], hero_id=data['hero_id'], power_id=data['power_id']
        )
        db.session.add(new_hero_power)
        db.session.commit()
        return make_response(new_hero_power.to_dict(), 201)

api.add_resource(HeroPowerResource, '/hero_powers', '/hero_powers/<int:hero_power_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
