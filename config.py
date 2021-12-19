import os


class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    CSRF_ENABLED = True
    # import secrets
    # secrets.token_hex()
    CSRF_SESSION_KEY = 'ebd8623d749c18e635647d5cfdbec3f8c4790199b157d9c041027676c768701a'
    SECRET_KEY = 'dc587e979e9e14e5d4d0a993bd138fe0a918dfb5f851a70fcd4d6b307fdafe5f'


class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ...
    DATABASE = ...


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(Config.BASE_DIR, 'geo_service.db')
    DATABASE = 'sqlite:///' + os.path.join(Config.BASE_DIR, 'geo_service.db')
