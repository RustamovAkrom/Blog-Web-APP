![logo](logo.png)

# ✨ Blog Web App

**Blog Web App** — это современное веб-приложение на **Django**, позволяющее создавать 📝, редактировать ✏️ и просматривать 👀 блог-посты с безопасной аутентификацией через **JWT-токены**.

---

## 🚀 Основные возможности

- 📝 **Создание постов**: авторизированные пользователи могут добавлять и редактировать свои посты.  
- 👥 **Чтение постов**: все пользователи могут просматривать записи.  
- 🔐 **Авторизация через JWT**: безопасная аутентификация с использованием Access и Refresh токенов (Algorithm **RS256**).  

---

## 🛠️ Стек технологий

- **Backend**: Django, Django REST Framework  
- **Аутентификация**: JWT (`djangorestframework-simplejwt`)  
- **База данных**: PostgreSQL (или SQLite для локальной разработки)  
- **Кэширование**: Django Cache (опционально 🚀 для ускорения работы)  

---

## ⚡ Быстрый старт

### 📥 Клонирование репозитория
```bash
git clone https://github.com/RustamovAkrom/Blog-Web-APP.git
cd Blog-Web-APP
```

### 🐍 Настройка виртуального окружения
```bash
python -m venv venv
source venv/bin/activate  # для Linux/macOS
venv\Scripts\activate     # для Windows
```

### 📦 Установка зависимостей
```bash
pip install -r requirements.txt
```

### ⚙️ Настройка переменных окружения
Создайте файл `.env` в корне проекта и укажите настройки:

```bash
SECRET_KEY=<your django secret key>
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_SETTINGS_MODULE=core.settings.development

PRIVATE_KEY_PATH=security_settings/private_key.pem
PUBLIC_KEY_PATH=security_settings/public_key.pem

DATABASE_ENVIRON=sqlite

DATABASE_NAME=<your database name>
DATABASE_USER=<your database user>
DATABASE_PASSWORD=<your database password>
DATABASE_HOST=localhost
DATABASE_PORT=5432

ADMIN_USERNAME=admin
ADMIN_PASSWORD=password
ADMIN_EMAIL=admin@example.com
```

---

## 🔑 Генерация RSA-ключей

JWT с алгоритмом **RS256** требует приватный и публичный ключи.  
👉 Подробная инструкция: [docs/generate-rsa-keys-for-simple-jwt.md](docs/generate-rsa-keys-for-simple-jwt.md)

---

### 📚 Применение миграций и создание суперпользователя
```bash
python manage.py migrate
python manage.py createadmin
```

### ▶️ Запуск сервера
```bash
python manage.py runserver
```

Теперь приложение доступно по адресу:  
👉 `http://127.0.0.1:8000`

---

## 🔐 Аутентификация через JWT

После входа пользователь получает два токена:

- 🔑 **Access Token** — доступ к защищённым маршрутам  
- ♻️ **Refresh Token** — обновление Access Token  

Пример использования:
```http
Authorization: Bearer <access_token>
```

---

## 📂 Структура проекта

- `apps/users` — управление пользователями и аутентификацией  
- `apps/blog` — блог-посты  
- `middleware` — JWT-middleware  
- `settings` — настройки Django, базы данных и кэша  

---

## ⚡ Кэширование

Для ускорения работы Blog App можно использовать кэширование JWT-токенов.

---

## 📜 Лицензия

Проект распространяется по лицензии **MIT License**.

---

## 📖 Документация

Подробная документация доступна здесь:  
👉 [Documentation](https://rustamovakrom.github.io/Blog-Web-APP/)
