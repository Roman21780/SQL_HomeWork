# Задание 2: Запрос для выборки магазинов, продающих целевого издателя.
# Напишем скрипт, который подключается к базе данных, принимает имя
# или идентификатор издателя и выводит информацию о продажах его книг.

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

from ORM.Python_BD_ORM1 import Publisher, Book, Shop, Stock, Sale

# Параметры подключения к базе данных
DSN = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}\
@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DSN)
Session = sessionmaker(bind=engine)
session = Session()

# Ввод имени или идентификатора издателя
publisher_input = input("Введите имя или идентификатор издателя: ")

try:
    publisher_id = int(publisher_input)
    publisher = session.query(Publisher).filter(Publisher.id == publisher_id).first()
except ValueError:
    publisher = session.query(Publisher).filter(Publisher.name == publisher_input).first()

if publisher:
    # Запрос для выборки данных
    sales_info = session.query(
        Book.title,
        Shop.name,
        Sale.price,
        Sale.date_sale
    ).join(Stock, Book.id == Stock.id_book)\
    .join(Shop, Stock.id_shop == Shop.id)\
    .join(Sale, Stock.id == Sale.id_stock)\
    .filter(Book.id_publisher == publisher.id)\
    .all()

    # Вывод результатов
    for title, shop_name, price, date_sale in sales_info:
        print(f"{title} | {shop_name} | {price} | {date_sale.strftime('%d-%m-%Y')}")
else:
    print("Издатель не найден.")

