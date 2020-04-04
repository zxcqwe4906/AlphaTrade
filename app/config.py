import os

class Config:
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or '127.0.0.1'
    ALEMBIC_MYSQL_HOST = os.environ.get('ALEMBIC_MYSQL_HOST') or '127.0.0.1'
    MYSQL_PORT = os.environ.get('MYSQL_PORT') or 4306
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE') or 'alpha_trade'
    MYSQL_USERNAME = os.environ.get('MYSQL_USERNAME') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or ''

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}{}@{}:{}/{}'.format(
        MYSQL_USERNAME,
        f':{MYSQL_PASSWORD}' if len(MYSQL_PASSWORD) > 0 else '',
        MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
