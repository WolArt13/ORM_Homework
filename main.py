import sqlalchemy, datetime
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Book, Stock, Shop, Sale

login = input("Логин БД: ")
password = input("Пароль БД: ")
db_name = input("Название БД: ")

DSN = f"postgresql://{login}:{password}@localhost:5432/{db_name}"
engine = sqlalchemy.create_engine(DSN)

Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)

# Вносим авторов в таблицу "publisher"
Pushkin = Publisher(name = "А.С.Пушкин")
Lermontov = Publisher(name = "М.Ю.Лермонтов")
Tolstoy = Publisher(name = "Л.Н.Толстой")

session.add_all([Pushkin,
                 Lermontov,
                 Tolstoy])

session.commit()

# Вносим книги в таблицу "book"
Evgeny_Onegin = Book(title = "Евгений Онегин", id_publisher = 1)
Captain_daughter = Book(title = "Капитанская Дочка", id_publisher = 1)
Ruslan_and_Ludmila = Book(title = "Руслан и Людмила", id_publisher = 1)

Geroy = Book(title = "Герой нашего времени", id_publisher = 2)
Mascarade = Book(title = "Маскарад", id_publisher = 2)
Borodino = Book(title = "Бородино", id_publisher = 2)

War_and_Peace = Book(title = "Война и мир", id_publisher = 3)
Anna_Korelina = Book(title = "Анна Корелина", id_publisher = 3)
Kavkazky_Plennyk = Book(title = "Кавказский пленник", id_publisher = 3)

session.add_all([Evgeny_Onegin, Captain_daughter, Ruslan_and_Ludmila,
                 Geroy, Mascarade, Borodino,
                 War_and_Peace, Anna_Korelina, Kavkazky_Plennyk])

session.commit()

# Вносим магазины в таблицу "shop"
Bukvoed = Shop(name = "Буквоед")
Labirint = Shop(name = "Лабиринт")
Knizhny_Dom = Shop(name = "Книжный дом")

session.add_all([Bukvoed,
                 Labirint,
                 Knizhny_Dom])

session.commit()

# Вносим количество книг в магазинах в таблицу "stock"
Evgeny_Onegin1 = Stock(id_book = 1, id_shop = 3, count = 34)

Captain_daughter1 = Stock(id_book = 2, id_shop = 1, count = 21)
Captain_daughter2 = Stock(id_book = 2, id_shop = 2, count = 16)

Ruslan_and_Ludmila1 = Stock(id_book = 3, id_shop = 1, count = 23)

Geroy1 = Stock(id_book = 4, id_shop = 1, count = 19)
Geroy2 = Stock(id_book = 4, id_shop = 2, count = 14)
Geroy3 = Stock(id_book = 4, id_shop = 3, count = 16)

Mascarade1 = Stock(id_book = 5, id_shop = 2, count = 8)

Borodino1 = Stock(id_book = 6, id_shop = 1, count = 19)
Borodino2 = Stock(id_book = 6, id_shop = 3, count = 21)

War_and_Peace1 = Stock(id_book = 7, id_shop = 1, count = 38)
War_and_Peace2 = Stock(id_book = 7, id_shop = 2, count = 9)
War_and_Peace3 = Stock(id_book = 7, id_shop = 3, count = 17)

Anna_Korelina1 = Stock(id_book = 8, id_shop = 2, count = 10)

Kavkazky_Plennyk1 = Stock(id_book = 9, id_shop = 3, count = 11)

session.add_all([Evgeny_Onegin1,
                 Captain_daughter1, Captain_daughter2,
                 Ruslan_and_Ludmila1,
                 Geroy1, Geroy2, Geroy3,
                 Mascarade1,
                 Borodino1, Borodino2,
                 War_and_Peace1, War_and_Peace2, War_and_Peace3,
                 Anna_Korelina1,
                 Kavkazky_Plennyk1])

session.commit()

# Вносим информацию о продажах книг в таблицу "sale"
book1 = Sale(price = 576, date_sale = datetime.datetime(2024, 9, 20), id_stock = 1, count = 1)
book2 = Sale(price = 617, date_sale = datetime.datetime(2024, 7, 24), id_stock = 4, count = 2)
book3 = Sale(price = 842, date_sale = datetime.datetime(2024, 5, 17), id_stock = 5, count = 1)
book4 = Sale(price = 560, date_sale = datetime.datetime(2024, 2, 8), id_stock = 7, count = 3)
book5 = Sale(price = 654, date_sale = datetime.datetime(2024, 1, 21), id_stock = 9, count = 1)
book6 = Sale(price = 632, date_sale = datetime.datetime(2023, 12, 3), id_stock = 10, count = 8)
book7 = Sale(price = 487, date_sale = datetime.datetime(2023, 6, 5), id_stock = 11, count = 5)
book8 = Sale(price = 561, date_sale = datetime.datetime(2022, 7, 27), id_stock = 13, count = 2)

session.add_all([book1, book2, book3, book4,
                 book5, book6, book7, book8])

session.commit()

def get_shops(res_):
    """Функция для получения информации о продажах книг в магазинах"""
    query = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale
                        ).select_from(Shop).join(Stock).join(Book).join(Publisher).join(Sale)
    if res_.isdigit():
        query = query.filter(Publisher.id == res_).all()
    else:
        query = query.filter(Publisher.name.like(f"%{res_}%")).all()
    print(f'Информация о продажах книг в книжных магазинах: ')
    for title, name, price, date_sale in query:
        print(f'{title} | {name} | {price} | {date_sale}')


if __name__ == "__main__":
    res_ = input('Введите ID или имя автора: ')
    get_shops(res_)

session.close()