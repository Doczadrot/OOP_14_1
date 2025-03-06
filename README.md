# Проект "Магазин электроники

## Возможности
- **Учет товаров*
  Создание карточек товаров с названием, описанием, ценой и количеством
- **Категории товаров  
  Группировка товаров по категориям (например "Смартфоны" или "Телевизоры")
- **Автоматический подсчет**  
  - Всего категорий: `Category.category_count`  
  - Всего товаров: `Category.product_count`



## Пример использования

# Создание товара
phone = Product("iPhone 15", "512GB, Space Gray", 100000.0, 5)

# Создание категории
smartphones = Category("Смартфоны", "Мобильные устройства", [])
smartphones.append_product(phone)
```

## Тестирование
```bash
python -m pytest Tests/
```

## Архитектура
### Класс `Product`
- Хранит данные о товаре
- Валидация входных данных

### Класс `Category`
- Управление коллекцией товаров
- Автоматический подсчет статистики


