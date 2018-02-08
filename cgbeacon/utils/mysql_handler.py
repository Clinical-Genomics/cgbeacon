#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import coloredlogs
import configparser
import logging
import os.path
from pathlib import Path
import enlighten
import pymysql
import sqlalchemy
from sqlalchemy.engine import create_engine
import sys
import warnings

db_settings = []
LOG = logging.getLogger(__name__)

def use_mysqlalchemy(conn_url):
    """
    Connects to beacon database using a connection url and mysqlalchemy
    """
    try:
        engine = sqlalchemy.create_engine(conn_url, echo=False, encoding='utf-8')
        connection = engine.connect()
        return connection

    except Exception as e:
        LOG.critical('MysqlAlchemy was not able to use connection ulr:%s', e)
        sys.exit()

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

def remove_variants(conn, dataset, list_of_var_tuples):
    """
    Deletes variants from beacon
    """
    delete_counter=0
    LOG.info('Deleting variants from database..')

    #loop over each sample(key) of the dictionary:
    click.echo("variants to remove:%s (it might take some time!)" % len(list_of_var_tuples))
    pbar = enlighten.Counter(total=len(list_of_var_tuples), desc='', unit='ticks')

    for var_tuple in list_of_var_tuples:
        try:
            unique_key = dataset+"_"+str(var_tuple[0])+"_"+str(var_tuple[1])+"_"+var_tuple[2]
            # Remove 1 from the occurrence field if this is not the last occurrence
            sql = "update beacon_data_table set occurrence = occurrence -1 where chr_pos_alt_dset=%s"
            result = conn.execute(sql, unique_key)
            if result.rowcount > 0:
                delete_counter += 1
            pbar.update()

        except Exception as ex:
            print('Unexpected error:',ex)

    # delete all records with no samples associated:
    if delete_counter>0:
        sql = "delete from beacon_data_table where occurrence = 0;"
        conn.execute(sql)
    return delete_counter

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
                    unique_key = dataset+"_"+str(val[0])+"_"+str(val[1])+"_"+val[2]
                    sql = "insert into beacon_data_table (dataset_id, chromosome, position, alternate, occurrence, chr_pos_alt_dset) values (%s, %s, %s, %s, %s, %s) on duplicate key update occurrence = occurrence + 1"
                    result = conn.execute(sql, dataset, val[0], str(val[1]), val[2], 1, unique_key)

                    if result.rowcount >0:
                        insert_counter += 1

                except Exception as ex:
                    LOG.warn('Unexpected error:%s', ex)

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
        sql = "update beacon_dataset_table set size=%s where id=%s;"
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
        sql = 'insert into beacon_dataset_table (id, description, access_type, reference_genome, size) VALUES (%s, %s, %s, %s, %s);'
        result = conn.execute(sql, dataset, 'Sample variants','PUBLIC', build, n_variants)
        updates += result.rowcount

    # Handle the exception that occurrs when trying to insert the same dataset twice
    except sqlalchemy.exc.IntegrityError as e:
        LOG.warn('Dataset already in beacon')
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
        try:
            updated_datasets = update_datasets(conn, dataset, genome_reference)

            if updated_datasets:
                LOG.info('Dataset table was also updated')
            else:
                LOG.info('Dataset was already present in db')
        except sqlalchemy.exc.IntegrityError:
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
