from sqlalchemy import create_engine, text
from web_scraping import scrape_chinese_caixin, scrape_usd_cny
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

df_chinese_caixin = scrape_chinese_caixin()
df_usd_cny = scrape_usd_cny()
engine = postgres_conn()

chinese_caixin_services_index = "chinese_caixin_services_index"
usd_cny = "usd_cny"
schema_bronze = "bronze"

def extract_load_bronze():
    try:
        df_chinese_caixin.rename(
            columns={
                "Date": "date",
                "Actual": "actual_state",
                "Forecast": "forecast",
                "Previous": "previous"
            }, inplace=True
        )

        create_chinese_caixin = """
            CREATE TABLE IF NOT EXISTS bronze.chinese_caixin_services_index (
                id SERIAL PRIMARY KEY,
                date TEXT,
                actual_state TEXT,
                forecast TEXT,
                previous TEXT
            );
            """
        
        with engine.connect() as conn:
            conn.execute(text(create_chinese_caixin))
            conn.commit()

        df_chinese_caixin.to_sql(
            chinese_caixin_services_index, 
            engine, 
            schema=schema_bronze, 
            if_exists='append', 
            index=False
        )

        df_usd_cny.rename(
            columns={
                "Date": "date",
                "Último": "close",
                "Abertura": "opening",
                "Máxima": "high",
                "Mínima": "low",
                "Vol.": "volume",
                "Var%": "variation"
            }, inplace=True
        )

        create_usd_cny = """
            CREATE TABLE IF NOT EXISTS bronze.usd_cny (
                id SERIAL PRIMARY KEY,
                date TEXT,
                close TEXT,
                opening TEXT,
                high TEXT,
                low TEXT,
                volume TEXT,
                variation TEXT
            );
            """
       
        with engine.connect() as conn:
            conn.execute(text(create_usd_cny))
            conn.commit()

        df_usd_cny.to_sql(
            usd_cny, 
            engine, 
            schema=schema_bronze, 
            if_exists='append', 
            index=False
        )
    except Exception as e:
        print(f"Erro ao inserir dados no banco: {e}")
