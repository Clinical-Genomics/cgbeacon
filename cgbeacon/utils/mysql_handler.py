#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import coloredlogs
import configparser
import logging
import os.path
import enlighten
import pymysql
import sys
import warnings

db_settings = []
LOG = logging.getLogger(__name__)

def get_config():
    """
    Returns the mysql database configuration file path
    """
    return os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '..', 'settings', 'mysqlconfig.txt'))

#import mysql.connector
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
    return

def connect_to_db():
    """
    Connects to beacon mysql database
    """
    try:
        LOG.info('Connectiong to db %s', db_settings[3])
        connection = pymysql.connect(user=db_settings[0],
                                     password=db_settings[1],
                                     host=db_settings[2],
                                     db=db_settings[3],
                                     port=int(db_settings[4]),
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        return connection
    except Exception as e:
        LOG.error('Unexpected error:%s',e)
        return


def close_connection(conn):
    """
    Closes connection to database
    """

    conn.close()
    return

def get_variant_number(conn):

    try:
        with conn.cursor() as cursor:
            sql = 'select count(*) as n_vars from beacon_data_table'
            cursor.execute(sql)
            result = cursor.fetchone()
            nvars = result['n_vars']
            LOG.info('----> number of variants in this beacon:%s',nvars)
            return nvars
    except:
        LOG.error('Unexpected error:%s',sys.exc_info()[0])
        print('error',sys.exc_info()[0])
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
                    with conn.cursor() as cursor:
                        sql='INSERT IGNORE INTO beacon_data_table (dataset_id, chromosome, position, alternate) VALUES (%s, %s, %s, %s)'

                        cursor.execute(sql,( dataset, val[0], val[1], val[2]))
                        conn.commit()
                        insert_counter += cursor.rowcount

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
        with conn.cursor() as cursor:
            sql='select count(*) as vars from beacon_data_table where dataset_id=%s'
            cursor.execute(sql,dataset)
            result = cursor.fetchone()
            nvars = result['vars']
    except:
        LOG.error('Unexpected error:%s',sys.exc_info()[0])

    return nvars

def update_dataset_vars(conn, dataset, vars):
    """
    Updates the number of variants for a given dataset
    """
    try:
        with conn.cursor() as cursor:
            sql='update beacon_dataset_table set size=%s where id=%s'
            cursor.execute(sql,(vars,dataset))
            conn.commit()
    except:
        LOG.error('Unexpected error:%s',sys.exc_info()[0])

def update_datasets(conn, dataset, build='grch37'):
    """
    Updates column beacon_dataset_table after variant insertion step
    """
    n_variants = variants_per_dataset(conn,dataset)
    updates=0

    #update dataset table:
    try:
        with conn.cursor() as cursor:
            sql='insert into beacon_dataset_table (id, description, access_type, reference_genome, size) VALUES (%s, %s, %s, %s, %s)'
            cursor.execute(sql, (dataset, 'Sample variants','PUBLIC', build, n_variants))

            conn.commit()
            updates += cursor.rowcount

    except pymysql.err.IntegrityError as e:

        # if the dataset exists then just update the number of vars:
        if 'Duplicate entry' in str(e) :
            LOG.info('It look like dataset %s exists already. Updating number of variants for this dataset.',dataset)
            update_dataset_vars(conn, dataset, n_variants)

    except:
        LOG.error('Unexpected error:%s',sys.exc_info()[0])

    return updates

def db_handler(reference, dataset, variant_dict, vars_to_beacon):
    """
    Handles the connection to beacon mysql db and variant data entry.
    """
    #import parameter from con file:
    set_db_params()

    #connect to db:
    conn = connect_to_db()

    #variants before:
    time0_vars = get_variant_number(conn)

    #insert variants:
    inserted_variants = insert_variants(conn, dataset, variant_dict, vars_to_beacon)

    if inserted_variants:
        LOG.info('Number of new inserted variants from the VCF file:%s',inserted_variants)

        #update dataset col:
        updated_datasets = update_datasets(conn, dataset, 'grch37')

        if updated_datasets:
            LOG.info('Dataset table was also updated')
        else:
            LOG.info('Dataset was already present in db')

    else:
        LOG.warning('No variants could be inserted from this VCF file!')

    #close connection:
    close_connection(conn)

    # return number of variants in beacon before and after adding the VCF file:
    return (time0_vars, inserted_variants)


def test_connection():
    """
    Tests the connection to the beacon server
    """
    print("Testing connection to server.")

    #import parameter from con file:
    set_db_params()
    #try connection:
    conn = connect_to_db()
    if conn:
        print("Connection to db established!")
    else:
        print("Couldn't connect to db, please check connection settings and try again!")
    #get number of variants in db:
    print("n. of variants in this beacon ---> ", get_variant_number(conn))
    #close connection:
    close_connection(conn)
    print("connection closed.\n")

if __name__ == '__main__':
    test_connection()
