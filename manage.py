import os
from app import create_app
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app.models import Image

#app = create_app(os.getenv('FLASK_CONFIG') or 'development')
app = create_app()
manager = Manager(app)

if __name__ == '__main__':
    manager.run()