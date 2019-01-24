import psycopg2
import sys

class create_tables():
    def create_tables(self, ena):
        conn = psycopg2.connect(ena.conn_string)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE Users (id serial PRIMARY KEY, username VARCHAR, password VARCHAR, level INTEGER, harddata_path VARCHAR )")
        conn.commit()
        conn.close()
