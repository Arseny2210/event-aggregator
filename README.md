# ИС «Мероприятия БГИТУ»

Единая информационная витрина мероприятий БГИТУ — лекции, хакатоны, конкурсы, спортивные события. Позволяет студентам, преподавателям и руководству видеть полную картину событий вуза в одном месте.

<p align="center">
  <img src="https://img.shields.io/badge/Next.js-15-black?logo=next.js" alt="Next.js" />
  <img src="https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/PostgreSQL-16-336791?logo=postgresql" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Tailwind_CSS-4-06B6D4?logo=tailwindcss" alt="Tailwind" />
  <img src="https://img.shields.io/badge/Docker-✓-2496ED?logo=docker" alt="Docker" />
</p>

---

## Возможности

### Для зрителей (публичный портал)
- **Таймлайн** — хронологическая лента событий с группировкой по дням («Сегодня», «Завтра»)
- **Календарь** — месячная сетка с цветными маркерами категорий и подсветкой загруженных дней (3+ события)
- **Поиск** — по названию, описанию и месту проведения (без учёта регистра)
- **Фильтр по категориям** — 7 категорий: Лекция, Хакатон, Спорт, Конкурс, Карьера, Культура, Другая
- **Кнопка «Записаться»** — анонимный счётчик участников с возможностью отмены

### Для администратора (админ-панель)
- **CRUD мероприятий** — создание, редактирование, удаление
- **Массовый импорт из Excel** — шаблон с инструкцией в `backend/import_example.xlsx`
- **Массовые действия** — выбрать несколько событий и опубликовать/отправить в черновик
- **Загрузка изображений** — drag & drop с предпросмотром
- **Кастомные категории** — создание новых категорий на лету при заполнении формы
- **История импортов** — прогресс обработки, статус каждой строки
- **Черновик формы** — автосохранение в localStorage при перезагрузке страницы

---

## Технологический стек

| Слой | Технология |
|---|---|
| **Frontend** | Next.js 15, React 19, TypeScript, Tailwind CSS 4, Framer Motion |
| **Backend** | FastAPI, SQLAlchemy 2 (async), Pydantic v2, Alembic |
| **База данных** | PostgreSQL 16 |
| **Кеш** | Redis 7 |
| **State management** | React Hook Form + Zod, TanStack Query |
| **Деплой** | Docker Compose, Nginx |

---

## Структура проекта

```
event-aggregator/
├── frontend/                    # Next.js приложение
│   ├── src/
│   │   ├── app/                 # App Router: страницы и лейауты
│   │   ├── components/          # UI и feature-компоненты
│   │   │   ├── features/        # Бизнес-компоненты (events, public, imports, dashboard)
│   │   │   ├── layout/          # Header, Footer, Sidebar, EmptyState
│   │   │   └── ui/              # Атомарные компоненты (Button, Input, Select, etc.)
│   │   ├── lib/
│   │   │   ├── api/             # API-клиенты
│   │   │   ├── hooks/           # React Query хуки
│   │   │   └── utils/           # Валидация (Zod), утилиты
│   │   └── types/               # TypeScript-типы
│   ├── next.config.ts
│   └── package.json
│
├── backend/                     # FastAPI приложение
│   ├── app/
│   │   ├── api/v1/endpoints/    # REST эндпоинты
│   │   ├── models/              # SQLAlchemy модели
│   │   ├── schemas/             # Pydantic DTO
│   │   ├── services/            # Бизнес-логика
│   │   ├── repositories/        # Доступ к данным
│   │   ├── middleware/          # CORS, etc.
│   │   └── core/                # Конфигурация, константы
│   ├── tests/                   # Pytest тесты
│   ├── pyproject.toml
│   └── entrypoint.sh
│
├── docker/                      # Docker и деплой
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   ├── docker-compose.yml       # Локальная разработка
│   ├── docker-compose.override.yml
│   ├── docker-compose.prod.yml  # Продакшн
│   ├── nginx/                   # Nginx конфиги
│   └── .env.prod.example        # Шаблон переменных окружения
│
├── docs/                        # Документация
├── reference/                   # API-референсы, схема БД
└── scripts/                     # Вспомогательные скрипты
```

---

## Быстрый старт

### Локальная разработка

**Требования:** Python 3.12+, Node.js 22+, PostgreSQL 16+, Redis 7.

```bash
# 1. Бэкенд
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e .
cp .env.example .env   # Заполни DATABASE_URL и REDIS_URL
alembic upgrade head
python seed_admin.py    # Создать админа (admin / admin123)
uvicorn app.main:app --reload --port 8001

# 2. Фронтенд
cd frontend
cp .env.example .env.local
npm install
npm run dev             # http://localhost:3000
```

### Docker (одной командой)

```bash
cp docker/.env.prod.example docker/.env.prod   # Заполни переменные
docker compose -f docker/docker-compose.yml up -d
# Приложение доступно на http://localhost:80
```

### Продакшн

```bash
cp docker/.env.prod.example docker/.env.prod   # Замени <secure-password> и <your-domain>
docker compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml up -d
```

---

## Переменные окружения

### Бэкенд

| Переменная | Назначение | По умолчанию |
|---|---|---|
| `DATABASE_URL` | Строка подключения к PostgreSQL | `postgresql+asyncpg://postgres:postgres@localhost:5432/event_aggregator` |
| `REDIS_URL` | Строка подключения к Redis | `redis://localhost:6379/0` |
| `SECRET_KEY` | Ключ для JWT-токенов | *обязательно заменить в продакшене* |
| `CORS_ORIGINS` | Разрешённые домены (через запятую) | `http://localhost:3000` |
| `ENVIRONMENT` | `development` / `production` | `development` |
| `DEFAULT_IMPORT_CATEGORY_ID` | UUID категории по умолчанию для импорта | `""` |
| `UPLOAD_DIR` | Директория для загруженных изображений | `uploads/` |

