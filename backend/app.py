from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from models import db



from models import *
from auth import auth
from routes import routes

app = Flask(__name__)


@app.get('/')
def home():
  return "hello world"

# Database configuration (replace with your own PostgreSQL credentials)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2001@localhost:5432/timemanagement'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'a3T&hD@9d%L1oWpF*!rCxYkNvQz98J^&'


# db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)




 

app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(routes, url_prefix='/routes')

 

if __name__ == "__main__":
  with app.app_context():
    db.create_all()  

    app.run(debug=True)


