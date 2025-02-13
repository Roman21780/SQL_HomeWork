# Задание 1: Создание моделей SQLAlchemy
# На основе предоставленной схемы создадим модели для таблиц:
# Publisher, Book, Shop, Stock, Sale.

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из файла .env
load_dotenv()

# Создаем базовый класс для моделей
Base = declarative_base()

class Publisher(Base):
    __tablename__ = 'publisher'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    books = relationship('Book', back_populates='publisher')

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    id_publisher = Column(Integer, ForeignKey('publisher.id'), nullable=False)

    publisher = relationship('Publisher', back_populates='books')
    stocks = relationship('Stock', back_populates='book')

class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    stocks = relationship('Stock', back_populates='shop')

class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'), nullable=False)
    id_shop = Column(Integer, ForeignKey('shop.id'), nullable=False)
    count = Column(Integer, nullable=False)

    book = relationship('Book', back_populates='stocks')
    shop = relationship('Shop', back_populates='stocks')
    sales = relationship('Sale', back_populates='stock')

class Sale(Base):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    date_sale = Column(Date, nullable=False)
    id_stock = Column(Integer, ForeignKey('stock.id'), nullable=False)
    count = Column(Integer, nullable=False)

    stock = relationship('Stock', back_populates='sales')

# Подключение к базе данных
DSN = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}\
@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DSN)

# Создание таблиц в базе данных
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()