from connections import postgres_conn
from flights_searching import data_merge


try:
    engine = postgres_conn()
    data_merge().to_sql(
    "best_flights", 
    engine, 
    schema="bronze", 
    if_exists='append', 
    index=False
    )
except Exception as e:
    print(e)
