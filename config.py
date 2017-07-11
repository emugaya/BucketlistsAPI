class Config(object):
    """
    Common configurations
    """
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'

class ProductionConfig(Config):

    SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost/spaceshipDB"


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "postgresql://buckelist_db:bucketlist001@localhost/buckelist_db"

class TestingConfig(Config):
    """
    Testing configurations
    """
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:'

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
