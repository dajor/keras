import os
from app import create_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.models import Image

#app = create_app(os.getenv('FLASK_CONFIG') or 'development')
app = create_app()
manager = Manager(app)

if __name__ == '__main__':
    print(("* Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))
    #manager.run()
    app.run(host='0.0.0.0')
