class Config(object):
    """
    Common configurations
    """
    DEBUG = False
    TESTING = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:app'
    SQLALCHEMY_DATABASE_URI = "postgresql://buckelist_db:bucketlist001@localhost/buckelist_db"

class ProductionConfig(Config):

    SQLALCHEMY_DATABASE_URI = "postgresql://buckelist_db:bucketlist001@localhost/buckelist_db"


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost/bucketlist_db"

class TestingConfig(Config):
    """
    Testing configurations
    """
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost/test_db"

app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
