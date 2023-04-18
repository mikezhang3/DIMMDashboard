from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from scripts import create_app, db
from scripts import constants
#创建flask 的应用对象
app = create_app(constants.CONFIG_MODE)


print(app.url_map)
manager = Manager(app)
Migrate(app,db)



manager.add_command("db",MigrateCommand)
if __name__ == '__main__':
    manager.run()
