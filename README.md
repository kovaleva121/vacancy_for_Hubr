# Тестовое задание

REST API для управления кошельком, реализованное на Django и Django REST Framework. Система предоставляет функционал для
управления кошельком и транзакциями.

## 🚀 Функциональность

## Основная часть (обязательная по ТЗ):

#### ✅ Контроллер для просмотра детальной информации кошелька

#### ✅ Контроллер для создания транзакций

#### ✅ Контроллеры описаны через generic классы

#### ✅ Описаны сериализаторы для каждой модели

#### ✅ Реализована сборка и установка образов через Docker-compose

## Технологический стек

#### Backend: Django 4.2 + Django REST Framework

#### База данных: PostgreSQL

#### Контейнеризация: Docker + Docker Compose

## 📂 Установка и запуск

Клонировать репозиторий:

```
 git clone https://github.com/yourname/vacancy_for_Hubr.git`

```

Создать и активировать виртуальное окружение:

```
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

Создать файл .env на основе .env.example:

```
cp .env.example .env
```

Запустить сервисы:

```
docker-compose up -d --build
```

Создать суперпользователя:

```
docker-compose exec web python manage.py createsuperuser
```




