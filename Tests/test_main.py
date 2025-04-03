import unittest
from itertools import product
from unittest.mock import patch
import io
import sys
import contextlib

from src.main import Product, Category, Smartphone, LawnGrass, BaseProduct, CreateLogMixin
from io import StringIO
from abc import ABC, abstractmethod


class TestProduct(unittest.TestCase):

    def test_product_creation_valid(self):
        """Тест корректного создания продукта с валидными данными"""
        product = Product(
            name="Тестовый продукт",
            description="Тестовое описание",
            price_=100.0,
            quantity=10
        )
        self.assertEqual(product.name, "Тестовый продукт")
        self.assertEqual(product.description, "Тестовое описание")
        self.assertEqual(product.price, 100.0)
        self.assertEqual(product.quantity, 10)

    def test_product_creation_valid_price_as_string(self):
        """Тест на корректное создание продукта, когда цена задана строкой."""
        product = Product(
            name="Тестовый продукт",
            description="Тестовое описание",
            price_="100.0",
            quantity=10
        )
        self.assertEqual(product.price, 100.0)

    def test_product_creation_logs(self):
        with contextlib.redirect_stdout(StringIO()) as captured_output:
            test_product = Product("Тестовый продукт", "Описание для теста", 100.0, 5)
        output = captured_output.getvalue()
        self.assertIn("Создан объект класса: Product", output)
        self.assertIn("Переданные аргументы: args=('Тестовый продукт', 'Описание для теста', 100.0, 5), kwargs={}",
                      output)

    def test_product_creation_empty_name_empty_string(self):
        """Тест на создание продукта с пустым именем (пустая строка)."""
        with self.assertRaises(ValueError) \
                as context:
            Product(name="",
                    description="Тестовое описание",
                    price_=100.0,
                    quantity=10)
        self.assertEqual(
            str(context.exception),
            "Имя товара не может быть пустым"
        )
    
    def test_product_str(self):
        product = Product("Тестовый продукт", "Тестовое описание", 100.1, 10)
        product_str = str(product)
        expected_str = "Тестовый продукт, 100.1 руб. Остаток: 10 шт."
        self.assertEqual(product_str, expected_str)
        
    def test_product_add(self):
        """Тест магического метода __add__ для сложения стоимостей товаров"""
        product1 = Product("Товар 1", "Описание 1", 100.0, 2)
        product2 = Product("Товар 2", "Описание 2", 200.0, 3)
        total_price = product1 + product2
        expected_price = (100.0 * 2) + (200.0 * 3)  # 800.0
        self.assertEqual(total_price, expected_price)


    def test_product_creation_empty_description_spaces(self):
        """Тест на создание продукта с описанием, состоящим только из """
        "пробелов."
        with self.assertRaises(ValueError) \
                as context:
            Product(
                name="Тестовый продукт",
                description="   ",
                price_=100.0,
                quantity=10
            )
        self.assertEqual(
            str(context.exception),
            "Описание товара не может быть пустым"
        )

    def test_product_creation_empty_description_empty_string(self):
        """Тест на создание продукта с пустым описанием (пустая строка)."""
        with self.assertRaises(ValueError) \
                as context:
            Product(name="Тестовый продукт",
                    description="",
                    price_=100.0,
                    quantity=10)
        self.assertEqual(
            str(context.exception),
            "Описание товара не может быть пустым"
        )
        
    def test_product_creation_zero_quantity(self):
        """Тест на создание продукта с нулевым количеством."""
        with self.assertRaises(ValueError) as context:
            Product(name="Тестовый продукт",
                    description="Тестовое описание",
                    price_=100.0,
                    quantity=0)
        self.assertEqual(
            str(context.exception),
            "Товар с нулевым количеством не может быть добавлен"
        )

    def test_new_product_valid_data(self):
        """Тест создания продукта с валидными данными через new_product"""
        product_data = {
            'name': 'MacBook Pro',
            'description': '16-inch, 32GB RAM, 1TB SSD',
            'price': '250000.0',
            'quantity': 10
        }
        product = Product.new_product(product_data)
        self.assertEqual(product.name, 'MacBook Pro')
        self.assertEqual(product.description, '16-inch, 32GB RAM, 1TB SSD')
        self.assertEqual(product.price, 250000.0)
        self.assertEqual(product.quantity, 10)

    def test_new_product_missing_name(self):
        """Тест создания продукта с отсутствующим именем через new_product"""
        product_data = {
            'description': '16-inch, 32GB RAM, 1TB SSD',
            'price': '250000.0',
            'quantity': 10
        }
        with self.assertRaises(ValueError) as context:
            Product.new_product(product_data)
        self.assertEqual(str(context.exception), "Имя товара не может быть пустым")

    def test_new_product_invalid_price(self):
        """Тест создания продукта с некорректной ценой через new_product"""
        product_data = {
            'name': 'MacBook Pro',
            'description': '16-inch, 32GB RAM, 1TB SSD',
            'price': '-250000.0',
            'quantity': 10
        }
        with self.assertRaises(ValueError) as context:
            Product.new_product(product_data)
        self.assertEqual(str(context.exception), "Цена должна быть положительной")

    def test_new_product_missing_description(self):
        """Тест создания продукта с отсутствующим описанием через new_product"""
        product_data = {
            'name': 'MacBook Pro',
            'price': '250000.0',
            'quantity': 10
        }
        with self.assertRaises(ValueError) as context:
            Product.new_product(product_data)
        self.assertEqual(str(context.exception), "Описание товара не может быть пустым")


