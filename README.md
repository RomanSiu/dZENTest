# Коментарна система на Django + Vue 3

Це повнофункціональний вебзастосунок для створення, відповіді та перегляду коментарів. Застосунок підтримує вкладені відповіді, прикріплення файлів, CAPTCHA, авторизацію за JWT, сортування, пагінацію та асинхронну обробку зображень через Celery і Redis.

---

## 🔧 Використані технології

### Backend:

* Django 4+
* Django REST Framework
* JWT авторизація (`djangorestframework-simplejwt`)
* Celery + Redis
* PostgreSQL
* django-simple-captcha

### Frontend:

* Vue 3 (Composition API)
* Vite
* CSS
* Axios

---

## ⚙️ Основний функціонал

* Реєстрація та авторизація користувачів (JWT)
* Додавання основних та вкладених коментарів
* Валідація форми, CAPTCHA
* Можливість прикріпити:

  * зображення (JPG, PNG, GIF, < 320x240)
  * текстові файли (.txt, < 100 Кб)
* Ієрархічне відображення коментарів з пагінацією (по 25)
* Сортування за ім’ям, email, датою
* Обробка файлів через чергу (Celery)

---

## 📁 Структура репозиторію

```
project/
├── backend/             # Django API
│   ├── accounts/        # додаток аккаунтів
│   ├── comments/        # додаток коментарів
│   └── dZEN/          # налаштування Django
├── frontend/            # Vue 3 застосунок
├── docker-compose.yml  # запуск усіх сервісів
├── .env                # змінні середовища
```

---

## 🚀 Швидкий старт через Docker

### 1. Клонувати репозиторій

```bash
git clone https://github.com/your-repo/comment-app.git
cd comment-app
```

### 2. Створити `.env` файл

```ini
#.env
POSTGRES_DB=commentsdb
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

SECRET_KEY=your_secret_here
DJANGO_ALLOWED_HOSTS=*
```

### 3. Запуск

```bash
docker compose up --build
```

## 🌐 Доступ до сервісів

* Django API: [http://localhost:8000/api/](http://localhost:8000/api/)
* Фронтенд (Vite): [http://localhost:5173](http://localhost:5173)
