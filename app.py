from flask import Flask
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager

app = Flask(__name__)

#app.config["JWT_SECRET_KEY"] = "iot_nhom9_2023"
#jwt = JWTManager(app)

app.config["JWT_SECRET_KEY"] = "iot_nhom9_2023"
jwt = JWTManager(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# @app.after_request
# def after_request(response):
#   response.headers.add('Access-Control-Allow-Origin', '*')
#   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#   response.headers.add('Access-Control-Allow-Credentials', 'true')
#   return response


