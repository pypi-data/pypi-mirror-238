from essx import Sx, MySQLConnection

sx = Sx()

mysql_connection = MySQLConnection(host='host.docker.internal:3306', username='root', database='essx')

mysql_data_frame = sx.from_mysql(connection=mysql_connection, schema='essx', tables=['essx_netflix_2'])
csv_data_frame = sx.from_csv('/tmp/netflix_table1_csv.csv')

merged_data_frame = sx.merge(mysql_data_frame, csv_data_frame, how='inner', on=['show_id'])
dropped_data_frame = merged_data_frame.drop(columns=['duration', 'rating', 'description'])
