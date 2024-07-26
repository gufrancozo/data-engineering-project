# Data Engineering Project

Este projeto coleta dados do site Books to Scrape e os insere em um banco de dados PostgreSQL.


## Configurações

- Instale as dependências: pip install -r requirements.txt


- Abra o "SQL Shell (psql)" e conecte-se como usuário postgres

- Crie o banco de dados e a tabela: 

CREATE DATABASE bookclub;
\c bookclub
CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    category VARCHAR(255),
    price VARCHAR(50),
    availability VARCHAR(50)
);

- Execute o script: python book_scraper.py

## Dependências

- selenium
- beautifulsoup4
- webdriver_manager
- psycopg2-binary
## Autores

- [@gufrancozo](https://github.com/gufrancozo)
