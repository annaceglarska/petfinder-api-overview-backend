import os
import configparser

from app.factory import create_app

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join("config.ini")))

if __name__ == '__main__':
    app = create_app()
    app.config['DEBUG'] = True
    app.config['MONGO_URI'] = config['DEV']['DB_URI']

    app.run()
