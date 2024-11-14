import mysql.connector
from config_reader import get_config, DatabaseConfig
from structlog.typing import FilteringBoundLogger
import structlog
from typing import Tuple, Dict, Any, Optional

class Connection:
    
    def __init__(self) -> None:
        
        database_config: DatabaseConfig = get_config(model=DatabaseConfig, root_key="database")
        self.logger: FilteringBoundLogger = structlog.get_logger()

        try:
            self.connection = mysql.connector.connect(
                host = database_config.DB_HOST.get_secret_value(),
                user = database_config.DB_USER.get_secret_value(),
                password = database_config.DB_PASSWORD.get_secret_value(),
                database = database_config.DB_NAME,
                buffered=True
            )
            self.logger.info(f"Connected to [{database_config.DB_NAME}] database ✅")
        except mysql.connector.errors.DatabaseError:
            self.logger.error("Error while connecting to database... exiting...")
            exit(0) 

        self.cursor = self.connection.cursor()
        
    def commit(self) -> None:
        self.connection.commit()
    
    def execute(self, query, params=None) -> None:
        self.cursor.execute(query, params) if params else self.cursor.execute(query)
        self.commit()
    
    def fetchOne(self, query, params=None) -> Optional[Any]:
        self.execute(query, params)
        result = self.cursor.fetchone()

        if not result:
            return None
        elif len(result) > 1:
            return result
        elif len(result) == 1:
            return result[0]
    

    def fetchAll(self, query, params=None) -> Tuple[Dict[str, Any]]:
        return self.cursor.fetchall(query, params)
    
    def closeConnection(self) -> None:
        self.logger.info("Closing connection...")
        self.connection.close()
        self.logger.info("Closed ✅")