import os

class Config:
    mysql_db_host = os.environ.get("MYSQL_DB_HOST", default=True)
    SECRET_KEY = 'c425c9dd864d5737847c93f14fed0b0191924ab035886713f8d16f265159fb05'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///sonblogdata.db'
    # SQLALCHEMY_DATABASE_URI = 'mysql://phani:123456@172.20.10.6/son_blog'
    if mysql_db_host:
        SQLALCHEMY_DATABASE_URI = 'mysql://root:Phani_123@' + mysql_db_host.lower() + '/son_blog'
    else:
        SQLALCHEMY_DATABASE_URI = 'mysql://phani:123456@sonblogdb/son_blog'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'kondapalliphaniteja@gmail.com'
    MAIL_PASSWORD = ''