class TestCategory(unittest.TestCase):

    def setUp(self):
        Category.category_count = 0
        Category.product_count = 0
        self.category = Category(
            "Смартфоны",
            "Мобильные устройства",
            products=[])
        self.product1 = Product(
            "Iphone 15",
            "512GB, Gray space",
            210000.0,
            8
        )
        self.product2 = Product(
            "Xiaomi Redmi Note 11",
            "1024GB, Синий",
            31000.0,
            15
        )

    def test_category_product_getter(self):
        category = Category("Тестовая категория", "Тестовое описание", products=[])
        product1 = Product("Тест продукт1", "Описание1", 100, 5)
        product2 = Product("Тест продукт2", "Описание2", 200, 10)

        category.add_product(product1)
        category.add_product(product2)

        products_string = category.products
        expected_string = f'{product1.name}, {product1.price} руб. Остаток: {product1.quantity} шт.\n' \
                          f'{product2.name}, {product2.price} руб. Остаток: {product2.quantity} шт.'
        self.assertEqual(products_string.strip(), expected_string.strip())
        
    def test_category_average_price(self):
        """Тест метода average_price с товарами."""
        product1 = Product("Товар1", "Описание1", 100, 5)
        product2 = Product("Товар2", "Описание2", 200, 10)
        category = Category("Тестовая категория", "Тестовое описание", [product1, product2])
        self.assertEqual(category.average_price(), 150.0)
        
    def test_category_average_price_empty(self):
        """Тест метода average_price с пустой категорией."""
        category = Category("Пустая категория", "Тестовое описание", [])
        self.assertEqual(category.average_price(), 0)


    def test_category_count_increment(self):
        """Тест подсчета количества категорий"""
        initial_count = Category.category_count
        Category("Ноутбуки", "Портативные компьютеры", [])
        self.assertEqual(Category.category_count, initial_count + 1)

    def test_add_positive_price_and_quantity(self):
        product1 = Product("Товар1", "описание",100 , 50)
        product2 = Product("Товар2", "описание", 200, 100)
        expentet_total = (100 * 50) + (200 * 100)
        actual_total = product1 + product2
        self.assertEqual(expentet_total, actual_total)

    def test_add_zero_quantity(self):
        # Проверяем, что создание продукта с нулевым количеством вызывает исключение
        with self.assertRaises(ValueError) as context:
            product1 = Product("Товар1", "описание", 2, 0)
        self.assertEqual(str(context.exception), "Товар с нулевым количеством не может быть добавлен")

    def test_add_little_quantity(self):
        product1 = Product("Товар1", "описание",2 , 1)
        product2 = Product("Товар2", "описание", 3, 2)
        expentet_total = (2 * 1) + (3 * 2)
        actual_total = product1 + product2
        self.assertEqual(expentet_total, actual_total)

    def test_add_little_price(self):
        product1 = Product("Товар1", "описание", 00.2, 1)
        product2 = Product("Товар2", "описание", 00.3, 2)
        expentet_total = (00.2 * 1) + (00.3 * 2)
        actual_total = product1 + product2
        self.assertEqual(expentet_total, actual_total)



    def test_product_count_calculation(self):
        """Тест подсчета общего количества продуктов"""
        self.assertEqual(Category.product_count, 0)
        self.category.add_product(self.product1)
        self.category.add_product(self.product2)
        Category("Ноутбуки", "Портативные компьютеры", [self.product1])
        self.assertEqual(Category.product_count, 3)

    def test_product_removal(self):
        """Тест уменьшения счётчика при удалении продукта"""
        self.category.add_product(self.product1)
        initial_count = Category.product_count
        self.category.remove_product(self.product1)
        self.assertEqual(len(self.category._Category__products), 0)
        self.assertEqual(Category.product_count, initial_count - 1)
        
    def test_private_products_encapsulation(self):
        """Проверка невозможности прямого доступа к списку продуктов"""
        with self.assertRaises(AttributeError):
            _ = self.category.__products

    def test_products_list_format(self):
        """Проверка формата списка продуктов"""
        self.category.add_product(self.product1)
        expected = "Iphone 15, 210000.0 руб. Остаток: 8 шт."
        self.assertEqual(self.category.products.strip(), expected)


