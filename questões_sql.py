import pandas as pd
from sqlalchemy import create_engine

# 1. CONFIGURAÇÃO DA CONEXÃO COM O BANCO DE DADOS

USER = "looqbox-challenge"
PASS = "looq-challenge"
IP = "35.199.115.174"
SCHEMA = "looqbox-challenge"

engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASS}@{IP}/{SCHEMA}")

# 2. QUERIES DO TESTE SQL

# QUESTÃO 1: Quais são os 10 produtos mais caros da empresa?
query_1 = """
SELECT PRODUCT_COD, PRODUCT_NAME, PRODUCT_VAL
FROM data_product
ORDER BY PRODUCT_VAL DESC
LIMIT 10;
"""

# QUESTÃO 2: Quais são as seções dos departamentos 'BEBIDAS' e 'PADARIA'?
query_2 = """
SELECT DISTINCT SECTION_NAME, DEP_NAME
FROM data_product
WHERE DEP_NAME IN ('BEBIDAS', 'PADARIA');
"""

# QUESTÃO 3: Total de vendas de produtos por área de negócios no Q1 de 2019
query_3 = """
SELECT 
    c.BUSINESS_NAME,
    SUM(s.SALES_VALUE) AS TOTAL_SALES
FROM data_store_cad c
JOIN data_product_sales s ON c.STORE_CODE = s.STORE_CODE
WHERE s.DATE BETWEEN '2019-01-01' AND '2019-03-31'
GROUP BY c.BUSINESS_NAME
ORDER BY TOTAL_SALES DESC;
"""

# 3. EXECUÇÃO E EXIBIÇÃO DOS RESULTADOS NO TERMINAL

try:
    print("--- RESULTADO QUESTÃO 1 ---")
    df_q1 = pd.read_sql(query_1, con=engine)
    print(df_q1.to_string(index=False)) # Imprime a tabela limpa sem o índice lateral
    print("\n" + "="*50 + "\n")
    
    print("--- RESULTADO QUESTÃO 2 ---")
    df_q2 = pd.read_sql(query_2, con=engine)
    print(df_q2.to_string(index=False))
    print("\n" + "="*50 + "\n")
    
    print("--- RESULTADO QUESTÃO 3 ---")
    df_q3 = pd.read_sql(query_3, con=engine)
    print(df_q3.to_string(index=False))

except Exception as e:
    print(f"Erro ao executar consultas SQL: {e}")