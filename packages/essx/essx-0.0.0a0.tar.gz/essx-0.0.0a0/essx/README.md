This script requires some initial setup to be completed before using it:
1. Export your Platform API credentials to your localhost's environment variables as SCH_CRED_ID (credential id) and
  SCH_AUTH_TOKEN (authentication token).
2. Export your Snowflake Password (the password used to log into your Snowflake organization) to your localhost's
  environment variables as SF_P. You will supply the username as an argument to the snowflake_conn method.
3. Export your MySQL password (the password used to authenticate with your MySQL instance) to your localhost's
  environment variables as MYSQL_P. You will supply the username as an argument to the mysql_conn method.
4. Spin up a Transformer deployment with a 'docker' install type, and run the resulting install/startup command
  on the same host where the script is being run. Note: you may need to add `-p 19630:19630` to expose the Transformer
  instance inside the docker container on your localhost's 19630 port.
5. Use `docker cp` to copy your target CSV file into your Transformer docker container, and use the path of the copied
  file in the `from_csv` method.

The current script usage is as follows:
    
    import essx

    sx = essx.Sx()
    mysql_conn = sx.mysql_conn(host='url.of.mysql:port', username='username')
    snowflake_conn = sx.snowflake_conn(account='snowflake-account', role='SNOWFLAKE_ROLE',
                                       warehouse='SNOWFLAKE_WAREHOUSE', database='DATABASE', schema='SCHEMA',
                                       username='USERNAME')

    pt1_df = sx.from_mysql(connection=mysql_conn, schema='SCHEMA', tables=['TABLE_NAME'])
    pt2_df = sx.from_csv('/path/to/file.csv')
    final_df = sx.merge(pt1_df, pt2_df, how='JOIN_TYPE', on='COLUMN_NAME')
    final_df = sx.drop(columns=['COLUMN_ONE', 'COLUMN_TWO', 'COLUMN_THREE', 'COLUMN_FOUR'])
