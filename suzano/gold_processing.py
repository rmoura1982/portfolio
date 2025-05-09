import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os


load_dotenv()

def postgres_conn():
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")

    db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(db_url)
    return engine

chinese_caixin_services_index = "chinese_caixin_services_index"
usd_cny = "usd_cny"
usd_cny_chinese_caixin = "usd_cny_chinese_caixin"
schema_silver = "silver"
schema_gold = "gold"
engine = postgres_conn()

def read_data(engine, schema, table):
    try:
        query = f"SELECT * FROM {schema}.{table};"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"Ocorreu um erro ao tentar ler os dados: {e}")
        return None
    
def rule_load_gold():
    silver_chinese_caixin = read_data(engine, schema_silver, chinese_caixin_services_index)
    silver_usd_cny = read_data(engine, schema_silver, usd_cny)

    gold_usd_cny_silver_chinese = pd.merge(
        silver_usd_cny, 
        silver_chinese_caixin, 
        on='date', 
        how='inner',
        suffixes=('_usd_cny', '_chinese')
    )

    gold_usd_cny_silver_chinese.to_sql(
        usd_cny_chinese_caixin, engine, schema=schema_gold, if_exists='append', index=False)
