
from app import app
from controllers.device import *

@app.route('/', methods=['GET', 'POST'])
def index():
    return "Welcome"

if __name__ == '__main__':
    app.run()