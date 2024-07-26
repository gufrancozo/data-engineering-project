import psycopg2
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Configurar logging
logging.basicConfig(filename='book_scraper.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Configuração do driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    driver.get('http://books.toscrape.com/')
    books = []

    for page in range(1, 51):  # Supondo 50 páginas para exemplo
        driver.get(f'http://books.toscrape.com/catalogue/page-{page}.html')
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')

        for book in soup.findAll('article', class_='product_pod'):
            name = book.h3.a['title']
            category = book.find('p', class_='star-rating')['class'][1]
            price = book.find('p', class_='price_color').text
            availability = book.find('p', class_='instock availability').text.strip()
            books.append((name, category, price, availability))

    driver.quit()

    # Inserção de dados no banco de dados
    try:
        conn = psycopg2.connect(
            dbname="bookclub",
            user="postgres",
            password="140501",
            host="localhost"
        )
        cursor = conn.cursor()

        for book in books:
            cursor.execute("SELECT id FROM books WHERE name=%s AND category=%s AND price=%s AND availability=%s", 
                           (book[0], book[1], book[2], book[3]))
            result = cursor.fetchone()
            if not result:
                cursor.execute("INSERT INTO books (name, category, price, availability) VALUES (%s, %s, %s, %s)", 
                               (book[0], book[1], book[2], book[3]))

        conn.commit()
        cursor.close()
        conn.close()
        logging.info("Dados inseridos com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao inserir dados no banco de dados: {e}")

except Exception as e:
    logging.error(f"Erro ao coletar dados: {e}")
finally:
    driver.quit()
