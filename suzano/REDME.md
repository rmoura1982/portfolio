
# Coleta de Dados Financeiros - USD/CNY & Caixin Chinês

## Arquitetura

Este projeto coleta dados diários e mensais de taxas de câmbio USD/CNY e serviços Caixin Chinês diretamente do **Investing.com**. Os dados passam por um pipeline de transformação em 3 camadas (**Bronze**, **Silver**, **Gold**), com todo o processo orquestrado no **Google Cloud** usando **Airflow**.

### 📊 Arquitetura Geral

![Arquitetura](./architeture/architecture.jpg)

### Componentes principais

- **Fontes de Dados**
  - Taxas diárias de USD/CNY e serviços Caixin Chinês
  - Taxas mensais de USD/CNY desde 1991

- **Google Cloud**
  - **Google Cloud Storage (GCS)** → Armazenamento nas camadas Bronze, Silver e Gold
  - **Cloud Composer (Airflow)** → Orquestração do pipeline

- **Pipeline ETL (Airflow)**
  - **Bronze** → Dados brutos coletados e armazenados no GCS
  - **Silver** → Dados limpos e transformados no GCS
  - **Gold** → Dados limpos e transformados conforme regras de negócio; BigQuery apenas consome

## Funcionalidade do Pipeline

- **Coleta** → Scraping diário e mensal do Investing.com
- **Transformação** → Limpeza e preparação na Silver
- **Carga** → Script Python carrega os dados finais na Gold

## Acessos e Usos

- **Silver** → Cientistas de dados acessam para modelagem e machine learning
- **Gold** → Time de negócios acessa para insights e relatórios; BigQuery consome para análises

## Requisitos

- Python 3.x
- Google Cloud SDK configurado
- Apache Airflow
- Bibliotecas no `requirements.txt`:
  - `pandas`, `requests`, `beautifulsoup4`
  - `google-cloud-storage`, `google-cloud-bigquery`
  - `apache-airflow`

## Como Executar

1. **Configurar Google Cloud**
   - Configure GCS e BigQuery
   - Crie buckets no GCS e datasets no BigQuery

2. **Instalar dependências**
   ```bash
   pip install -r requirements.txt
   ```

## Compartilhamento do Banco de Dados

O banco de dados **db_suzano** foi compartilhado através do arquivo de backup **db_suzano.dump**.

### Como Restaurar o Banco de Dados

Para restaurar o banco de dados a partir do arquivo **db_suzano.dump**, use o seguinte comando no **shell do PostgreSQL**:

```bash
pg_restore -U postgres -d db_suzano -v "C:/path/banco/db_suzano.dump"
```

Isso irá restaurar todos os dados e a estrutura do banco **db_suzano** a partir do arquivo de backup.
