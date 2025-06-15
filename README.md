# Catálogo de Produtos E-commerce com Azure e Streamlit

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Azure SQL Database](https://img.shields.io/badge/Azure%20SQL%20Database-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)
![Azure Blob Storage](https://img.shields.io/badge/Azure%20Blob%20Storage-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)

## 📝 Descrição do Projeto

Este projeto é uma aplicação web interativa desenvolvida em Python com Streamlit, focada no gerenciamento de produtos para um e-commerce. Ele foi criado como parte do módulo "Microsoft Azure Cloud Native" da Digital Innovation One (DIO), com o objetivo de demonstrar a integração de serviços essenciais da Microsoft Azure para construir aplicações escaláveis e resilientes na nuvem.

A aplicação permite aos usuários:
* Cadastrar novos produtos, incluindo nome, descrição, preço e uma imagem.
* Realizar o upload seguro das imagens dos produtos para o **Azure Blob Storage**.
* Persistir as informações textuais dos produtos (nome, descrição, preço e a URL da imagem) em um **Azure SQL Database**.
* Visualizar uma lista de todos os produtos cadastrados, com suas respectivas imagens.

## ⚙️ Arquitetura da Solução

A arquitetura deste projeto é baseada em serviços cloud da Microsoft Azure para prover uma solução robusta e escalável:

* **Frontend (Streamlit):** A interface do usuário é construída com Streamlit em Python, oferecendo um formulário para cadastro e uma área para listagem dos produtos.
* **Armazenamento de Imagens (Azure Blob Storage):** As imagens dos produtos são enviadas e armazenadas em um contêiner no Azure Blob Storage, otimizado para dados não estruturados e com acesso via URL.
* **Banco de Dados (Azure SQL Database):** Os dados textuais dos produtos (nome, descrição, preço, e a URL da imagem no Blob Storage) são persistidos em uma tabela no Azure SQL Database, um serviço de banco de dados relacional gerenciado.

## 🚀 Tecnologias Utilizadas

* **Python 3.13.5:** Linguagem de programação principal.
* **Streamlit:** Framework para criação da interface web interativa.
* **Microsoft Azure Blob Storage:** Serviço de armazenamento de objetos para imagens.
* **Microsoft Azure SQL Database:** Banco de dados relacional gerenciado para dados estruturados.
* **`pyodbc`:** Biblioteca Python para conexão com o SQL Server.
* **`azure-storage-blob`:** SDK Python para interagir com o Azure Blob Storage.
* **`python-dotenv`:** Para gerenciamento seguro de variáveis de ambiente.

## 📋 Pré-requisitos

Antes de executar o projeto, certifique-se de ter os seguintes pré-requisitos:

* **Python 3.13.5** instalado.
* Uma **Conta Azure** ativa.
* **ODBC Driver 17 for SQL Server** instalado (necessário para `pyodbc` se estiver usando).

### Configuração no Azure

1.  **Azure SQL Database:**
    * Crie um **Azure SQL Server** e um **Azure SQL Database** no portal do Azure.
    * Configure as **regras de firewall** do seu SQL Server para permitir conexões do seu endereço IP local ou permitir o acesso de "Serviços e recursos do Azure" (se for fazer deploy).
    * Obtenha o nome do seu servidor (`SERVER_NAME`), nome do banco de dados (`DATABASE_NAME`), usuário (`USERNAME`) e senha (`PASSWORD`).
    * **Crie a tabela `Produtos`** no seu Azure SQL Database executando o seguinte script SQL:
        ```sql
        CREATE TABLE Produtos (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    nome NVARCHAR(255),
                    descricao NVARCHAR(MAX),
                    preco DECIMAL(18,2),
                    imagem_url NVARCHAR(2083)
                );
        ```
        
2.  **Azure Storage Account:**
    * Crie uma **Azure Storage Account** no portal do Azure.
    * Dentro dela, crie um **Blob Container** com o nome `produtos`.
    * Defina o **nível de acesso** do contêiner para **"Blob"** (acesso anônimo de leitura para blobs) para que as imagens possam ser exibidas publicamente pela URL.
    * Obtenha a **Connection String** da sua Storage Account (em "Access keys").
    * Obtenha o **Nome da sua Conta de Armazenamento** (ex: `stadiolab01`).

## 🔑 Configuração de Variáveis de Ambiente

Este projeto utiliza variáveis de ambiente para gerenciar as credenciais de forma segura. Crie um arquivo chamado `.env` na raiz do projeto (no mesmo diretório de `main.py`) e preencha-o com suas informações do Azure:

```dotenv
BLOB_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=SEU_ACCOUNT_NAME;AccountKey=SUA_ACCOUNT_KEY;EndpointSuffix=core.windows.net"
BLOB_CONTAINER_NAME="produtos" # Este nome deve ser 'produtos' conforme configurado
BLOB_ACCOUNT_NAME="SEU_ACCOUNT_NAME"

SQL_SERVER="SEU_SQL_SERVER.database.windows.net"
SQL_DATABASE="SEU_SQL_DATABASE"
SQL_USER="SEU_SQL_USER"
SQL_PASSWORD="SUA_SQL_PASSWORD"
```

## ▶️ Como Rodar o Projeto Localmente

Siga os passos abaixo para clonar o repositório, configurar o ambiente e executar a aplicação Streamlit no seu computador.

### Passo 1: Clonar o Repositório

Primeiro, você precisa baixar o código do seu projeto para a sua máquina local.

1.  Abra seu terminal ou prompt de comando.
2.  Use o comando `git clone` seguido da URL do seu repositório no GitHub. **Lembre-se de substituir `SEU_USUARIO` e `SEU_REPOSITORIO` pelos seus dados reais, ou mantenha seu link já corrigido.**
    ```bash
    git clone https://github.com/LZanata/azure-streamlit-product-catalog.git
    ```
3.  Entre na pasta do projeto recém-clonado:
    ```bash
    cd azure-streamlit-product-catalog
    ```

### Passo 2: Configurar o Ambiente Virtual (Recomendado)

É uma boa prática usar um ambiente virtual para isolar as dependências do seu projeto e evitar conflitos com outras instalações Python no seu sistema.

1.  Dentro da pasta do projeto, crie o ambiente virtual:
    ```bash
    python -m venv venv
    ```
2.  Ative o ambiente virtual:
    * **No Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **No macOS / Linux:**
        ```bash
        source venv/bin/activate
        ```
    Você saberá que o ambiente está ativo quando o nome `(venv)` aparecer antes do prompt do seu terminal.

### Passo 3: Instalar as Dependências

Com o ambiente virtual ativo, instale todas as bibliotecas Python necessárias para o projeto. Elas estão listadas no arquivo `requirements.txt`.

1.  Execute o seguinte comando:
    ```bash
    pip install -r requirements.txt
    ```

### Passo 4: Configurar as Variáveis de Ambiente

Para que o projeto se conecte aos seus serviços do Azure, você precisa informar as credenciais. **Nunca adicione essas credenciais diretamente ao código ou ao repositório Git!** Em vez disso, usaremos um arquivo `.env` para isso.

1.  Na pasta raiz do seu projeto (a mesma onde estão `main.py` e `requirements.txt`), crie um novo arquivo chamado **`.env`**.
2.  Copie o conteúdo abaixo para o arquivo `.env` e **substitua os valores entre aspas pelos seus próprios dados do Azure**.
    ```dotenv
    BLOB_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=SEU_ACCOUNT_NAME;AccountKey=SUA_ACCOUNT_KEY;EndpointSuffix=core.windows.net"
    BLOB_CONTAINER_NAME="produtos" # Este nome deve ser 'produtos' conforme configurado
    BLOB_ACCOUNT_NAME="SEU_ACCOUNT_NAME"

    SQL_SERVER="SEU_SQL_SERVER.database.windows.net"
    SQL_DATABASE="SEU_SQL_DATABASE"
    SQL_USER="SEU_SQL_USER"
    SQL_PASSWORD="SUA_SQL_PASSWORD"
    ```
    * Para `BLOB_CONNECTION_STRING`, obtenha nas "Access keys" da sua Storage Account.
    * Para `BLOB_ACCOUNT_NAME`, é o nome da sua Storage Account.
    * Para `SQL_SERVER`, `SQL_DATABASE`, `SQL_USER`, `SQL_PASSWORD`, use os dados do seu Azure SQL Database que você criou e configurou.

3.  **Certifique-se de que o arquivo `.env` está listado no seu `.gitignore`** para que ele nunca seja enviado ao GitHub.

### Passo 5: Executar a Aplicação Streamlit

Com todas as dependências instaladas e as variáveis de ambiente configuradas, você pode iniciar a aplicação Streamlit.

1.  Ainda no terminal (com o ambiente virtual ativo), execute o comando:
    ```bash
    streamlit run main.py
    ```
2.  Após alguns segundos, seu navegador padrão será automaticamente aberto, exibindo a aplicação Streamlit, geralmente no endereço `http://localhost:8501`.

Agora você está pronto para interagir com o "Gerenciador de Produtos Cloud-Native"!

## ✨ Insights e Aprendizados

Durante o desenvolvimento deste projeto, pude aprofundar meus conhecimentos e obter os seguintes insights:

* **Modularidade e Cloud Native:** Compreendi a importância de arquiteturas cloud-native, onde diferentes serviços gerenciados (Azure SQL, Blob Storage) são utilizados para tarefas específicas, garantindo escalabilidade, segurança e alta disponibilidade.
* **Gerenciamento de Dados:** Aprendi a lidar com diferentes tipos de dados (textuais e binários de imagem) utilizando os serviços mais adequados do Azure para cada um, otimizando o armazenamento e acesso.
* **Agilidade com Streamlit:** A experiência com Streamlit demonstrou a rapidez e facilidade em transformar scripts Python em aplicações web interativas e funcionais, ideal para prototipagem e ferramentas internas.
* **Segurança e Boas Práticas:** A utilização de variáveis de ambiente com `python-dotenv` reforçou a importância de não expor credenciais diretamente no código-fonte, um pilar fundamental em desenvolvimento seguro.
* **Depuração e Resolução de Problemas:** Enfrentei desafios relacionados à conexão com o Azure SQL e permissões no Blob Storage, o que me permitiu praticar habilidades de depuração e consulta à documentação oficial da Microsoft.

## 🛣️ Próximos Passos e Melhorias Futuras

Algumas funcionalidades e aprimoramentos que podem ser implementados:

* **Funcionalidades CRUD Completas:** Adicionar opções para editar e excluir produtos.
* **Autenticação de Usuários:** Implementar um sistema de login para gerenciar o acesso (ex: usando Azure Active Directory B2C).
* **Paginação e Filtros:** Para uma melhor experiência do usuário em catálogos grandes.
* **Deploy Contínuo (CI/CD):** Configurar um pipeline de CI/CD (ex: com GitHub Actions) para automatizar o deploy da aplicação Streamlit no Azure App Service ou Azure Container Apps.
* **Otimização de Imagens:** Redimensionar e comprimir imagens antes do upload para economizar espaço e melhorar o desempenho.

## 🤝 Contribuição

Contribuições são bem-vindas! Se você tiver sugestões ou melhorias, sinta-se à vontade para abrir uma issue ou enviar um pull request.