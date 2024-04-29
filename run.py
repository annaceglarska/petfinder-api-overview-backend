import os
import configparser

from app.factory import create_app

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join("config.ini")))

if __name__ == '__main__':
    app = create_app()
    app.config['DEBUG'] = True
    app.config['MONGO_URI'] = config['DEV']['DB_URI']

    app.config['JWT_SECRET_KEY'] = config['DEV']['JWT_SECRET_KEY']
    app.config['PETFINDER_API_SECRET_KEY'] = config['DEV']['PETFINDER_API_SECRET_KEY']
    app.config['PETFINDER_API_CLIENT_ID'] = config['DEV']['PETFINDER_API_CLIENT_ID']

    app.run()
