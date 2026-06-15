# Farm Products Marketplace System

## Опис проєкту
Система автоматизації онлайн-маркетплейсу для фермерських продуктів. Платформа підтримує реєстрацію користувачів з різними ролями (фермери та покупці), публікацію товарів за категоріями, оформлення замовлень із автоматичним контролем залишків на складах та систему відгуків.

## Технологічний стек
* **Мова програмування:** Python 3.13
* **Веб-фреймворк:** FastAPI (ASGI)
* **База даних:** PostgreSQL / SQLite (для тестів)
* **ORM:** SQLAlchemy 2.0
* **Токени безпеки:** bcrypt, python-jose
* **Тестування:** pytest 9.0

## Базове налаштування проєкту
Ці кроки виконуються один раз для всього циклу розробки.

```bash
git clone https://github.com/ivan-hrytsenko/architecture-labs.git
python -m venv .venv
source venv/bin/activate
pip install -r ./lab1/requirements.txt

```

---

## Етапи розробки (Лабораторні роботи)

### Лабораторна робота №1: CRUD Baseline

Перша ітерація системи, написана у форматі швидкого базового прототипу (анемічна доменна модель, бізнес-логіка розмита між контролерами та статичними сервісами).

#### Структура модулів

* `lab1/src/models/` — ORM моделі SQLAlchemy
* `lab1/src/services/` — Процедурна бізнес-логіка
* `lab1/src/schemas.py` — Схеми валідації Pydantic
* `lab1/src/auth.py` — Перевірка ролей та JWT автентифікація
* `lab1/src/main.py` — Точка входу FastAPI та ендпоінти
* `lab1/tests/` — Інтеграційні тести API

#### Запуск бази даних (Docker)

```bash
docker run --name farm-postgres -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=farm_products -p 5432:5432 -d postgres

```

#### Створення конфігурації

Створіть файл `.env` у папці `lab1/`:

**Варіант А: Локальна SQLite (Швидкий старт без Docker)**
  ```env
  DATABASE_URL=sqlite:///./farm_marketplace.db

  ```

**Варіант Б: PostgreSQL у Docker (Аналог production-середовища)**
  ```env
  DATABASE_URL=postgresql://user:password@localhost:5432/farm_products
  ```

#### Запуск веб-сервера

```bash
uvicorn lab1.src.main:app --reload

```

Документація API (Swagger) після запуску доступна за адресою: `http://127.0.0.1:8000/docs`

#### Запуск тестування

```bash
pytest lab1/tests/

```

### Лабораторна робота №2: Шарова архітектура та доменна модель

Рефакторинг системи із застосуванням принципів Чистої архітектури (Clean Architecture), інверсії залежностей (DIP) та насиченої доменної моделі (Rich Domain Model).

#### Структура модулів

* `lab2/src/domain/` — Ядро системи: насичені сутності, Value Objects, фабрики та інтерфейси репозиторіїв.
* `lab2/src/application/` — Прикладний шар: сценарії використання (Use Cases), що оркеструють виконання операцій.
* `lab2/src/infrastructure/` — Шар інфраструктури: реалізація репозиторіїв через SQLAlchemy, ORM-моделі бази даних та мапери даних.
* `lab2/src/presentation/` — Шар представлення: ендпоінти FastAPI, схеми валідації Pydantic (DTO) та логіка автентифікації.
* `lab2/tests/` — Розділене тестування: ізольовані Unit-тести для домену та Use Cases, а також Integration-тести для API.

#### Налаштування середовища та запуску

Перед виконанням команд переконайтеся, що віртуальне середовище активоване, а термінал знаходиться в корені проєкту.

**Конфігурація шляхів імпорту:**
* Windows (PowerShell): `$env:PYTHONPATH = "lab2"`
* Windows (CMD): `set PYTHONPATH=lab2`
* Linux / macOS: `export PYTHONPATH=lab2`

#### Запуск веб-сервера

```Bash
uvicorn src.presentation.main:app --reload
```

Документація API (Swagger) після запуску доступна за адресою: `http://127.0.0.1:8000/docs`

#### Запуск тестування

```bash
pytest lab2/tests/

```