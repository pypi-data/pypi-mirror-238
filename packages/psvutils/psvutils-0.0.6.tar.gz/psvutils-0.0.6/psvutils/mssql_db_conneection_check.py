import re
from typing import Dict, Optional, Tuple

import pyodbc
import win32security
from pydantic import BaseModel, Field


class DatabaseConfig(BaseModel):
    username: str
    password: str
    windows_integrated_auth: bool = Field(default=False)
    domain: Optional[str] = Field(default="")
    server_name: str
    database: str
    driver_name: str
    query: Optional[str] = Field(default="SELECT * FROM sys.tables")




def dataBaseConnection(databaseConfigs):
    username = databaseConfigs['username']
    password = databaseConfigs['password']
    windows_integrated_auth = databaseConfigs['windows_integrated_auth']
    domain = databaseConfigs['domain']
    server_name = databaseConfigs['server_name']
    database = databaseConfigs['database']
    # sql_query = databaseConfigs.sql_query
    driver_name = databaseConfigs['driver_name']
    databaseCursor = None
    databaseConnection = None
    try:
        if windows_integrated_auth != None and str(windows_integrated_auth).lower() == 'true':
            handler = win32security.LogonUser(username, domain, password, win32security.LOGON32_LOGON_NEW_CREDENTIALS, win32security.LOGON32_PROVIDER_WINNT50)
            win32security.ImpersonateLoggedOnUser(handler)
        try:
            if windows_integrated_auth != None and str(windows_integrated_auth).lower() == 'true':
                if database == None or database == "":
                    conn = pyodbc.connect('Driver={' + driver_name + '};Server='+server_name+';Trusted_Connection=yes;TrustServerCertificate=yes;')
                else:
                    conn = pyodbc.connect('Driver={' + driver_name + '};Server=' + server_name + ';Database=' + database + ';Trusted_Connection=yes;TrustServerCertificate=yes;')
            else:
                if database == None or database == "":
                    conn = pyodbc.connect('Driver={' + driver_name + '};Server='+server_name+ ';uid=' + username + ';pwd=' + password + ';TrustServerCertificate=yes;')
                else:
                    conn = pyodbc.connect('Driver={' + driver_name + '};Server=' + server_name + ';Database=' + database + ';uid=' + username + ';pwd=' + password + ';TrustServerCertificate=yes;')
            databaseConnection = conn
            databaseCursor = databaseConnection.cursor()
        except Exception as errorMessage:
            return None,None
    except Exception as e:
        if windows_integrated_auth != None and str(windows_integrated_auth).lower() == 'true':
            win32security.RevertToSelf()
    return databaseCursor, databaseConnection


def check_mssql_db_connection(databaseConfigs: Dict[str,str], query: str="")-> Tuple[bool, str]:
    """
    Checks the database connection and executes a SELECT query.

    Parameters:
    - databaseConfigs (Dict[str, str]): A dictionary containing the configuration settings for the database connection. It should include keys such as 'host', 'port', 'user', 'password', 'database', and any other required parameters, all of type str.
    - query (str): The SQL query to be executed, which is expected to be a SELECT query.

    Returns:
    - Tuple (bool, str):
        - A boolean value indicating the success of the operation.
            - True if the connection is established and the query returns results.
            - False if there are any failures during the operation.
        - A message describing the outcome of the operation.

    Note:
    - This function updates the 'query' key in the 'databaseConfigs' dictionary with the provided query.
    - It attempts to establish a database connection and execute the given SELECT query.
    - If the query is a SELECT query and the connection is successful, it checks if any tables are returned.
    - If tables are found, it returns True and a success message. Otherwise, it returns False and a relevant error message.
    - If there are any exceptions during the operation, it returns False and an error message.

    Example Usage:
    database_config = {
        'host': 'localhost',
        'port': '3306',
        'user': 'username',
        'password': 'password',
        'database': 'my_database',
    }
    query = "SELECT * FROM my_table"
    success, message = check(database_config, query)
    if success:
        print(message)  # Connection Established And Found Tables!
    else:
        print(message)  # Database Connection Failed!
    """
    if query != "":
        databaseConfigs.update({"query":query})
    try:
        dc = DatabaseConfig(**databaseConfigs) 
        query = dc.query
        del dc 
        db_cursor, db_connection = dataBaseConnection(databaseConfigs)
        if db_cursor and db_connection:
            try:
                regex = "^SELECT"
                match = re.search(regex, query, re.IGNORECASE)
                if match:
                    db_cursor.execute(query)
                    tables = db_cursor.fetchall()
                    if len(tables) != 0:
                        return True , 'Connection Established And Found Tables!'
                    else:
                        return False, 'Connection Established But Not Found Tables!'
                else:
                    raise Exception("Invalid query type. Please provide SELECT query!")
            except Exception as e:
                return False, f"Couldn't fetch results even after successful connection! {str(e)}"
        else:
            return False, 'Database Connection Failed!'
    except:
        False, "Invalid credentials or structure please check"
    
