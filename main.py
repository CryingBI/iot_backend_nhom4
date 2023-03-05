
from app import *
from controllers.device import *
from controllers.login import login
from controllers.user import *
from controllers.room import *
from controllers.house import *

# @app.after_request
# def after_request(response):
#   response.headers.add('Access-Control-Allow-Origin', '*')
#   response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#   response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#   response.headers.add('Access-Control-Allow-Credentials', 'true')
#   return response

@app.route('/', methods=['GET', 'POST'])
def index():
    return "Welcome"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug='on')