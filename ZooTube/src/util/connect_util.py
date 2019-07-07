#! /bin/env python3
'''
Utility file to connect mysql database and rabbitmq
'''
import mysql.connector
import pika

def mysql_connect(cfg):
    # connect mysql database
    mysqlconfig = {
        'user': cfg['mysql']['db_user'],
        'password': cfg['mysql']['db_passwd'],
        'host': cfg['mysql']['db_host'],
        'database': cfg['mysql']['db_name'],
        'port' : cfg['mysql']['db_port'],
        'raise_on_warnings': True
        }
    cnx = mysql.connector.connect(**mysqlconfig)
    cur = cnx.cursor()
    return (cnx,cur)

def rabbit_connect(cfg):
    # connect rabbitmq
    credentials = pika.PlainCredentials(cfg["rabbitmq"]["mq_user"], cfg["rabbitmq"]["mq_passwd"])
    parameters = pika.ConnectionParameters(cfg["rabbitmq"]["mq_host"],cfg["rabbitmq"]["mq_port"],'/',credentials)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=cfg["rabbitmq"]["mq_name"])
    return (connection,channel)


    