class TestMainExecution(unittest.TestCase):

    def test_main_output(self):
        """Тестирование вывода выполнения командной строки"""
        from src.main import main
        import io
        import sys

        captured_output = io.StringIO()
        sys.stdout = captured_output
        main()
        sys.stdout = sys.__stdout__

        output = captured_output.getvalue()

        self.assertIn('Samsung Galaxy S23 Ultra', output)
        self.assertIn('256GB, Серый цвет, 200MP камера', output)
        self.assertIn('180000.0', output)
        self.assertIn('5', output)

        self.assertIn('Iphone 15', output)
        self.assertIn('512GB, Gray space', output)
        self.assertIn('210000.0', output)

        self.assertIn('Xiaomi Redmi Note 11', output)
        self.assertIn('1024GB, Синий', output)
        self.assertIn('31000.0', output)

    def test_price_setter_valid_value(self):
        """Проверка установки корректной цены"""
        product = Product("Тест", "Тест", 100.0, 5)
        product.price = 200.0
        self.assertEqual(product.price, 200.0)

    def test_price_setter_invalid_values(self):
        """Проверка реакции на невалидные значения цены"""
        product = Product("Тест", "Тест", 100.0, 5)
        
        # Тест нулевой цены
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            product.price = 0
            self.assertEqual(product.price, 100.0)
            self.assertIn("Цена не должна быть нулевая или отрицательная", buf.getvalue())

        # Тест отрицательной цены
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            product.price = -50
            self.assertEqual(product.price, 100.0)
            self.assertIn("Цена не должна быть нулевая или отрицательная", buf.getvalue())

    def test_price_setter_negative_value(self):
        """Тест сеттера цены с отрицательным значением"""
        product = Product(
            name="Test Product",
            description="Test Description",
            price_=100.0,
            quantity=10
        )
        with patch('sys.stdout', new=StringIO()) as fake_out:
            product.price = -50.0
            self.assertIn("Цена не должна быть нулевая или отрицательная", fake_out.getvalue().strip())
        self.assertEqual(product.price, 100.0)
class TestInheritedClasses(unittest.TestCase):
    def setUp(self):
        self.product1 = Product(
            "Iphone 15",
            "512GB, Gray space",
            210000.0,
            8
        )
        self.category = Category(
            "Смартфоны",
            "Мобильные устройства",
            products=[]
        )
    def test_smartphone_creation(self):
        smartphone = Smartphone(
            name="Test Phone",
            description="A test smartphone",
            price_=500.0,
            quantity=5,
            efficiency="High",
            model="TestModel",
            memory="64GB",
            color="Black"
        )
        self.assertIsNotNone(smartphone)
        # Проверка, что Smartphone является наследником Product
        self.assertTrue(issubclass(Smartphone, Product))
        # Проверка атрибутов Smartphone
        self.assertEqual(smartphone.name, "Test Phone")
        self.assertEqual(smartphone.description, "A test smartphone")
        self.assertEqual(smartphone.price, 500.0)
        self.assertEqual(smartphone.quantity, 5)
        self.assertEqual(smartphone.efficiency, "High")
        self.assertEqual(smartphone.model, "TestModel")
        self.assertEqual(smartphone.memory, "64GB")
        self.assertEqual(smartphone.color, "Black")
        # Проверка метода calculate_total_value
        self.assertEqual(smartphone.calculate_total_value(), 500.0 * 5)

    def test_lawn_grass_creation(self):
        """Тест создания и проверки объекта класса LawnGrass"""
        lawn_grass = LawnGrass(
            name="Premium Grass",
            description="Высококачественная газонная трава",
            price_=1500.0,
            quantity=10,
            country="Россия",
            germination_period=14,
            color="Зеленый"
        )
        self.assertIsNotNone(lawn_grass)
        # Проверка, что LawnGrass является наследником Product
        self.assertTrue(issubclass(LawnGrass, Product))
        # Проверка атрибутов LawnGrass
        self.assertEqual(lawn_grass.name, "Premium Grass")
        self.assertEqual(lawn_grass.description, "Высококачественная газонная трава")
        self.assertEqual(lawn_grass.price, 1500.0)
        self.assertEqual(lawn_grass.quantity, 10)
        self.assertEqual(lawn_grass.country, "Россия")
        self.assertEqual(lawn_grass.germination_period, 14)
        self.assertEqual(lawn_grass.color, "Зеленый")
        # Проверка метода calculate_total_value
        self.assertEqual(lawn_grass.calculate_total_value(), 1500.0 * 10)

    def test_mixin_logging(self):
        with patch('sys.stdout', new=io.StringIO()) as fake_out:
            product = Product("Test", "Desc", 100, 5)
            self.assertIn("Создан объект класса: Product", fake_out.getvalue())
            self.assertIn("Переданные аргументы: args=('Test', 'Desc', 100, 5), kwargs={}", fake_out.getvalue())

    def test_category_str_output(self):
        cat = Category("Test", "Desc", [self.product1])
        output = str(cat)
        self.assertIn("Категория: Test", output)
        self.assertIn("Iphone 15, 210000.0 руб. Остаток: 8 шт.", output)





