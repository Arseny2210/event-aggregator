# Схема базы данных «ИС Мероприятия БГИТУ»

> Чтобы получить PNG-файл для отчёта, скопируй блок `mermaid` и вставь на [mermaid.live](https://mermaid.live) → Export → PNG.

```mermaid
erDiagram
    events {
        uuid id PK "UUID"
        varchar title "Название"
        varchar short_description "Краткое описание"
        varchar description "Полное описание"
        uuid category_id FK "Категория"
        uuid organizer_id FK "Организатор"
        date start_date "Дата начала"
        time start_time "Время начала"
        time end_time "Время окончания"
        varchar location "Место"
        varchar image_url "Картинка"
        varchar registration_url "Ссылка на регистрацию"
        varchar status "draft|published|completed|archived"
        varchar target_audience "Целевая аудитория"
        boolean participation_enabled "Сбор участников"
        timestamp created_at "Создано"
        timestamp updated_at "Обновлено"
    }

    categories {
        uuid id PK "UUID"
        varchar name "Название"
        varchar description "Описание"
    }

    organizers {
        uuid id PK "UUID"
        varchar name "Название"
        varchar description "Описание"
        varchar contact_info "Контакты"
    }

    users {
        uuid id PK "UUID"
        varchar username UK "Логин"
        varchar email UK "Email"
        text password_hash "Хеш пароля"
        int role_id FK "Роль"
        boolean is_active "Активен"
        timestamp last_login "Последний вход"
        timestamp created_at "Создан"
        timestamp updated_at "Обновлён"
    }

    roles {
        int id PK "ID"
        varchar name "Название"
        text description "Описание"
    }

    permissions {
        int id PK "ID"
        varchar name "Название"
        text description "Описание"
    }

    role_permissions {
        int role_id FK "Роль"
        int permission_id FK "Право"
    }

    participations {
        uuid id PK "UUID"
        uuid event_id FK "Мероприятие"
        varchar session_id "Сессия браузера"
        varchar status "registered|confirmed|cancelled"
        timestamp created_at "Создано"
        timestamp updated_at "Обновлено"
    }

    import_jobs {
        uuid id PK "UUID"
        varchar filename "Имя файла"
        varchar status "processing|completed|failed"
        uuid created_by FK "Кто загрузил"
        json summary "Итоги"
        timestamp created_at "Создано"
        timestamp updated_at "Обновлено"
    }

    import_job_row_results {
        uuid id PK "UUID"
        uuid import_job_id FK "Импорт"
        int row_number "№ строки"
        varchar status "imported|warning|failed"
        varchar error_code "Код ошибки"
        text error_message "Текст ошибки"
        uuid event_id FK "Созданное событие"
    }

    notifications {
        uuid id PK "UUID"
        varchar channel "email|telegram|in_app"
        varchar recipient "Получатель"
        varchar template_type "Тип шаблона"
        json payload "Данные"
        varchar status "pending|sent|failed|retrying"
        varchar priority "LOW|NORMAL|HIGH|CRITICAL"
        timestamp sent_at "Отправлено"
        timestamp created_at "Создано"
    }

    notification_templates {
        uuid id PK "UUID"
        varchar template_type "Тип"
        varchar channel "Канал"
        varchar subject "Тема"
        text body "Тело"
        varchar language "Язык"
        int version "Версия"
        boolean is_active "Активен"
    }

    events ||--o{ participations : "участвуют"
    events }o--|| categories : "категория"
    events }o--|| organizers : "организатор"
    users }o--|| roles : "роль"
    roles ||--o{ role_permissions : "права"
    permissions ||--o{ role_permissions : ""
    import_jobs ||--o{ import_job_row_results : "строки"
    import_jobs }o--|| users : "загрузил"
    import_job_row_results }o--|| events : "событие"
```

## Таблицы и связи — описание

### Основные сущности

| Таблица | Назначение | Записей |
|---|---|---|
| `events` | Мероприятия: лекции, хакатоны, конкурсы и т.д. | основная |
| `categories` | Категории: Лекция, Хакатон, Спорт, Конкурс, Карьера, Культура, Другая | 7+ |
| `organizers` | Организаторы мероприятий (кафедры, деканаты) | ~ |
| `participations` | Записи участников (анонимно, по session_id) | ~ |
| `users` | Пользователи админ-панели (админы, редакторы) | ~ |

### Ролевая модель (RBAC)

| Таблица | Назначение |
|---|---|
| `roles` | Роли: `administrator`, `editor` |
| `permissions` | Права: `event:manage`, `import:create`, ... (12 прав) |
| `role_permissions` | Связь M2M: роль ↔ право |

### Импорт

| Таблица | Назначение |
|---|---|
| `import_jobs` | Загруженные Excel-файлы: статус, итоги |
| `import_job_row_results` | Результат обработки каждой строки: успех/ошибка |

### Уведомления

| Таблица | Назначение |
|---|---|
| `notifications` | Отправленные уведомления: email, telegram |
| `notification_templates` | Шаблоны уведомлений (версионируются) |

---

## Связи (диаграмма)

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│  categories  │       │  organizers  │       │    users     │
│  id (PK)     │       │  id (PK)     │       │  id (PK)     │
│  name        │       │  name        │       │  username    │
└──────┬───────┘       └──────┬───────┘       │  email       │
       │ 1:N                  │ 1:N            │  role_id ────┐
       ▼                      ▼                └──────┬───────┘│
┌──────────────────────────────────────┐              │        │
│              events                  │              ▼        │
│  id (PK)                             │       ┌──────┐       │
│  title, description, location        │       │ roles │◄──────┘
│  start_date, start_time, end_time    │       │ id   │
│  category_id (FK) ────────────► cat  │       │ name │
│  organizer_id (FK) ───────────► org  │       └──┬───┘
│  status, participation_enabled       │          │ M2M
└────────────┬─────────────────────────┘          ▼
             │ 1:N                        ┌──────────────┐   ┌─────────────┐
             ▼                            │role_permission│───│ permissions │
┌─────────────────────┐                   │ role_id (FK) │   │  id (PK)    │
│   participations    │                   │ perm_id (FK) │   │  name       │
│  id (PK)            │                   └──────────────┘   └─────────────┘
│  event_id (FK)      │
│  session_id         │       ┌──────────────────┐
│  status             │       │   import_jobs    │       ┌──────────────────────┐
└─────────────────────┘       │  id (PK)         │──1:N─►│ import_job_row_result│
                              │  filename        │       │  id (PK)             │
                              │  status          │       │  import_job_id (FK)  │
                              │  created_by (FK)─┐       │  row_number          │
                              │  summary         │       │  status, error_code  │
                              └──────────────────┘       │  event_id (FK)       │
                                     │                   └──────────────────────┘
                                     │  N:1
                                     ▼
                              ┌──────────────┐
                              │    users     │
                              └──────────────┘
```
