class Product:
    """Класс, представляющий товар."""

    def __init__(self, name: str, description: str,
                 price: float, quantity: int):
        try:
            price = float(price)
        except ValueError as e:
            raise ValueError(
                f"Не удалось преобразовать строку в float: '{price}'") from e

        if price <= 0:
            raise ValueError("Цена должна быть положительной")
        if quantity < 0:
            raise ValueError("Количество не может быть отрицательным")
        if not name.strip():
            raise ValueError("Имя товара не может быть пустым")
        if not description.strip():
            raise ValueError("Описание товара не может быть пустым")

        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс, представляющий категорию товаров."""
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str, products: list[Product]):
        Category.category_count += 1
        Category.product_count += len(products)
        self.name = name
        self.description = description
        self.products = products

    def append_product(self, product):
        self.products.append(product)
        Category.product_count += 1

    def remove_product(self, product):
        if product not in self.products:
            raise ValueError("Продукт не найден в категории")
        self.products.remove(product)
        Category.product_count -= 1


def main():

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
    smartphones.append_product(product1)
    smartphones.append_product(product2)

    notebooks = Category("Ноутбуки", "Портативные компьютеры", [])
    notebooks.append_product(product3)


    print(
        f"{product1.name}\n"
        f"{product1.description}\n"
        f"{product1.price}\n"
        f"{product1.quantity}"
    )
    print(
        f"\n{product2.name}\n"
        f"{product2.description}\n"
        f"{product2.price}\n"
        f"{product2.quantity}"
    )
    print(
        f"\n{product3.name}\n"
        f"{product3.description}\n"
        f"{product3.price}\n"
        f"{product3.quantity}"
    )


if __name__ == "__main__":
    main()
