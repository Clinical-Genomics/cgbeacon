#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import coloredlogs
import configparser
import logging
import os.path
import enlighten
import pymysql
import sqlalchemy
from sqlalchemy.engine import create_engine
import sys
import warnings

db_settings = []
LOG = logging.getLogger(__name__)

def get_config():
    """
    Returns the mysql database configuration file path
    """
    return os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', 'settings', 'mysqlconfig.txt'))

def use_mysqlalchemy(conn_url):
    """
    Connects to beacon database using a connection uls and mysqlalchemy
    """
    try:
        engine = sqlalchemy.create_engine(conn_url, echo=False, encoding='utf-8')
        connection = engine.connect()
        return connection

    except Exception as e:
        LOG.critical('MysqlAlchemy was not able to use connection ulr:%s', e)
        sys.exit()

# Connect using mysqlconfig file:
def set_db_params():
    """
    Parses database config params
    """
    LOG.info('Parsing connection params')

    config = configparser.ConfigParser()
    config.read(get_config())

    # set connection params
    try:
        db_settings.append( config['database']['mysql_user'] )
        db_settings.append( config['database']['password'] )
        db_settings.append( config['database']['host'] )
        db_settings.append( config['database']['db'] )
        db_settings.append( config['database']['port'] )

    except Exception as e:
        LOG.critical('There was a problem parsing the database settings file:%s', e)
        sys.exit()

    if len(db_settings) < 4 or '' in db_settings:
        LOG.critical('One or more database settings are missing. Please check parameters file.')
        sys.exit()

    LOG.info('Connection params set.')

    # Return connection url to be used in use_mysqlalchemy
    connect_string = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(db_settings[0], db_settings[1], db_settings[2], db_settings[4], db_settings[3])
    return connect_string

def close_connection(conn):
    """
    Closes connection to database
    """
    conn.close()
    return

def get_variant_number(conn):

    try:
        sql = 'select count(*) as n_vars from beacon_data_table'
        result = conn.execute(sql)
        row = result.fetchone()
        return row['n_vars']

    except:
        LOG.error('Unexpected error:%s',sys.exc_info()[0])
        conn.close()
        return

def insert_variants(conn, dataset, variant_dict, vars_to_beacon):
    """
    Inserts variants into beacon
    """
    insert_counter=0

    LOG.info('Inserting variants into database..')

    #loop over each sample(key) of the dictionary:
    click.echo("variants to process:%s" % vars_to_beacon)
    pbar = enlighten.Counter(total=vars_to_beacon, desc='', unit='ticks')

    for keys, values in variant_dict[1].items():

        #loop over each variant tuple for the sample
        for val in values:

            with warnings.catch_warnings():
                warnings.simplefilter('ignore', pymysql.Warning)

                try:
                    sql = "insert ignore into beacon_data_table (dataset_id, chromosome, position, alternate) values (%s,%s,%s,%s);"
                    result = conn.execute(sql, dataset, val[0], val[1], val[2])
                    insert_counter += result.rowcount

                except:
                    LOG.error('Unexpected error:%s',sys.exc_info()[0])

                pbar.update()

    return insert_counter

def variants_per_dataset(conn, dataset):
    """
    Counts how many variants exist for a given dataset
    """
    nvars=0

    try:
        #with conn.cursor() as cursor:
        sql='select count(*) as vars from beacon_data_table where dataset_id=%s'
        result = conn.execute(sql,dataset)
        row = result.fetchone()
        nvars = row['vars']

    except:
        LOG.error('Unexpected error:%s',sys.exc_info()[0])

    return nvars

def update_dataset_vars(conn, dataset, n_vars):
    """
    Updates the number of variants for a given dataset
    """
    try:
        sql = "pdate beacon_dataset_table set size=%s where id=%s;"
        result = conn.execute(sql, n_vars, dataset)
        return result.rowcount

    except:
        LOG.error('Unexpected error:%s',sys.exc_info()[0])
        return

