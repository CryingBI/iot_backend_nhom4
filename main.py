
from app import app
from controllers.device import *

@app.route('/', methods=['GET', 'POST'])
def index():
    return "Welcome"

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)