### Фронтенд

| Переменная | Назначение | По умолчанию |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | URL бэкенд-API | `http://localhost:8000/api/v1` |

---

## API

API доступно по адресу `/api/v1/`. Документация Swagger — `/docs`.

### Основные эндпоинты

| Метод | Путь | Назначение |
|---|---|---|
| `GET` | `/events/` | Список событий с фильтрацией и поиском |
| `POST` | `/events/` | Создать событие |
| `PATCH` | `/events/{id}` | Обновить событие |
| `DELETE` | `/events/{id}` | Удалить событие |
| `POST` | `/events/batch-status` | Массовое изменение статуса |
| `GET` | `/categories/` | Список категорий |
| `POST` | `/categories/` | Создать категорию |
| `POST` | `/upload/image` | Загрузить изображение |
| `POST` | `/imports/` | Загрузить Excel-файл |
| `GET` | `/events/{id}/participate` | Статус участия пользователя |
| `POST` | `/events/{id}/participate` | Записаться на мероприятие |
| `DELETE` | `/events/{id}/participate` | Отменить участие |

---

## Excel-импорт

Файл `backend/import_example.xlsx` содержит готовый шаблон с двумя вкладками:

- **Мероприятия** — примеры строк с 7 категориями
- **Инструкция** — правила заполнения и UUID категорий

### Обязательные столбцы
`title`, `description`, `start_date` (ГГГГ-ММ-ДД), `location`, `organizer_name`

### Необязательные столбцы
`short_description`, `start_time`, `end_time`, `category_id`, `image_url`, `registration_url`

---

## Команды

```bash
# Бэкенд
cd backend && ruff check app/     # Линтинг
cd backend && pytest                # Тесты (требуется TEST_DATABASE_URL)

# Фронтенд
cd frontend && npm run lint         # ESLint
cd frontend && npm run typecheck    # TypeScript
cd frontend && npm run build        # Production-сборка
```

---

## Роли

| Роль | Права |
|---|---|
| **Зритель** | Просмотр таймлайна/календаря, запись на мероприятия (анонимно) |
| **Редактор (editor)** | Создание, редактирование, удаление мероприятий, импорт Excel, управление участием |
| **Администратор** | То же + управление пользователями и правами редакторов |

Данные для входа по умолчанию: `admin` / `admin123` (создаётся через `python seed_admin.py`).

---

## Чек-лист деплоя на сервер

Перед деплоем на продакшн-сервер выполни следующие замены:

### 1. Создать `.env.prod`

```bash
cp docker/.env.prod.example docker/.env.prod
```

Заменить в `docker/.env.prod`:

| Найти | Заменить на |
|---|---|
| `<secure-password>` | Сложный пароль для PostgreSQL (минимум 16 символов) |
| `<random-secret-at-least-32-chars>` | Случайный ключ (сгенерировать: `openssl rand -hex 32`) |
| `<your-domain>` | Реальный домен (например, `events.bgitu.ru`) |

### 2. Заменить дефолтные credentials админа

В `backend/seed_admin.py` заменить `admin123` на сложный пароль:

```python
password="<сгенерированный-пароль-админа>"
```

### 3. Обновить `CORS_ORIGINS`

В `docker/.env.prod`:
```
CORS_ORIGINS=https://events.bgitu.ru
```

### 4. Обновить `NEXT_PUBLIC_API_URL`

В `docker/.env.prod`:
```
NEXT_PUBLIC_API_URL=https://events.bgitu.ru/api/v1
```

### 5. Отключить документацию в проде

В `docker/.env.prod` добавить:
```
ENVIRONMENT=production
```
Swagger (`/docs`) и ReDoc (`/redoc`) автоматически отключаются nginx в проде.

### 6. Настроить SSL (Let's Encrypt)

Установить certbot и получить сертификаты:
```bash
docker compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml up -d nginx
certbot certonly --webroot -w /var/www/certbot -d events.bgitu.ru
```

Скопировать сертификаты:
```bash
cp /etc/letsencrypt/live/events.bgitu.ru/fullchain.pem docker/nginx/certs/
cp /etc/letsencrypt/live/events.bgitu.ru/privkey.pem docker/nginx/certs/
```

### 7. Бэкапы БД

Настроить cron для ежедневного дампа:
```bash
0 3 * * * docker exec event-aggregator-postgres-1 pg_dump -U postgres event_aggregator > /backups/ea_$(date +\%Y\%m\%d).sql
```

### 8. Запустить

```bash
docker compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml up -d --build
docker compose -f docker/docker-compose.yml -f docker/docker-compose.prod.yml exec backend python seed_admin.py
```

### 9. Проверить

- [ ] `https://events.bgitu.ru` — главная страница
- [ ] `https://events.bgitu.ru/login` — вход (`admin` / новый пароль)
- [ ] `https://events.bgitu.ru/dashboard` — админ-панель
- [ ] Создать тестовое мероприятие, проверить отображение на главной
- [ ] Загрузить изображение — проверить отображение
- [ ] Импортировать Excel — проверить обработку
- [ ] SSL сертификат действителен
- [ ] Бэкапы настроены
