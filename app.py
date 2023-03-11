from flask import Flask
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "iot_nhom9_2023"
jwt = JWTManager(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})



