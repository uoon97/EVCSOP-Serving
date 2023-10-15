from dateutil.relativedelta import relativedelta
from private import db_info
import pandas as pd
import numpy as np
import datetime
import pymysql
import torch

# get input's datetime
def get_dt():
    now = datetime.datetime.now()
    dt = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute//20*20, 00)
    dt -= relativedelta(months=18)
    return dt

# get realtime datetime
def get_rdt(n):
    dt_realtime = []
    dt = get_dt()
    for i in range(n-1, -1, -1):
        if i == 0 or i == n-1:
            rdt = dt - datetime.timedelta(minutes = 20*(i+1))
            dt_realtime.append(rdt.strftime('%Y-%m-%d %H:%M:%S'))
    return dt_realtime

# get historic datetime
def get_hdt(h, minutes):
    dt_historic = []
    dt = get_dt()
    for i in range(h):
        hdt = dt - datetime.timedelta(days = 7*(i+1))
        for j in minutes:
            hsdt = hdt + datetime.timedelta(minutes = j)
            dt_historic.append(hsdt.strftime('%Y-%m-%d %H:%M:%S'))
    return dt_historic

# connect to database by pymysql
def db_connect():
    host, user, password, db = db_info()

    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db,
        charset='utf8',
        port = 3306
    )

    return connection

# get station id from database
def db2Sid():
    connection = db_connect()
    select_query = "SELECT Sid FROM station"

    with connection.cursor() as cursor:
        cursor.execute(select_query)
        result = cursor.fetchall()
        connection.close()

    sid = [res[0] for res in result]
    return sid

def db2Now():
    connection = db_connect()
    now = get_dt().strftime('%Y-%m-%d %H:%M:%S')
    select_query = f"SELECT * FROM sequence WHERE Time = '{now}'"

    with connection.cursor() as cursor:
        cursor.execute(select_query)
        result = cursor.fetchall()
        connection.close() 
    
    df = pd.DataFrame(result, columns=[col[0] for col in cursor.description])
    return torch.tensor(df.set_index('Time').values).reshape(-1, 1)

# get realtime sequence inputs from database
def db2Rseq():
    connection = db_connect()
    start, end = get_rdt(12)
    select_query = f"SELECT * FROM sequence WHERE Time BETWEEN '{start}' AND '{end}'"

    with connection.cursor() as cursor:
        cursor.execute(select_query)
        result = cursor.fetchall()
        connection.close()

    df = pd.DataFrame(result, columns=[col[0] for col in cursor.description])
    return torch.tensor(df.set_index('Time').T.values.reshape(len(cursor.description)-1, -1, 1))

# get historical sequence inputs from database
def db2Hseq(h_step):
    connection = db_connect()
    minutes = [20, 40, 60, 120]
    values = tuple(get_hdt(h_step, minutes))
    select_query = f'SELECT * FROM sequence WHERE Time IN {values}'

    with connection.cursor() as cursor:
        cursor.execute(select_query)
        result = cursor.fetchall()
        connection.close()

    df = pd.DataFrame(result, columns=[col[0] for col in cursor.description])
    return torch.tensor(df.set_index('Time').T.values.reshape(len(cursor.description)-1, len(minutes), h_step, 1))

# get time index
def dt2T():
    connection = db_connect()
    select_query = "SELECT * FROM sequence LIMIT 1"
    with connection.cursor() as cursor:
        cursor.execute(select_query) 
        _ = cursor.fetchall()
        connection.close()

    dt = get_dt()
    T = []
    minutes = [20, 40, 60, 120]
    for i in minutes:
        t_dt = dt + datetime.timedelta(minutes=i)
        time_idx = t_dt.hour * 3 + t_dt.minute // 20
        dow = t_dt.weekday()
        weekend = dow//5
        T.append([time_idx, dow, weekend])
    
    T = np.array(T)
    T = np.repeat(T[np.newaxis, :, :], repeats = len(cursor.description)-1, axis = 0)
    return torch.tensor(T)

# get station inputs from database
def db2S():
    connection = db_connect()
    select_query = "SELECT * FROM station"

    with connection.cursor() as cursor:
        cursor.execute(select_query)
        result = cursor.fetchall()
        connection.close()

    df = pd.DataFrame(result, columns=[col[0] for col in cursor.description])
    attr_cols = ['Sid', 'latitude', 'longitude', 'capacity', 'slow',
                 'fast', 'mean_trip', 'length_city', 'length_highway',
                 'length_local', 'length_national', 'indust_ratio', 'etc_ratio',
                 'green_ratio', 'commerce_ratio', 'reside_ratio']

    embed_cols = ['Sid', 'umap_1', 'umap_2', 'umap_3', 'umap_4', 
                  'umap_5', 'umap_6', 'umap_7', 'umap_8']

    attrs = torch.tensor(df.loc[:, attr_cols].values)
    embed = torch.tensor(df.loc[:, embed_cols].values)

    return attrs, embed

# update outputs data to database
from utils import *

def y2db(outputs):

    sid = db2Sid()
    connection = db_connect()
    update_query = "UPDATE occupancy SET {}"
    minutes = [20, 40, 60, 120]
    labels = [0, 1, 2]

    for i in range(len(sid)):
        output = outputs[i].tolist()[1:]
        label_query_values = ', '.join([f'Occupancy{k}_{m} = {output[m + 3*j]}' for m in labels for j, k in enumerate(minutes)])
        values = ' '.join([f'Occupancy0 = {outputs[i][0]}, '] + [label_query_values] + [f'WHERE Sid = {sid[i]}'])
        
        with connection.cursor() as cursor:
            cursor.execute(update_query.format(values))
        
    connection.commit()
    connection.close()