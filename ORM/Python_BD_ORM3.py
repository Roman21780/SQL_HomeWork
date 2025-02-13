# Задание 3: Заполнение базы данных тестовыми данными из JSON-файла.

import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ORM.Python_BD_ORM1 import Publisher, Book, Shop, Stock, Sale, Base
from dotenv import load_dotenv
import os

# Параметры подключения к базе данных
DSN = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DSN)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Чтение данных из JSON-файла
with open(r'C:\\SQL\SQL_HomeWork\ORM\tests_data.json', 'r') as fd:
    data = json.load(fd)

# Заполнение базы данных
for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))

session.commit()
