import numpy as np
import pandas as pd
import pika
import json
import yaml
import platform
import schedule
import datetime
import pyodbc
import os
from krb5 import do_kinit_w_keytab


try:
    ENV = os.environ["ENVIRONMENT"]
    print("ENV is OK")
except Exception as e:
    ENV = 'DEV'

print(ENV)
with open("config.yaml") as f:
    config=yaml.full_load(f)[ENV]





def getfilials(con_filials):
    schema,table = config['sql']['listfilials']['schema'], config['sql']['listfilials']['table']
    sql = f"select FilID from [{schema}].[{table}]"
    df = pd.read_sql_query(sql,con_filials)
    return df



def func():
    credentials = pika.PlainCredentials(username=config['rabbit']['user'], password=config['rabbit']['pwd'])
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config['rabbit']['host'],\
                                port=config['rabbit']['port'],virtual_host=config['rabbit']['vhost'], credentials=credentials))
    channel = connection.channel()

    end = datetime.datetime.now().strftime('%Y-%m-%d')
    start=str((pd.to_datetime(end)-pd.to_timedelta(33,unit='d')).date())
    server,database = config['sql']['listfilials']['server'],config['sql']['listfilials']['db']
    #con_filials = pyodbc.connect(DRIVER='{ODBC Driver 17 for SQL Server}',server=server\
     #       ,DATABASE=database,Trusted_Connection='yes')

    con_filials = pyodbc.connect(DRIVER='{ODBC Driver 17 for SQL Server}',server=server\
            ,DATABASE=database,uid='j-gb-client',pwd='Mb1ygZywkGxi8ZQLbVeb')

    filials=getfilials(con_filials).values
    con_filials.close()
    for fil in filials:
        mes=dict(filid=fil.item() ,start=start,end=end)
        channel.basic_publish(exchange='',routing_key=config['rabbit']['queue_in'],body=json.dumps(mes),\
                    properties=pika.BasicProperties(delivery_mode=2))
        print(mes)
    channel.close()
    connection.close()

if __name__=='__main__':
    #schedule.every(0.1).minutes.do(func)
    schedule.every().day.at("16:00:40").do(func)
    #schedule.every().Wednesday.at("8:00").do(func)



    while True:
        schedule.run_pending()
