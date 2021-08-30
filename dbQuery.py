# This Python script connects to a PostgreSQL database and utilizes Pandas to obtain data and create a data frame
# A initialization and configuration file is used to protect the author's login credentials

import psycopg2

host = 'ec2-34-228-100-83.compute-1.amazonaws.com'
database = 'dcoq02ha858v2a'
user = 'rlalcrqujcawky'
password = 'fa67ebbbdf58ff2dc74cf67aca83f8f7239e08a199c6eab9c96ec37ac57ccad1'

conn = psycopg2.connect(dbname=database, user=user, password=password,
                        host=host)
cur = conn.cursor()
cur.execute("DROP TABLE custDesc;")
conn.commit()

cur.close()

conn.close()

