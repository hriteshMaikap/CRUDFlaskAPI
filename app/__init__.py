from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_mail import Mail

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    from app.routes.planets import planets_bp
    from app.routes.users import users_bp
    app.register_blueprint(planets_bp, url_prefix='/api/planets')
    app.register_blueprint(users_bp, url_prefix='/api/users')

    return app