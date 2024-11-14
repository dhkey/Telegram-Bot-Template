from typing import Optional
from databaseConnection import connection

tableName = 'users'

def initialization() -> None:
    connection.execute(f"""
            CREATE TABLE IF NOT EXISTS {tableName} (
                user_id BIGINT PRIMARY KEY,
                language_code VARCHAR(5),
                subscription VARCHAR(10),
                status VARCHAR(10), 
                isfFirstLogin BOOLEAN DEFAULT 1
            ) """)

    connection.logger.info(f"Table name: {tableName} ::: Initialization completed ✅")

class User:
    def __init__(self, user_id) -> None:
        self.connection = connection
    
        self.user_id = user_id
    
    def createNewUser(self) -> bool:
        query = f"""
            INSERT IGNORE INTO {tableName} (
                user_id, language_code, subscription, status, isfFirstLogin
            ) VALUES ( %(user_id)s, %(language_code)s, %(subscription)s, %(status)s, %(isfFirstLogin)s)"""
        
        params = {
            'user_id' : self.user_id,
            'language_code' : "uk",
            'subscription' : "free",
            'status' : "member",
            'isfFirstLogin' : True
        }
        
        self.connection.execute(query, params)
        
        if self.isUserFirstLogin():
            self.connection.logger.info(f"Table name: {tableName} ::: new user has been created.")
            
            self.connection.execute(
                query = f"UPDATE {tableName} SET isfFirstLogin = %(isfFirstLogin)s WHERE user_id = %(user_id)s",
                params = {
                    'user_id' : self.user_id,
                    'isfFirstLogin': False
                    }
            )
            
            return True
        else:
            return False
        
    
    def isUserInDatabase(self) -> bool:
        language_code = self.connection.fetchOne(
            f"""SELECT user_id FROM {tableName} 
                WHERE user_id = %(user_id)s""",
            {'user_id': self.user_id} )
        
        return True if language_code != None else False
    
    def getUserLanguageCode(self) -> Optional[str]:
        language_code = self.connection.fetchOne(
            f"""SELECT language_code FROM {tableName} 
                WHERE user_id = %(user_id)s""",
            {'user_id': self.user_id} )
        
        return language_code

    def isUserFirstLogin(self) -> bool:
        firstLoginStatus = self.connection.fetchOne(
            f"""SELECT isfFirstLogin FROM {tableName} 
                WHERE user_id = %(user_id)s""",
            {'user_id': self.user_id} )
        
        return firstLoginStatus if firstLoginStatus != None else 0
