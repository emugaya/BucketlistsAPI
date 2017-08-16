giimport os

class Config(object):
    """
    Common configurations
    """
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'Some_long_text_here'
    # SQLALCHEMY_DATABASE_URI = 'sqlite://:memory:app'
    SQLALCHEMY_DATABASE_URI = "postgresql://buckelist_db:bucketlist001@localhost/buckelist_db"

class ProductionConfig(Config):

    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost/bucketlist_db"


class DevelopmentConfig(Config):
    """
    Development configurations
    """
    DEBUG = True
    SQLALCHEMY_ECHO = True
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_DATABASE_URI = "postgres://vohsudxlhkvkvz:24c07d9f20407614a4a6aa463235a34a5ae2f3c9aa452ce38915fca51d446210@ec2-54-75-239-190.eu-west-1.compute.amazonaws.com:5432/d7d7jfgb4midv"

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
