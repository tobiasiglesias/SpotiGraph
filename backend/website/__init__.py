# from flask import Flask
# from os import path
# from .models import Artist, Track, Colab
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker


# DB_NAME = "db.sqlite3"

# # Crear una conexión a la base de datos
# engine = create_engine(f"sqlite:///{DB_NAME}", echo=False)

# # Crear una sesión de base de datos
# Session = sessionmaker(bind=engine, autoflush=False)
# session = Session()


# def create_app():
#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = 'SDKLJFLSKD'
#     app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

#     # Crear las tablas en la base de datos si no existen
#     if not path.exists(f'website/{DB_NAME}'):
#         with app.app_context():
#             print("Creando las tablas en la base de datos...")
#             Artist.__table__.create(bind=engine, checkfirst=True)
#             Track.__table__.create(bind=engine, checkfirst=True)
#             Colab.create(bind=engine, checkfirst=True)

#     return app


from flask import Flask
from os import path
from flask_sqlalchemy import SQLAlchemy

DB_NAME = "db.sqlite3"

# Crear una instancia de SQLAlchemy
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'SDKLJFLSKD'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar la extensión SQLAlchemy con la aplicación
    db.init_app(app)

    # Crear las tablas en la base de datos si no existen
    from .models import Artist, Track, Colab
    with app.app_context():
        print("creando tablas")
        db.create_all()
        db.reflect()

    return app
