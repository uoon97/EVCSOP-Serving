# Create Table
import pymysql
import pandas as pd
from private import db_info

host, user, password, db = db_info()

attributes = pd.read_csv('data/evcs_attributes.csv')
embedding = pd.read_csv('data/evcs_embedding.csv')

connection = pymysql.connect(
    host=host,
    user=user,
    password=password,
    db=db,
    charset='utf8',
    port = 3306
)

create_query = '''
CREATE TABLE IF NOT EXISTS station (
Sid INT NOT NULL PRIMARY KEY, 
Sname VARCHAR(100) NOT NULL, 
Latitude DOUBLE NOT NULL, 
Longitude DOUBLE NOT NULL, 
Capacity FLOAT NOT NULL, 
Slow_Chargers INT NOT NULL,
Fast_Chargers INT NOT NULL,
Mean_trip DOUBLE NOT NULL,
Length_city DOUBLE NOT NULL,
Length_highway DOUBLE NOT NULL,
Length_local DOUBLE NOT NULL,
Length_national DOUBLE NOT NULL,
Indust_ratio DOUBLE NOT NULL,
Etc_ratio DOUBLE NOT NULL,
Green_ratio DOUBLE NOT NULL,
Commerce_ratio DOUBLE NOT NULL,
Reside_ratio DOUBLE NOT NULL,
UMAP_1 DOUBLE NOT NULL,
UMAP_2 DOUBLE NOT NULL,
UMAP_3 DOUBLE NOT NULL,
UMAP_4 DOUBLE NOT NULL,
UMAP_5 DOUBLE NOT NULL,
UMAP_6 DOUBLE NOT NULL,
UMAP_7 DOUBLE NOT NULL,
UMAP_8 DOUBLE NOT NULL
)
'''

with connection.cursor() as cursor:
    cursor.execute(create_query.replace('\n', ''))

for idx in range(attributes.shape[0]):
    atts = attributes.iloc[idx, :].values.tolist()
    emb = embedding.iloc[idx, :].values.tolist()[1:]
    values = tuple([idx] + atts + emb)
    insert_query = "INSERT INTO station VALUES {};"
    
    with connection.cursor() as cursor:
        cursor.execute(insert_query.format(values))

connection.commit()