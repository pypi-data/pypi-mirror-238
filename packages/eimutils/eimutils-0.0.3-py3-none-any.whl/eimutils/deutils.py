"""
*******************************************************************************
File: deUtils.py

Purpose: Creates some nice helper functions

Dependencies/Helpful Notes : 

*******************************************************************************
"""

from deUtils.aws_secrets import get_secret
from deUtils.delogging import log_to_console

"""
*******************************************************************************
Function: get_sqlserver_connection_from_secret

Purpose: Generate a database connection from AWS secret.

Parameters:
     secret_name - AWS secret name from the account the process is running in
                   that contains the db connection information.  

Calls:
    get_secret
    connect_database
    
Called by:

Returns: database connection

*******************************************************************************
"""

def get_sqlserver_connection_from_secret(secret_name):

    try:
        # get the secret
        db_connection_secret = get_secret(secret_name)

        # get the values into variables
        user = db_connection_secret["user"]
        host = db_connection_secret["host"]
        password = db_connection_secret["password"]
        database = db_connection_secret["database"]

        # get the database connection
        db_connection = 'test' # connect_database(host, user, password, database)

    except Exception as e:
        log_to_console(__name__, 'Err', str(e))

    return db_connection

"""
*******************************************************************************
Function: get_db_connection_from_secret

Purpose: Generate a database connection from AWS secret.

Parameters:
     secret_name - AWS secret name from the account the process is running in
                   that contains the db connection information.  

Calls:
    get_secret
    connect_database
    
Called by:

Returns: database connection

*******************************************************************************
"""

def get_snowflake_connection_from_secret(secret_name, env, account):

    try:
        # get the secret
        db_connection_secret = get_secret(secret_name)

        # ToDo: Decrypt the pkbDER key

        # ToDo: Create the connection to snowflake
        db_connection = 'testing'
        """
        db_connection = snc.connect(
            user=f'EIM_{env}_DW3_SVC_USER',
            account=account,
            private_key=pkbDER,
            role=f'EIM_{env}_DW3_ADMIN'
        )
        """


    except Exception as e:
        log_to_console(__name__, 'Err', str(e))

    return db_connection

"""
*******************************************************************************
Change History:

Author		Date		Description
----------	----------	-------------------------------------------------------
Frank		04/08/2022  Initial Iteration
                        + get_db_connection_from_secret
Frank		20230919    + imports
*******************************************************************************
"""