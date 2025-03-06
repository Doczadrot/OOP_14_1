import unittest

from src.main import Product, Category


class TestProduct(unittest.TestCase):

    def test_product_creation_valid(self):
        """Тест корректного создания продукта с валидными данными"""
        product = Product(
            name="Тестовый продукт",
            description="Тестовое описание",
            price=100.0,
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
            price="100.0",
            quantity=10
        )
        self.assertEqual(product.price, 100.0)

    def test_product_creation_empty_name_empty_string(self):
        """Тест на создание продукта с пустым именем (пустая строка)."""
        with self.assertRaises(ValueError) \
                as context:
            Product(name="",
                    description="Тестовое описание",
                    price=100.0,
                    quantity=10)
        self.assertEqual(
            str(context.exception),
            "Имя товара не может быть пустым"
        )

    def test_product_creation_empty_description_spaces(self):
        """Тест на создание продукта с описанием, состоящим только из """
        "пробелов."
        with self.assertRaises(ValueError) \
                as context:
            Product(
                name="Тестовый продукт",
                description="   ",
                price=100.0,
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
                    price=100.0,
                    quantity=10)
        self.assertEqual(
            str(context.exception),
            "Описание товара не может быть пустым"
        )


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

    def test_category_count_increment(self):
        """Тест подсчета количества категорий"""
        initial_count = Category.category_count
        Category("Ноутбуки", "Портативные компьютеры", [])
        self.assertEqual(Category.category_count, initial_count + 1)

    def test_product_count_calculation(self):
        """Тест подсчета общего количества продуктов"""
        self.assertEqual(Category.product_count, 0)
        self.category.append_product(self.product1)
        self.category.append_product(self.product2)
        Category("Ноутбуки", "Портативные компьютеры", [self.product1])
        self.assertEqual(Category.product_count, 3)

    def test_product_removal(self):
        """Тест уменьшения счётчика при удалении продукта"""
        self.category.append_product(self.product1)
        initial_count = Category.product_count
        self.category.remove_product(self.product1)
        self.assertEqual(Category.product_count, initial_count - 1)


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
