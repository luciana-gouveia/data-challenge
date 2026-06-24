import pandas as pd
from sqlalchemy import create_engine

# Conexão
USER = "looqbox-challenge"
PASS = "looq-challenge"
IP = "35.199.115.174"
SCHEMA = "looqbox-challenge"
engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASS}@{IP}/{SCHEMA}")

# 1. Obter as duas consultas 
query_1 = """
SELECT
      STORE_CODE,
      STORE_NAME,
      START_DATE,
      END_DATE,
      BUSINESS_NAME,
      BUSINESS_CODE
FROM data_store_cad
"""

query_2 = """
SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
FROM data_store_sales
WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
"""

try:
    print("--- CASO 2: PROCESSANDO DADOS NO PANDAS ---")
    
    # Carregando as consultas para o Pandas
    df_lojas = pd.read_sql(query_1, con=engine)
    df_vendas = pd.read_sql(query_2, con=engine)
    
    # Garantindo que a coluna DATE está no formato de data correto para filtrar
    df_vendas['DATE'] = pd.to_datetime(df_vendas['DATE'])
    
    # 2. Filtrando o período no Pandas: ['2019-10-01', '2019-12-31']
    df_vendas_filtrado = df_vendas[
        (df_vendas['DATE'] >= '2019-10-01') & (df_vendas['DATE'] <= '2019-12-31')
    ]
    
    # 3. Cruzando os DataFrames (Merge/Join) usando a coluna STORE_CODE
    df_consolidado = pd.merge(df_vendas_filtrado, df_lojas, on='STORE_CODE')
    
    # 4. Agrupando por Loja e Categoria (Business Name) e somando os valores/quantidades
    df_agrupado = df_consolidado.groupby(['STORE_NAME', 'BUSINESS_NAME']).agg({
        'SALES_VALUE': 'sum',
        'SALES_QTY': 'sum'
    }).reset_index()
    
    # 5. Calculando o Ticket Médio (TM)
    df_agrupado['TM'] = df_agrupado['SALES_VALUE'] / df_agrupado['SALES_QTY']
    
    # Formatando para ficar igual ao exemplo do cliente
    df_final = df_agrupado[['STORE_NAME', 'BUSINESS_NAME', 'TM']]
    df_final.columns = ['Loja', 'Categoria', 'TM']
    
    # Arredondando o TM para 2 casas decimais e ordenando por Loja
    df_final = df_final.round({'TM': 2}).sort_values(by='Loja')
    
    print("\nTabela Resultante:")
    print(df_final.to_string(index=False))

except Exception as e:
    print("Erro no processamento dos dados:")
    print(e)