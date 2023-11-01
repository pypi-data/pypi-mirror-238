import os
import psycopg2
import pandas as pd
from psycopg2 import extras



class Database(object):
    def __init__(self, user,password,host,port,database,multiple=False):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.multiple = multiple

    def connect(self,db):

        try:
            conn = psycopg2.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=db
            )
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            return conn, cur
        except Exception as e:
            print(f'Error connecting to {db}: {e}')
            return None, None

    def get_sql(self, sql, params=None):
        conn, cur = self.connect(self.database)
        if conn is None or cur is None:
            return None

        try:
            cur.execute(sql, params)
            result = cur.fetchall()
            df = pd.DataFrame(result)
            return df
        finally:
            conn.close()

    def commit_sql(self, sql, params=None):

        conn, cur = self.connect(self.database)
        if conn is None or cur is None:
            return
        try:
            if params is None:
                cur.execute(sql)
            else:
                cur.execute(sql, params)
            conn.commit()
        except Exception as e:
            print(f"SQL execution error: {e}")
        finally:
            conn.close()



    def insert(self,table, df,onConflict=''):
        if self.multiple :
            for db in ['research','trading'] : 
                self.batch_insert(db,table, df,onConflict)
        else :
            self.batch_insert(self.database,table, df,onConflict)


    def batch_insert(self,db,table, df,onConflict=''):
        try:
            conn, cur = self.connect(db)
            if conn is None or cur is None:
                return

            tuples = [tuple(x) for x in df.to_numpy()]
            cols = ','.join(list(df.columns))
            query = f"INSERT INTO {table}({cols}) VALUES %s {onConflict}"
            extras.execute_values(cur, query, tuples)
            conn.commit()
            print("Data inserted",db)
        except Exception as error:
            print(f"Data Error: {error,db}")
            conn.rollback()
        finally:
            if conn is not None:
                conn.close()
    
