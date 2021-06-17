
#!/usr/bin/env python
import snowflake.connector
from snowflake.connector.pandas_tools import *
import pandas as pd
import fastparquet
# Gets the version
ctx = snowflake.connector.connect(
    user='',
    password='',
    account=''
    )
cs = ctx.cursor()
cs.execute('USE ROLE hopelab_infra')
cs.execute(f'USE DATABASE quit_the_hit_raw')
cs.execute(f'USE SCHEMA rescue_files')
print("Established snowlake")

def upload_to_snowflake(conn, df, table_name, database, schema):
    
    # Drop table if exact table exists
    cs.execute(f'''DROP TABLE IF EXISTS {database}.{schema}.{table_name}''')
    
    # Make empty table to transfer into 
    cs.execute(f'''CREATE TABLE IF NOT EXISTS {database}.{schema}.{table_name} 
                        LIKE quit_the_hit_raw.rescue_files.engagement_template''')
    print(f'New table location: {database}.{schema}.{table_name}')
       
    # Load into snowflake
    cs.execute('USE WAREHOUSE hopelab')
    success, num_chunks, num_rows, output = write_pandas(conn=ctx, 
             df=df, 
             table_name = table_name.upper(), 
             database = database.upper(), 
             schema =schema.upper())
    print(f"Snowflake load success: {success}")
    
# Call above function
upload_to_snowflake()
