import click
from databricks import sql
import json
import hashlib
import hmac
import base64
import requests
from datetime import datetime
from airflow.models import Variable
import pytz
from typing import List, Tuple
import os
from airflow.hooks.base_hook import BaseHook
import logging
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine

@click.command()
@click.option('--env', default='databricks')
@click.option('--dwhcid', default='jaffle_shop_databricks_connection')
@click.option('--azpurview', default='azure_purview')
def dbtpurview(env,dwhcid,azpurview):


   if(env == "databricks"):
        conn = BaseHook.get_connection(str(dwhcid))
        databricks_extras_dict = json.loads(conn.get_extra())
        connection_string = str(conn.host)
        token = str(conn.password)
        http_path = str(databricks_extras_dict["http_path"])


   if(env == "snowflake"):
        snowflake_conn = BaseHook.get_connection(str(dwhcid))
        e1xtras_dict = json.loads(snowflake_conn.get_extra())
        engine = create_engine(URL(
            account = str(e1xtras_dict['account']),
            user = str(snowflake_conn.login),
            password = str(snowflake_conn.password),
            database = str(e1xtras_dict['database']),
            schema = str(snowflake_conn.schema),
            warehouse = str(e1xtras_dict['warehouse']),
            role= str(e1xtras_dict['role']),
        ))

   PROJECT_ROOT_PATH=Variable.get("PROJECT_ROOT_PATH")
   print(PROJECT_ROOT_PATH)
   root_directory = "/tmp"
   list_files_and_directories(root_directory)

def list_files_and_directories(root_dir):
    for root, dirs, files in os.walk(root_dir):
        print("Current Directory:", root)
        print("Subdirectories:")
        for directory in dirs:
            print(os.path.join(root, directory))
        print("Files:")
        for file in files:
            print(os.path.join(root, file))


if __name__ == '__main__':
   dbtpurview()   
   
   

