# 🌴 Thailand Bazar API

Backend-часть платформы для объявлений и услуг в Таиланде. Построена на **Django REST Framework** с использованием **Channels** для чатов и **Celery** для фоновых задач.

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14+-red.svg)](https://www.django-rest-framework.org/)

---

## 🚀 Основные возможности

- **Пользователи**: Регистрация, авторизация (JWT), профили, система верификации.
- **Объявления**: Создание, модерация, категории, поиск и фильтрация.
- **Чат**: Обмен сообщениями в реальном времени (WebSockets).
- **События**: Управление мероприятиями с автоматическим контролем срока истечения.
- **Баннеры и Реклама**: Система управления рекламными материалами.
- **Жалобы**: Система тикетов и модерации контента.

---

## 🛠 Технологический стек

- **Core**: Python 3.10+, Django 4.2+
- **API**: Django REST Framework, SimpleJWT
- **Real-time**: Django Channels
- **Async Tasks**: Celery + Redis
- **Database**: PostgreSQL (Production) / SQLite (Local dev)
- **Storage**: Yandex Cloud (S3 compatible) / Local Media
- **Documentation**: Swagger (drf-yasg)

---

## 📦 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone <repository_url>
cd thailand_bazar
```

### 2. Настройка окружения
Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # Для Linux/macOS
# или
venv\Scripts\activate     # Для Windows

pip install -r requirements.txt
```

### 3. Переменные окружения
Создайте файл `.env` в корне проекта на основе `.env.example`:
```bash
cp .env.example .env
```
Заполните `.env` своими данными (секретный ключ, доступы к БД, SMTP и S3).

### 4. Миграции и база данных
```bash
python manage.py migrate
```

### 5. Создание суперпользователя
```bash
python manage.py createsuperuser
```

### 6. Запуск сервера разработки
```bash
python manage.py runserver
```
API будет доступно по адресу: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## ⚙️ Запуск дополнительных сервисов

### Celery (Фоновые задачи)
```bash
celery -A thailand_bazar worker -l info
```

### Celery Beat (Периодические задачи)
```bash
celery -A thailand_bazar beat -l info
```

### Redis
Убедитесь, что Redis запущен и доступен по адресу, указанному в `settings.py`.

---

## 📖 Документация API
После запуска сервера документация доступна по адресам:
- **Swagger**: `http://127.0.0.1:8000/swagger/`
- **ReDoc**: `http://127.0.0.1:8000/redoc/`

---

## 📁 Структура проекта
- `apps/` — основные приложения (users, announcement, chat и др.)
- `thailand_bazar/` — конфигурация проекта и настройки.
- `media/` — локальное хранилище медиа-файлов.
- `requirements.txt` — список зависимостей.
