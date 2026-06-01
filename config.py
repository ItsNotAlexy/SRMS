class Config:
    SECRET_KEY = 'secretkey123'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/srms_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False