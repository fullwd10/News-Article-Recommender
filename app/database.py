import psycopg2
import numpy as np
from psycopg2.extensions import register_adapter, AsIs

def connect_to_db(host: str, dbname: str, user: str, password:str):
    try:
        conn = psycopg2.connect(host=host, dbname=dbname, user=user, password=password)
        print('connection to database successful')
        return conn

    except Exception as error:
        print('connection to database failed')
        print('error', error)

def in_db(db, url):
    cur = db.cursor()
    query = cur.execute("SELECT * FROM bbc WHERE url = %s", (url,))
    row = cur.fetchone()
    return row != None

def save_to_db(db, entry):
    cur = db.cursor()
    query = """
            INSERT INTO bbc (url, title, published_time, content, embedding)
            VALUES (%s, %s, %s, %s, %s)
            """
    values = (entry['url'], entry['title'], entry['published_time'], entry['content'], entry['embedding'])
    cur.execute(query, values)
    #db.commit()
     


def addapt_numpy_array(numpy_array):
    return AsIs(tuple(numpy_array))

register_adapter(np.ndarray, addapt_numpy_array)

def most_similiar_articles(db, id:int, n:int):
    cur = db.cursor()
    sql = """
            SELECT table1.id
            FROM guardian AS table1
            JOIN (
                SELECT 
                    ((SELECT embedding FROM guardian WHERE id = (%s)) <=> embedding) AS inner_prod, 
                    id 
                FROM guardian
                WHERE id != (%s)
            ) AS table2
            ON table1.id = table2.id
            ORDER BY inner_prod ASC
            LIMIT (%s)
            """
    cur.execute(sql, (id, id, n))
    ids = [int(x[0]) for x in cur.fetchall()]
    return list(ids)

