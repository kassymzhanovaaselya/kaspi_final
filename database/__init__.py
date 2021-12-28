from database.database import Database
from configs import configs

DB = Database(connection=configs['db_conn'])
