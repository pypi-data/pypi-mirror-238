from sqlalchemy import create_engine
import pandas as pd


class BaseProcess:
    def __init__(self, engine_uri, sql_query):
        self.engine = create_engine(engine_uri)
        self.sql_query = sql_query

    def load_data(self):
        return pd.read_sql_query(self.sql_query, self.engine)

    def filter_data(self, df):
        """子类可以重写这个方法以提供自己的过滤逻辑"""
        return df

    def execute_operations(self, df):
        """子类可以重写这个方法以执行特定的操作"""
        pass

    def run(self):
        df = self.load_data()
        df_filtered = self.filter_data(df)
        self.execute_operations(df_filtered)
