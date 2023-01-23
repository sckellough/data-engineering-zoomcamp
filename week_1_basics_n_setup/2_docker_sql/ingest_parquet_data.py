#!/usr/bin/env python
# coding: utf-8

import argparse
import os
import pyarrow.parquet as pq
import sqlalchemy as sa

def __download_file__(url):
    # todo: download arbitrary parquet files from any url
    #       via os.system(f"wget {url} -O {csv_name}")    

    if url == 'yellow_tripdata_2022-01.parquet':
        print("file exists")
    else:
        raise Exception(f"""
                I don't know how to handle data file {url}.
                I only know how to handle 'yellow_tripdata_2022-01.parquet""")

        

def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    url = params.url

    eng = sa.create_engine('postgresql://{user}:{password}@{host}:{port}/{db}')

    trips = pq.read_table('yellow_tripdata_2022-01.parquet').to_pandas()





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest Parquet data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='url of the parquet file')

    # will throw an error if the above arguments are not included
    args = parser.parse_args()

    main(args)