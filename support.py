import sqlite3
import json
import datetime
import pandas as pd
import plotly
import plotly.express as px

def connect_db():
    conn = sqlite3.connect("expense.db")
    cur = conn.cursor()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS user_login (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(30) NOT NULL, 
        email VARCHAR(30) NOT NULL UNIQUE, password VARCHAR(20) NOT NULL)''')
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS user_expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, pdate DATE NOT 
        NULL, expense VARCHAR(10) NOT NULL, amount INTEGER NOT NULL, pdescription VARCHAR(50), FOREIGN KEY (user_id) 
        REFERENCES user_login(user_id))''')
    conn.commit()
    return conn, cur

def close_db(connection=None, cursor=None):
    cursor.close()
    connection.close()
def execute_query(operation=None, query=None):
    connection, cursor = connect_db()
    if operation == 'search':
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        return data
    elif operation == 'insert':
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()
        return None


def generate_df(df):
    df = df
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month_name'] = df['Date'].dt.month_name()
    df['Month'] = df['Date'].dt.month
    df['Day_name'] = df['Date'].dt.day_name()
    df['Day'] = df['Date'].dt.day
    df['Week'] = df['Date'].dt.isocalendar().week
    return df
def num2MB(num):
    if num < 1000:
        return int(num)
    if 1000 <= num < 1000000:
        return f'{float("%.2f" % (num / 1000))}K'
    elif 1000000 <= num < 1000000000:
        return f'{float("%.2f" % (num / 1000000))}M'
    else:
        return f'{float("%.2f" % (num / 1000000000))}B'


def top_tiles(df=None):
    """
    Sum of total expenses
    :param df:
    :return: sum
    """
    if df is not None:
        tiles_data = df[['Expense', 'Amount']].groupby('Expense').sum()
        tiles = {'Earning': 0, 'Investment': 0, 'Saving': 0, 'Spend': 0}
        for i in list(tiles_data.index):
            try:
                tiles[i] = num2MB(tiles_data.loc[i][0])
            except:
                pass
        return tiles['Earning'], tiles['Spend'], tiles['Investment'], tiles['Saving']
    return