def update_datasets(conn, dataset, build='grch37'):
    """
    Updates column beacon_dataset_table after variant insertion step
    """
    n_variants = variants_per_dataset(conn,dataset)
    updates=0

    #update dataset table:
    try:
        sql = sql='insert into beacon_dataset_table (id, description, access_type, reference_genome, size) VALUES (%s, %s, %s, %s, %s);'
        result = conn.execute(sql, dataset, 'Sample variants','PUBLIC', build, n_variants)
        updates += result.rowcount

    # Handle the exception that occurrs when trying to insert the same dataset twice
    except pymysql.err.IntegrityError as e:

        # if the dataset exists then just update the number of its vars:
        if 'Duplicate entry' in str(e) :
            LOG.info('It looks like dataset %s exists already. Updating number of variants for this dataset.',dataset)
            updates = update_dataset_vars(conn, dataset, n_variants)

    except:
        LOG.error('Unexpected error:%s',sys.exc_info()[0])

    return updates

def db_handler( dataset, variant_dict, vars_to_beacon, connect_string, reference="grch37"):
    """
    Handles the connection to beacon mysql db and variant data entry.
    """
    conn = None
    if connect_string is None: #Extract connection params from settings file
        # Connect using mysqlconfig file:
        connect_string = set_db_params()

    conn = use_mysqlalchemy(connect_string)

    #variants before:
    time0_vars = get_variant_number(conn)

    #insert variants:
    inserted_variants = insert_variants(conn, dataset, variant_dict, vars_to_beacon)

    if inserted_variants:
        LOG.info('Number of new inserted variants from the VCF file:%s',inserted_variants)

        #update dataset col:
        updated_datasets = update_datasets(conn, dataset, reference)

        if updated_datasets:
            LOG.info('Dataset table was updated')
        else:
            LOG.info('Dataset table was not updated')

    else:
        LOG.warning('No variants could be inserted from this VCF file!')

    #close connection:
    close_connection(conn)

    # return number of variants in beacon before and after adding the VCF file:
    return (time0_vars, inserted_variants)


def bare_variants_uploader(conn, dataset, variant_dict, genome_reference):
    """
    Accepts a connection, the dataset name, the variants and a genome reference.
    Returns the number of uploaded variants_per_dataset
    """
    n_insert_attemps=0

    #Count how many variants are already present in the beacon:
    time0_vars = get_variant_number(conn)

    #loop over each variant tuple for the sample
    for keys, values in variant_dict[1].items():

        #Count the variants to be inserted:
        for val in values:
            n_insert_attemps +=1

    # Try to insert variants
    inserted_variants = insert_variants(conn, dataset, variant_dict, n_insert_attemps)

    if inserted_variants:
        LOG.info('Number of new inserted variants from the VCF file:%s',inserted_variants)

        #update dataset table:
        updated_datasets = update_datasets(conn, dataset, genome_reference)

        if updated_datasets:
            LOG.info('Dataset table was also updated')
        else:
            LOG.info('Dataset was already present in db')

    else:
        LOG.warning('No variants could be inserted from this VCF file!')

    # return number of variants in beacon before and after adding the VCF file:
    return (time0_vars, inserted_variants)

def test_connection():
    """
    Tests the connection to the beacon server
    """
    print("Testing connection to server.")

    #import parameter from con file:
    #try connection with mysqlalchemy
    conn = use_mysqlalchemy("mysql+pymysql://microaccounts_dev:r783qjkldDsiu@localhost:3306/elixir_beacon_testing")
    if conn:
        print("Connection to db established!")
    else:
        print("Couldn't connect to db, please check connection settings and try again!")
    #get number of variants in db:
    print("n. of variants in this beacon ---> ", get_variant_number(conn))
    #close connection:
    conn.close()
    print("connection closed.\n")

if __name__ == '__main__':
    test_connection()
