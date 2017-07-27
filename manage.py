import os

from flask_script import Manager # class for handling a set of commands
from flask_migrate import Migrate, MigrateCommand
#local imports
from app import db, create_app
from app import models
# from app import models
# config_name = 'development' #uncomment to implement migrations for heroku app
app = create_app(config_name)
app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
