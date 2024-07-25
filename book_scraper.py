import psycopg2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# Configuração do driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get('http://books.toscrape.com/')

# Coleta de dados
content = driver.page_source
soup = BeautifulSoup(content, 'html.parser')

books = []
for book in soup.findAll('article', class_='product_pod'):
    name = book.h3.a['title']
    category = book.find('p', class_='star-rating')['class'][1]
    price = book.find('p', class_='price_color').text
    availability = book.find('p', class_='instock availability').text.strip()
    books.append((name, category, price, availability))

driver.quit()

# Inserção de dados no banco de dados
conn = psycopg2.connect("dbname=bookclub user=seu_usuario password=sua_senha")
cursor = conn.cursor()

for book in books:
    cursor.execute("INSERT INTO books (name, category, price, availability) VALUES (%s, %s, %s, %s)", 
                   book)

conn.commit()
cursor.close()
conn.close()
