from statistics import quantiles

from sqlalchemy.sql.base import elements
from abc import ABC, abstractmethod

class CreateLogMixin:
    def __init__(self, *args, **kwargs):
        print(f"Создан объект класса: {self.__class__.__name__}")
        # Сохраняем оригинальные аргументы без преобразования в float
        original_args = args
        print(f"Переданные аргументы: args={original_args}, kwargs={kwargs}")
        super().__init__(*args, **kwargs)

class BaseProduct(ABC):
    def __init__(self, name: str, description: str, price_: float, quantity: int):
        self.name = name
        self.description = description
        # Сохраняем значение без преобразования
        self._price = price_  # Приватный атрибут
        self.quantity = quantity
    def __str__(self):
        """Метод возвращает в строковом значении Имя продукта +  цену + количество"""
        return f'{self.name}, {self._price} руб. Остаток: {self.quantity} шт.'

    @abstractmethod
    def calculate_total_value(self):
        pass


class Product(CreateLogMixin, BaseProduct):
    """Класс, представляющий товар."""

    def __init__(self, name: str, description: str, price_: float, quantity: int):
        if not name or not name.strip():
            raise ValueError("Имя товара не может быть пустым")
        if not description or not description.strip():
            raise ValueError("Описание товара не может быть пустым")
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
            
        # Сначала вызываем миксин с оригинальными аргументами
        super().__init__(name, description, price_, quantity)
        
        # Затем преобразуем цену в float
        try:
            self._price = float(price_)
        except ValueError as e:
            raise ValueError(f"Не удалось преобразовать строку в float: '{price_}'") from e
        
        if self._price <= 0:
            raise ValueError("Цена должна быть положительной")
        if quantity < 0:
            raise ValueError("Количество не может быть отрицательным")
        # try:
        #     price_ = float(price_)
        # except ValueError as e:
        #     raise ValueError(f"Не удалось преобразовать строку в float: '{price_}'") from e
        #
        # if price_ <= 0:
        #     raise ValueError("Цена должна быть положительной")
        # if quantity < 0:
        #     raise ValueError("Количество не может быть отрицательным")
        # if not name or not name.strip():
        #     raise ValueError("Имя товара не может быть пустым")
        # if not description or not description.strip():
        #     raise ValueError("Описание товара не может быть пустым")


    # def __str__(self):
    #     """Метод возвращает в строковом значении Имя продукта +  цену + количество"""
    #     return f'{self.name}, {self._price} руб. Остаток: {self.quantity} шт.'

    def __add__(self, other):
        if type(self) != type(other):
             raise TypeError("Нельзя складывать товары разных типов!")
        price_product_1 = self._price # Цена товара №1
        quantity_product_1 = self.quantity # Количество товара №1
        # Сумарная стоимость товара №1
        total_price_product_1 =  price_product_1 * quantity_product_1
        
        price_product_2 = other._price # Цена товара №2
        quantity_product_2 = other.quantity # Количество товара №2
        # Сумарная стоимость товара №2
        total_price_product_2 = price_product_2 * quantity_product_2
        # Расчитываем общую стоимость товаров
        total_price_all_product = total_price_product_2 + total_price_product_1
        return total_price_all_product


    def calculate_total_value(self):
        return self._price * self.quantity

        # price_product_1 = self._price # Цена товара №1
        # quantity_product_1 = self.quantity # Количество товара №1
        # # Сумарная стоимость товара №1
        # total_price_product_1 =  price_product_1 * quantity_product_1
        #
        # price_product_2 = other._price # Цена товара №2
        # quantity_product_2 = other.quantity # Количество товара №2
        # # Сумарная стоимость товара №2
        # total_price_product_2 = price_product_2 * quantity_product_2
        # # Расчитываем общую стоимость товаров
        # total_price_all_product = total_price_product_2 + total_price_product_1
        # return total_price_all_product
        
    @property
    def price(self):
        """Геттер для цены."""
        return self._price

    @price.setter
    def price(self, value):
        """Сеттер для цены с проверкой."""
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self._price = value
            
    @classmethod
    def new_product(cls, product_info: dict):
        """Создаёт новый объект Product из словаря параметров."""
        return cls(
            name=product_info.get('name', ''),
            description=product_info.get('description', ''),
            price_=product_info.get('price'),
            quantity=product_info.get('quantity')
        )

class Smartphone(Product):
    def __init__(self, name: str, description: str, price_: float, quantity: int, efficiency, model, memory, color):
        super().__init__(name, description, price_, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

class LawnGrass(Product):
    def __init__(self, name: str, description: str, price_: float, quantity: int, country: str, germination_period: int, color: str):
        super().__init__(name, description, price_, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    """Класс, представляющий категорию товаров."""

    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list[Product]):
        Category.category_count += 1
        Category.product_count += len(products)
        self.name = name
        self.description = description
        self.__products = products

    def __str__(self):
        total_quantity = 0
        for product in self.__products:
            total_quantity += product.quantity
        return f'{self.name}, количество продуктов: {total_quantity} шт.'

    def average_price(self):# расчитываем средний ценник
        all_price_category = 0
        for i in self.__products:
            all_price_category += i.price
        try:
            total_average_price = all_price_category / len(self.__products)
            return total_average_price
        except ZeroDivisionError:
            return 0






    @property
    def products(self):
        """Возвращает список продуктов в виде строки."""
        return "\n".join(str(product) for product in self.__products)

    def __str__(self):
        """Магический метод для строкового представления категории."""
        return f"Категория: {self.name}\n" \
               f"Описание: {self.description}\n" \
               f"Количество товаров: {len(self.__products)}\n" \
               f"Список товаров: {self.products}\n"

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только объекты класса Product или его наследников")
        self.__products.append(product)
        Category.product_count += 1

    def remove_product(self, product):
        if product not in self.__products:
            raise ValueError("Продукт не найден в категории")
        self.__products.remove(product)
        Category.product_count -= 1


def main():
    new_product = Product("Тестовый продукт", "Описание для теста", 100.0, 5)
    product1 = Product(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.0,
        5
    )
    product2 = Product(
        "Iphone 15",
        "512GB, Gray space",
        210000.0,
        8
    )
    product3 = Product(
        "Xiaomi Redmi Note 11",
        "1024GB, Синий",
        31000.0,
        15
    )

    # Создание категорий
    smartphones = Category("Смартфоны", "Мобильные устройства", [])
    smartphones.add_product(product1)
    smartphones.add_product(product2)

    notebooks = Category("Ноутбуки", "Портативные компьютеры", [])
    notebooks.add_product(product3)

    print(
        f"{product1.name}\n"
        f"{product1.description}\n"
        f"{product1._price}\n"
        f"{product1.quantity}"
    )
    print(
        f"\n{product2.name}\n"
        f"{product2.description}\n"
        f"{product2._price}\n"
        f"{product2.quantity}"
    )
    print(
        f"\n{product3.name}\n"
        f"{product3.description}\n"
        f"{product3._price}\n"
        f"{product3.quantity}"
    )


if __name__ == "__main__":
    main()