import os

from app import app

config_name = os.getenv('FLASK_CONFIG')

if __name__ == '__main__':
    app.run()
