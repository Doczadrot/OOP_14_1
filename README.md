# Проект "Магазин электроники"

## Возможности
- **Учет товаров**
  - Создание карточек товаров с названием, описанием, ценой и количеством
- **Категории товаров**
  - Группировка товаров по категориям (например "Смартфоны" или "Телевизоры")
- **Автоматический подсчет**  
  - Всего категорий: `Category.category_count`  
  - Всего товаров: `Category.product_count`



## Пример использования

### Создание товара
```python
phone = Product("iPhone 15", "512GB, Space Gray", 100000.0, 5)

# Создание категории
smartphones = Category("Смартфоны", "Мобильные устройства", [])
smartphones.append_product(phone)
```

## Установка
```bash
pip install -r requirements.txt
```

## Тестирование
```bash
# Запуск тестов
python -m pytest Tests/


pytest --cov=src --cov-report=html


start htmlcov/index.html
```

## Архитектура
#Класс `Product
- Хранит данные о товаре
- Валидация входных данных

## Класс `Category`
- Управление коллекцией товаров
- Автоматический подсчет статистики

## Отчет о покрытии тестами
После запуска тестов с параметром `--cov-report=html` вы можете просмотреть отчет о покрытии кода тестами, открыв файл `htmlcov/index.html` в браузере.


