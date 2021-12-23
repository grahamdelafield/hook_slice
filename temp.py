import psycopg2

POSTGRES_URI = 'postgres://mewzpjro:LmVUqseI178MBoRAAXmk_RiTXLu3Kwa7@castor.db.elephantsql.com/mewzpjro'

connection = psycopg2.connect(POSTGRES_URI)
with connection:
    with connection.cursor() as cursor:
        cursor.execute('ALTER TABLE data DROP COLUMN putt_number')        