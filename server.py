import os
from dotenv import load_dotenv
from flask import Flask
from database.db_manager import db
from routes.auth import auth_bp
from routes.tickets import tickets_bp
from routes.admin import admin_bp

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(auth_bp)
app.register_blueprint(tickets_bp)
app.register_blueprint(admin_bp)


if __name__ == '__main__':
    app.run(debug=True)