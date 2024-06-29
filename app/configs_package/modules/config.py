import os

class Config:
    DEBUG = False
    TESTING = False
    DB_SERVER = os.environ.get('DB_SERVER')

    @property
    def DATABASE_URI(self):  # Note: all caps
        return f"mysql://user@{self.DB_SERVER}/foo"

class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY= os.getenv('SECRET_KEY') # KEY GENERATED WITH secrets.token_urlsafe(32) 32 byts
    OTP_SECRET_KEY= os.getenv('OTP_SECRET_KEY')

    #@property
    #def SQLALCHEMY_DATABASE_URI(self):
        #return "sqlite:///test3.db"
    def __init__(self, database_type = 'sqlite') -> None:
        super().__init__()
        self.database_type = database_type

        if self.database_type == 'mysql':
            pass
        elif self.database_type == 'postgres':
            pass
        else:
            @property
            def SQLALCHEMY_DATABASE_URI(self):
                return "sqlite:///test3.db"

    def load_configs(self):
        if self.database_type == 'mysql':
            pass
        elif self.database_type == 'postgres':
            pass
        else:
            pass

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'