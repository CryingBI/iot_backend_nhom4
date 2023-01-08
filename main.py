
from app import app
from controllers.customdevice import *

@app.route('/', methods=['GET', 'POST'])
def index():
    return "Welcome"

if __name__ == '__main__':
    app.run()