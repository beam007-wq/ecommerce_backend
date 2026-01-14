import pymysql
from configparser import ConfigParser

config = ConfigParser()
config.read(["config.ini"])
DBconfig = config["ecommerce_db"]

ecommerce_conn = pymysql.connect(
    host = DBconfig.get("host"),
    port = DBconfig.getint("port"),
    user = DBconfig.get("user"),
    password = DBconfig.get("password"),
    database = DBconfig.get("database")
)

def sql_operation(sql: str,mode: str,value: list | tuple | None = None,):
    with ecommerce_conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(sql,value)    
        match mode:
            case "FA":
                return cursor.fetchall()
            case "FO":
                return cursor.fetchone()
            case "CM":
                ecommerce_conn.commit()
                return True