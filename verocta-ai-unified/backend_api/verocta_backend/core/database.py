"""
Database configuration and setup
SQLAlchemy with PostgreSQL support
"""

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData

# SQLAlchemy instance
db = SQLAlchemy(metadata=MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
))

migrate = Migrate()


def init_db(app):
    """Initialize database with app"""
    db.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        # Create tables if they don't exist
        if app.config.get('DATABASE_URL'):
            db.create_all()


def get_db():
    """Get database session"""
    return db.session