import os

class DefaultConfig:
    SECRET_KEY=os.environ.get("SECRET_KEY")

class DevelopmentConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("DEVELOPMENT_SQLALCHEMY_DATABASE_URI")
    FLASK_DEBUG=True

class ProductionConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("PRODUCTION_SQLALCHEMY_DATABASE_URI")
    TESTING=False
    FLASK_DEBUG=False


class TestingConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = os.environ.get("TESTING_SQLALCHEMY_DATABASE_URI")
    TESTING=True
    FLASK_EBUG=True


app_config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
