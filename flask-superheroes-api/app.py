from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_mail import Mail, Message
from models import db, Hero, Power, HeroPower
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')

db.init_app(app)
migrate = Migrate(app, db)
mail = Mail(app)


@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_list = [hero.to_dict(only=('id', 'name', 'super_name')) for hero in heroes]
    return jsonify(heroes_list), 200


@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    
    hero_dict = hero.to_dict(only=(
        'id', 
        'name', 
        'super_name', 
        'hero_powers.id',
        'hero_powers.hero_id',
        'hero_powers.power_id',
        'hero_powers.strength',
        'hero_powers.power.id',
        'hero_powers.power.name',
        'hero_powers.power.description'
    ))
    
    return jsonify(hero_dict), 200


@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_list = [power.to_dict(only=('id', 'name', 'description')) for power in powers]
    return jsonify(powers_list), 200


@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    
    if not power:
        return jsonify({"error": "Power not found"}), 404
    
    power_dict = power.to_dict(only=('id', 'name', 'description'))
    return jsonify(power_dict), 200


@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    
    if not power:
        return jsonify({"error": "Power not found"}), 404
    
    data = request.get_json()
    
    try:
        if 'description' in data:
            power.description = data['description']
        
        db.session.commit()
        
        power_dict = power.to_dict(only=('id', 'name', 'description'))
        return jsonify(power_dict), 200
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400


@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    
    try:
        hero = Hero.query.get(data.get('hero_id'))
        power = Power.query.get(data.get('power_id'))
        
        if not hero:
            return jsonify({"errors": ["Hero not found"]}), 400
        if not power:
            return jsonify({"errors": ["Power not found"]}), 400
        
        hero_power = HeroPower(
            strength=data.get('strength'),
            hero_id=data.get('hero_id'),
            power_id=data.get('power_id')
        )
        
        db.session.add(hero_power)
        db.session.commit()
        
        hero_power_dict = hero_power.to_dict(only=(
            'id',
            'hero_id',
            'power_id',
            'strength',
            'hero.id',
            'hero.name',
            'hero.super_name',
            'power.id',
            'power.name',
            'power.description'
        ))
        
        return jsonify(hero_power_dict), 201
        
    except ValueError as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400


@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.get_json()
        msg = Message(
            subject=data.get('subject', 'Test Email'),
            recipients=[data.get('recipient')],
            body=data.get('body', 'This is a test email from Flask Superheroes API')
        )
        mail.send(msg)
        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5555, debug=True)