

class DefaultConfig:
    SECRET_KEY = b'_5#y2L"F4Q8z\n\xec/'
    JWT_AUTH_URL_RULE = '/api/v1/auth/login'
    JWT_AUTH_USERNAME_KEY = 'email'


class DevelopmentConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = 'postgresql:///bookameal'


class ProductionConfig(DefaultConfig):
    pass


class TestingConfig(DefaultConfig):
    SQLALCHEMY_DATABASE_URI = 'postgresql:///test'
    TESTING=True
    DEBUG=True


app_config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
