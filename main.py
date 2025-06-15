import streamlit as st
from azure.storage.blob import BlobServiceClient
import os
import uuid
import pyodbc
import json
from dotenv import load_dotenv
load_dotenv()

blobConnectionString = os.getenv("BLOB_CONNECTION_STRING")
blobContainerName = os.getenv("BLOB_CONTAINER_NAME")
blobAccountName = os.getenv("BLOB_ACCOUNT_NAME")

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")
SQL_USER = os.getenv("SQL_USER")
SQL_PASSWORD = os.getenv("SQL_PASSWORD")

st.title("Cadastro de Produtos")

# Formulário de cadastro de produtos
product_name = st.text_input("Nome do Produto")
product_description = st.text_area("Descrição do Produto")
product_price = st.number_input("Preço do Produto", min_value=0.0, format="%.2f")
product_image = st.file_uploader("Imagem do Produto", type=["jpg", "jpeg", "png"])

# Função para salvar imagem no blob storage
def upload_blob(file):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(blobConnectionString)
        container_client = blob_service_client.get_container_client(blobContainerName)
        blob_name = str(uuid.uuid4()) + "_" + file.name # Adicionei o nome original do arquivo para melhor organização
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(file.read(), overwrite=True)
        image_url = f"https://{blobAccountName}.blob.core.windows.net/{blobContainerName}/{blob_name}"
        return image_url
    except Exception as e:
        st.error(f"Erro ao fazer upload da imagem: {e}")
        return None

#Função para inserir produto no banco de dados
def insert_product(product_name, product_description, product_price, uploaded_file): # Renomeei product_image para uploaded_file
    image_url = None
    if uploaded_file is not None:
        image_url = upload_blob(uploaded_file)
        if image_url is None: # Se o upload falhar, não continue
            return False

    try:
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};" # Note as chaves duplas para escapar no f-string
            f"SERVER={SQL_SERVER};"
            f"DATABASE={SQL_DATABASE.strip()};" # Adicionado .strip() para remover espaços em branco
            f"UID={SQL_USER};"
            f"PWD={SQL_PASSWORD}"
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()

        insert_sql = "INSERT INTO Produtos (nome, descricao, preco, imagem_url) VALUES (?, ?, ?, ?)"
        cursor.execute(insert_sql, (product_name, product_description, product_price, image_url))

        conn.commit()
        cursor.close()
        conn.close()
        return True
    except pyodbc.Error as ex: # Tratamento de erro mais específico para pyodbc
        sqlstate = ex.args[0]
        st.error(f"Erro no SQL Server (Código: {sqlstate}): {ex}")
        return False
    except Exception as e:
        st.error(f"Erro inesperado ao inserir produto: {e}")
        return False

# Função para listar produtos do banco de dados
def list_products():
    rows = []
    try:
        conn_str = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={SQL_SERVER};"
            f"DATABASE={SQL_DATABASE.strip()};"
            f"UID={SQL_USER};"
            f"PWD={SQL_PASSWORD}"
        )
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT nome, descricao, preco, imagem_url FROM Produtos")

        # Obtém os nomes das colunas para criar dicionários (opcional, mas bom para clareza)
        columns = [column[0] for column in cursor.description]
        for row in cursor.fetchall():
            rows.append(dict(zip(columns, row))) # Converte tuplas em dicionários

        cursor.close()
        conn.close()
        return rows
    except pyodbc.Error as ex: # Tratamento de erro mais específico para pyodbc
        sqlstate = ex.args[0]
        st.error(f"Erro no SQL Server ao listar produtos (Código: {sqlstate}): {ex}")
        return []
    except Exception as e:
        st.error(f"Erro inesperado ao listar produtos: {e}")
        return []

# Função para exibir a lista de produtos
def list_products_screen():
    products = list_products()
    if products:
        # Define o número de cards por linha
        cards_por_linha = 3
        # Cria as colunas iniciais
        cols = st.columns(cards_por_linha)
        for i, product in enumerate(products):
            col = cols[i % cards_por_linha]
            with col:
                st.markdown(f"### {product['nome']}") # Acessando por chave se for dicionário
                st.write(f"**Descrição:** {product['descricao']}") # Acessando por chave
                st.write(f"**Preço:** R$ {product['preco']:.2f}") # Acessando por chave
                if product["imagem_url"]:
                    # Acessando por chave
                    # Use st.image diretamente para imagens de URLs no Streamlit
                    st.image(product["imagem_url"], width=200, caption=product['nome'])
                st.markdown("---")
            # A cada 'cards_por_linha' produtos, se ainda houver produtos, cria novas colunas
            if (i + 1) % cards_por_linha == 0 and (i + 1) < len(products):
                cols = st.columns(cards_por_linha)
    else:
        st.info("Nenhum produto cadastrado.")

if st.button("Salvar Produto"):
    if not product_name or not product_description or product_price is None:
        st.warning("Por favor, preencha todos os campos obrigatórios!")
    elif product_image is None: # Adiciona validação para imagem
        st.warning("Por favor, selecione uma imagem para o produto!")
    else:
        if insert_product(product_name, product_description, product_price, product_image):
            st.success("Produto salvo com sucesso!") # 
            list_products_screen()
        else:
            st.error("Falha ao salvar o produto.")

st.header("Produtos Cadastrados")

if st.button("Listar Produtos"):
    list_products_screen()
    st.info("Lista de produtos carregada!") # Exibir mensagem diretamente no Streamlit