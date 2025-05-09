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
schema_bronze = "bronze"
schema_silver = "silver"
engine = postgres_conn()

def read_data(engine, schema, table):
    try:
        query = f"SELECT * FROM {schema}.{table};"
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"Ocorreu um erro ao tentar ler os dados: {e}")
        return None

def tranform_load_silver():
    bronze_chinese_caixin = read_data(engine, schema_bronze, chinese_caixin_services_index)
    bronze_chinese_caixin["date"] = pd.to_datetime(
        bronze_chinese_caixin["date"].astype("string").str[:10].str.replace(".", "-"), format="%d-%m-%Y")
    bronze_chinese_caixin["actual_state"] = pd.to_numeric(
        bronze_chinese_caixin["actual_state"].astype("string").str.replace(",", "."), errors="coerce")
    bronze_chinese_caixin["forecast"] = pd.to_numeric(
        bronze_chinese_caixin["forecast"].astype("string").str.replace(",", "."), errors="coerce")
    bronze_chinese_caixin["previous"] = pd.to_numeric(
        bronze_chinese_caixin["previous"].astype("string").str.replace(",", "."), errors="coerce")

    bronze_usd_cny = read_data(engine, schema_bronze, usd_cny)
    bronze_usd_cny["date"] = pd.to_datetime(
        bronze_usd_cny["date"].astype("string").str.replace(".", "-"), format="%d-%m-%Y")
    bronze_usd_cny["close"] = pd.to_numeric(
        bronze_usd_cny["close"].astype("string").str.replace(",", "."), errors="coerce")
    bronze_usd_cny["opening"] = pd.to_numeric(
        bronze_usd_cny["opening"].astype("string").str.replace(",", "."), errors="coerce")
    bronze_usd_cny["high"] = pd.to_numeric(
        bronze_usd_cny["high"].astype("string").str.replace(",", "."), errors="coerce")
    bronze_usd_cny["low"] = pd.to_numeric(
        bronze_usd_cny["low"].astype("string").str.replace(",", "."), errors="coerce")
    bronze_usd_cny["volume"] = pd.to_numeric(
        bronze_usd_cny["volume"].astype("string").str.replace(",", "."), errors="coerce")
    bronze_usd_cny["variation"] = pd.to_numeric(
        bronze_usd_cny["variation"].astype("string").str.replace("+", "").str.replace("-", "")
        .str.replace("%", ""), errors="coerce")

    bronze_chinese_caixin.to_sql(
        chinese_caixin_services_index, engine, schema=schema_silver, if_exists='append', index=False)
    bronze_usd_cny.to_sql(
        usd_cny, engine, schema=schema_silver, if_exists='append', index=False)
    