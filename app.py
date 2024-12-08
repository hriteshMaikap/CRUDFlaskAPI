from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message


app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
# Looking to send emails in production? Check out our Email API/SMTP product!
app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'b215da3b2e9b6f'
app.config['MAIL_PASSWORD'] = '29e9b4434af93d'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print("Database created successfully!")


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print("Database dropped successfully!")


@app.cli.command('db_seed')
def db_seed():
    mercury = Planets(planet_name='Mercury',
                      planet_type='CLASS D',
                      home_star='Sol',
                      mass=3.258e23,
                      radius=1516,
                      distance=35.968e6)

    venus = Planets(planet_name='Venus',
                      planet_type='CLASS K',
                      home_star='Sol',
                      mass=4.258e23,
                      radius=3760,
                      distance=67.968e6)

    earth = Planets(planet_name='Earth',
                      planet_type='CLASS M',
                      home_star='Sol',
                      mass=5.258e23,
                      radius=3959,
                      distance=69.968e6)

    db.session.add(mercury)
    db.session.add(venus)
    db.session.add(earth)

    test_user = Users(first_name='Test',
                     last_name='Maikap',
                     email='test@test.com',
                     password='p@ssw0rd')

    db.session.add(test_user)
    db.session.commit()
    print("Database seeded successfully!") 

@app.route('/')
def hello():
    return 'Hello world!'


@app.route('/route')
def first_route():
    return jsonify(message='This is your first route. Lets see if it prints this and this') 
#this is key value pair message: "actual message"


@app.route('/parameters')
def parameters():
    name = request.args.get('name')
    val1 = int(request.args.get('val1'))
    val2 = int(request.args.get('val2'))

    if(val1+val2>20):
        return jsonify(message="The output is valid " + name)
    else:
        return jsonify(message="The output is invalid " + name), 401


@app.route('/url_variables/<string:name>/<int:age>')
def url_variables(name: str, age: int):
    if age<18:
        return jsonify(message="You are not authenticated " + name), 401
    else:
        return jsonify(message="You are authenticated " + name)


'''
METHOD 1 to serialize ORM Objects fro,m SQLAlchemy
def serialize_planet(planet):
    return {
        "id": planet.planet_id,
        "name": planet.planet_name,
        "type": planet.planet_type
    }

@app.route('/planets', methods=['GET'])
def planets():
    planets_list = Planets.query.all()
    serialized_planets = [serialize_planet(planet) for planet in planets_list]
    return jsonify(serialized_planets)'''

@app.route('/planets', methods=['GET'])
def planets():
    planets_list = Planets.query.all()
    result = planets_schema.dump(planets_list)
    return jsonify(result)


@app.route('/register', methods = ['POST'])
def register():
    email = request.form['email']
    test = Users.query.filter_by(email=email).first()
    if test:
        return jsonify(message="User already exists!"), 409 
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = Users(first_name=first_name, last_name=last_name, password=password, email=email)
        db.session.add(user)
        db.session.commit()
        return jsonify(message="User Registered Successfully!")
     

@app.route('/login', methods = ['POST'])
def login():
    #take only json input
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = Users.query.filter_by(email=email, password=password).first()
    if test:
        access_token = create_access_token(identity=email)
        return jsonify(message="Login Successful!", access_token=access_token)
    else:
         return jsonify(message="Incorrect Username or Password"), 401


@app.route('/forgot_password/<string:email>', methods=['GET'])
def forgot_password(email: str):
    user = Users.query.filter_by(email=email).first()
    if user:
        msg = Message("Your planetary-api password is: " + user.password,
                      sender="admin@planetary-api.com",
                      recipients=[email])
        mail.send(msg)
        return jsonify(message="Password has been sent to " + email)
    else:
        return jsonify(message="The given email doesn't exist!")

@app.route('/planet_details/<int:planet_id>', methods=["GET"])
def planet_details(planet_id: int):
    planet = Planets.query.filter_by(planet_id=planet_id).first()
    if planet:
        result = planet_schema.dump(planet)
        return jsonify(result)
    else:
        return jsonify(message="Given planet does not exist")


@app.route('/add_planet', methods=['POST'])
@jwt_required() #ensures only logged in person can add data
def add_planet():
    planet_name = request.form['planet_name']
    test = Planets.query.filter_by(planet_name=planet_name).first()
    if test:
        return jsonify("Planet with that name already exists!"), 409
    else:
        planet_type = request.form['planet_type']
        home_star = request.form['home_star']
        mass = request.form['mass']
        radius = request.form['radius']
        distance = request.form['distance']

        new_planet = Planets(planet_name=planet_name,
                            planet_type=planet_type,
                            home_star=home_star,
                            mass=mass,
                            radius=radius,
                            distance=distance)
        db.session.add(new_planet)
        db.session.commit()
        return jsonify("New Planet Added!"), 201
    

@app.route('/update_planet', methods=['PUT'])
@jwt_required()
def update_planet():
    planet_id = request.form['planet_id']
    planet = Planets.query.filter_by(planet_id=planet_id).first()
    if planet:
        planet.planet_name = request.form['planet_name']
        planet.planet_type = request.form['planet_type']
        planet.home_star = request.form['home_star']
        planet.mass = request.form['mass']
        planet.radius = request.form['radius']
        planet.distance = request.form['distance']
        db.session.commit() #there is no db.session.update() method
        return jsonify(Message="You updated a planet")
    else:
        return jsonify(Message="The given planet does not exist")


@app.route('/delete_planet/<int:planet_id>',methods=['DELETE'])
@jwt_required()
def delete_planet(planet_id: int):
    planet = Planets.query.filter_by(planet_id=planet_id).first()
    if planet:
        db.session.delete(planet)
        db.session.commit()
        return jsonify(message="You deleted the planet"), 202
    else:
        return jsonify(message="Your planet does not exist"), 404
    
    
#database models
class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(Integer, primary_key=True)
    first_name = db.Column(String)
    last_name = db.Column(String)
    email = db.Column(String, unique=True)
    password = db.Column(String)


class Planets(db.Model):
    __tablename__ = 'planets'
    planet_id = db.Column(Integer, primary_key=True)
    planet_name = db.Column(String)
    planet_type = db.Column(String)
    home_star = db.Column(String)
    mass = db.Column(Float)
    radius = db.Column(Float)
    distance = db.Column(Float) 


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')

class PlanetSchema(ma.Schema):
    class Meta:
        fields = ('planet_id', 'planet_name', 'planet_type', 'home_star', 'mass', 'radius', 'distance')

user_schema = UserSchema() #getting one record back
users_schema = UserSchema(many=True) #getting multiple records back
planet_schema = PlanetSchema() 
planets_schema = PlanetSchema(many=True) 

if __name__ == '__main__':
    app.run(debug=True)