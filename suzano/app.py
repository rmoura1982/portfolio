from bronze_postgres_loader import extract_load_bronze
from silver_processing import tranform_load_silver
from gold_processing import rule_load_gold


def app():
    extract_load_bronze()
    print("Extração e carregamento na bronze concluída!")

    tranform_load_silver()
    print("Transformação/Carregamento na Silver concluída!")

    print("Transformação/Carregamento na Gold concluída!")
    rule_load_gold()

if __name__ == "__main__":
    app()
    