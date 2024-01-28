'''
Description:
    - Steps to follow: https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/python-sql-driver-pyodbc?view=sql-server-ver15
    - Connect to Azure SQL Database: https://docs.microsoft.com/en-us/azure/azure-sql/database/connect-query-python?tabs=windows 
'''
import pandas as pd
import pyodbc
import os

def connect():
    # Database Credentials
    server   = os.getenv('azureServer')
    database = os.getenv('azureDBFinancial')
    username = os.getenv('azureDBUsername')
    password = os.getenv('azureDBPswd')
    driver   = '{ODBC Driver 17 for SQL Server}'

    # Connect to Database
    cnxn = pyodbc.connect('DRIVER='+driver+';      \
                           SERVER='+server+';      \
                           PORT=1433;              \
                           DATABASE='+database+';  \
                           UID='+username+';       \
                           PWD='+ password)
    return cnxn


def read(schema, table):

    # Connect to Database
    cnxn = connect()

    # Get All Columns from Database Table
    return pd.read_sql_query('''SELECT * FROM [{}].[{}]'''.format(schema, table), cnxn)
