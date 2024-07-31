import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=48), unique=True)

    # Создание связи с таблицей "book"
    books = relationship("Book", back_populates='publishers', cascade="all, delete-orphan")

    def __str__(self):
        return f'Publisher:\n\tid - {self.id}\n\tname - {self.name}\n'
    
class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=48), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey('publisher.id'), nullable=False)

    # Создание связи с таблицами "publisher", "stock"
    publishers = relationship("Publisher", back_populates='books')

    stocks = relationship("Stock", back_populates='books', cascade="all, delete-orphan")

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=48), nullable=False)

    # Создание связи с таблицей "stock"
    stocks = relationship("Stock", back_populates="shops", cascade="all, delete-orphan")

class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    # Создание связи с таблицами "book", "shop", "sale"
    books = relationship("Book", back_populates="stocks")
    shops = relationship("Shop", back_populates="stocks")

    sales = relationship("Sale", back_populates="stocks")

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Integer, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)

    # Создание связи с таблицей "stock"
    stocks = relationship("Stock", back_populates="sales")

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
