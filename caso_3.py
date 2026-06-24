import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

# Conexão
USER = "looqbox-challenge"
PASS = "looq-challenge"
IP = "35.199.115.174"
SCHEMA = "looqbox-challenge"
engine = create_engine(f"mysql+mysqlconnector://{USER}:{PASS}@{IP}/{SCHEMA}")

try:
    # 1. Carregar os dados do IMDB para o Pandas
    df_imdb = pd.read_sql("SELECT * FROM IMDB_movies LIMIT 500;", con=engine)
    
    # Mostrar as colunas para sabermos os nomes exatos
    print("Colunas encontradas na tabela IMDB_movies:")
    columns = df_imdb.columns.tolist()
    print(columns)
    
    # Identificar mapeamento dinâmico das colunas mais comuns de nota e gênero
    col_nota = [c for c in columns if 'score' in c.lower() or 'rating' in c.lower() or 'val' in c.lower()][0]
    col_genero = [c for c in columns if 'genre' in c.lower() or 'cat' in c.lower()][0]
    
    print(f"\nGerando gráfico usando as colunas: {col_nota} e {col_genero}")
    
    # 2. Criar a Visualização: Média de Nota por Gênero
    df_plot = df_imdb.groupby(col_genero)[col_nota].mean().reset_index().sort_values(by=col_nota, ascending=False).head(10)
    
    # Configuração do gráfico usando Seaborn e Matplotlib
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    
    # Criando o gráfico de barras
    ax = sns.barplot(x=col_nota, y=col_genero, data=df_plot, palette="viridis")
    
    # Títulos e rótulos
    plt.title('Top 10 Gêneros de Filmes com Maiores Notas Médias no IMDB', fontsize=14, pad=15)
    plt.xlabel('Nota Média do IMDB', fontsize=12)
    plt.ylabel('Gênero', fontsize=12)
    
    # Ajustar layout para não cortar texto
    plt.tight_layout()
    
    # Salvar o gráfico como imagem
    plt.savefig('grafico_imdb.png', dpi=300)
    print("\nGráfico gerado com sucesso e salvo como 'grafico_imdb.png'")
    plt.show()

except Exception as e:
    print("\nErro ao gerar o gráfico:")
    print(e)
    print("Listar as colunas disponíveis para corrigir:")
    try:
        df_error = pd.read_sql("SELECT * FROM IMDB_movies LIMIT 1;", con=engine)
        print(df_error.columns.tolist())
    except:
        pass