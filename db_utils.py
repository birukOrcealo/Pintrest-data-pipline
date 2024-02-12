import sqlalchemy
from sqlalchemy import text


class AWSDBConnector:
    """
    A class to handle the connection to the AWS RDS database.
    """


    def __init__(self):
        """
        Initializes the AWSDBConnector with the database connection details.
        """
        self.HOST = "pinterestdbreadonly.cq2e8zno855e.eu-west-1.rds.amazonaws.com"
        self.USER = 'project_user'
        self.PASSWORD = ':t%;yCY3Yjg'
        self.DATABASE = 'pinterest_data'
        self.PORT = 3306
        
    def create_db_connector(self):
        """
        Creates and returns a SQLAlchemy engine for connecting to the database.
        
        Returns:
            engine (sqlalchemy.engine.base.Engine): A SQLAlchemy engine object.
        """
        engine = sqlalchemy.create_engine(f"mysql+pymysql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.DATABASE}?charset=utf8mb4")
        return engine