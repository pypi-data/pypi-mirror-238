from flask import Flask


def get_sqlalchemy_db_url():
    try:
        app = Flask(__name__, template_folder="templates")
        config_file_location = None
        with app.app_context():
            if config_file_location:
                app.config.from_pyfile(config_file_location, silent=False)
            else:
                app.config.from_pyfile('../config/dev.cfg', silent=True)
                # app.config.from_pyfile('../config/prp.cfg', silent=True)

        sqlalchemy_database_url = app.config.get('SQLALCHEMY_DATABASE_URI')
        return sqlalchemy_database_url
    except Exception as e:
        return None
