# Script to read in a parquet file from local directory and write it to postgres

# import pyarrow to convert parquet to pandas
import pandas as pd
import pyarrow.parquet as pq 
import psycopg2 as pg
import sqlalchemy as sa

# convert the yellow_tripdata_2022-01.parquet to a pandas dataframe
trips = pq.read_table('yellow_tripdata_2022-01.parquet')
trips = trips.to_pandas()

""" doesn't work for some reason
# connect to postgres ny_taxi database using psychopg
conn = pg.connect(database='ny_taxi', 
                        user='root', 
                        password='root', 
                        host='localhost', port='5432')
"""

eng = sa.create_engine('postgresql://root:root@localhost:5432/ny_taxi')

def show_tables(conn):

  # Acquire the resource
  with conn.cursor() as cursor:
      try:
         # execute the query
         cursor.execute("""
           SELECT table_name 
           FROM information_schema.tables
           WHERE table_schema = current_schema();
          """)
  
         # Fetch and print the results of the first query
         results = cursor.fetchone()
         print(results)
  
      finally:
          # Close the cursor and connection
          cursor.close()

def print_available_memory():
    #To determine the amount of memory available and choose an appropriate chunksize value for the pandas.to_sql() function in a running Python script, you can use the psutil module.

    #Here's an example of how to do this:

    import psutil

    # Get the total amount of memory
    total_memory = psutil.virtual_memory().total

    # Calculate the amount of memory used by the script
    memory_used = sum(x.size for x in locals().values() if hasattr(x, 'size'))

    # Calculate the amount of memory available
    memory_available = total_memory - memory_used

    print(memory_available)

# the total amount of memory of the data in the trips data frame
# trips.memory_usage().sum()

# use to_sql to write a pandas data frame to the postgres database
trips.to_sql('yellow_taxi_data', con=eng, 
             if_exists='replace', 
             index=False, chunksize=100000) # 1,000,000 took 5 m and 40.5 s

# close the postgres connection
