# Biomirix Lucky Wheel

Telegram Mini App для проведения розыгрыша призов в формате колеса удачи. Пользователь запускает бота, подтверждает подписку на Telegram-канал и открывает колесо. После вращения приложение выбирает доступный приз и отправляет результат пользователю в Telegram.

Проект включает веб-интерфейс колеса, Telegram-бота, API, административную панель, PostgreSQL и Caddy. Все компоненты запускаются одной командой через Docker Compose.

## Возможности

- проверка подписки пользователя на Telegram-канал;
- запуск колеса внутри Telegram Mini App;
- проверка подлинности Telegram `initData` на сервере;
- ограничение до одного розыгрыша на пользователя;
- случайный выбор только среди активных призов с доступным остатком;
- защита от повторной выдачи при одновременных запросах;
- отправка выигранного приза пользователю через Telegram-бота;
- управление призами, остатками, пользователями и настройками через админ-панель;
- автоматическое применение миграций базы данных;
- автоматическое получение и обновление HTTPS-сертификатов через Caddy;
- healthcheck для основных сервисов.

## Как работает приложение

1. Пользователь отправляет боту команду `/start`.
2. Бот проверяет подписку пользователя на заданный Telegram-канал.
3. Подписанный пользователь получает кнопку запуска Mini App.
4. Mini App обращается к API с данными авторизации Telegram.
5. API проверяет пользователя, наличие предыдущего вращения и остатки призов.
6. После вращения API фиксирует выигрыш в PostgreSQL и уменьшает количество приза.
7. Бот отправляет пользователю сообщение с результатом.

## Архитектура

| Компонент | Назначение |
| --- | --- |
| `caddy` | Раздает Mini App, принимает HTTP/HTTPS-трафик и проксирует запросы |
| `client` | Telegram-бот на Aiogram и endpoint для webhook |
| `server` | FastAPI API и административная панель SQLAdmin |
| `migrations` | Применяет миграции Alembic перед запуском API |
| `db` | PostgreSQL 16 для пользователей, призов, розыгрышей и настроек |

Внешние порты публикует только Caddy. PostgreSQL, API и webhook-сервис доступны внутри Docker-сети и не открываются напрямую в интернет.

## Технологии

- Python 3.14;
- FastAPI и Uvicorn;
- Aiogram;
- SQLAlchemy и Alembic;
- PostgreSQL 16;
- SQLAdmin;
- Caddy;
- Docker Compose;
- HTML, CSS и JavaScript для Mini App.

## Структура проекта

```text
.
├── caddy/
│   ├── Caddyfile          # маршрутизация, HTTPS и reverse proxy
│   └── static/            # интерфейс Telegram Mini App
├── client/
│   ├── src/               # Telegram-бот и webhook
│   ├── Dockerfile
│   └── requirements.txt
├── server/
│   ├── alembic/           # миграции базы данных
│   ├── src/               # API, бизнес-логика и админ-панель
│   ├── Dockerfile
│   └── requirements.txt
├── .env.example           # шаблон переменных окружения
├── docker-compose.yaml    # запуск всех сервисов
└── DEPLOYMENT.md          # подробная инструкция для production
```

## Требования

Для запуска через Docker нужны:

- Docker Engine;
- Docker Compose v2;
- Telegram-бот, созданный через `@BotFather`;
- Telegram-канал, в котором бот имеет права администратора.

Для production дополнительно нужны домен, публичный сервер и открытые порты `80` и `443`.

## Переменные окружения

В проекте используется один файл `.env` в корневом каталоге.

Пример создания файла .env из шаблона:

```bash
cp .env.example .env
```

Основные переменные:

| Переменная | Описание |
| --- | --- |
| `APP_DOMAIN` | Адрес, который обслуживает Caddy |
| `HTTP_PORT` | Внешний HTTP-порт |
| `HTTPS_PORT` | Внешний HTTPS-порт |
| `ACME_EMAIL` | Email для выпуска TLS-сертификата |
| `BASE_URL` | Публичный URL Mini App и webhook без завершающего `/` |
| `BACKEND_API_URL` | Адрес API, доступный контейнеру Telegram-бота |
| `UPSTREAM_FORWARDED_PROTO` | Протокол, передаваемый API через reverse proxy |
| `BOT_TOKEN` | Токен Telegram-бота |
| `TELEGRAM_CHANNEL_ID` | Числовой ID проверяемого канала |
| `TELEGRAM_CHANNEL_URL` | Ссылка на канал для кнопки подписки |
| `TELEGRAM_INIT_DATA_MAX_AGE_SECONDS` | Допустимый возраст данных авторизации Telegram |
| `POSTGRES_*` | Настройки PostgreSQL |
| `ADMIN_TITLE` | Заголовок административной панели |
| `ADMIN_SECRET_KEY` | Секрет для сессий административной панели |

Файл `.env` содержит секреты и исключен из Git. В репозиторий следует добавлять только `.env.example` без настоящих токенов и паролей.

## Локальный запуск

Для обычного локального запуска достаточно указать в `.env`:

```dotenv
APP_DOMAIN=:80
HTTP_PORT=8080
HTTPS_PORT=8443
BASE_URL=http://localhost:8080
BACKEND_API_URL=http://server:8000/api/v1
UPSTREAM_FORWARDED_PROTO=http
POSTGRES_HOST=db
```

А также остальные обязательные значения по примеру из `.env.example`, затем запустите проект:

```bash
docker compose config --quiet
docker compose up -d --build
docker compose ps -a
```

После запуска доступны:

- Mini App: `http://localhost:8080`;
- API healthcheck: `http://localhost:8080/api/v1/health`;
- админ-панель: `http://localhost:8080/admin/login`.

Telegram принимает webhook и открывает Mini App только по публичному HTTPS-адресу. Для проверки через ngrok:

```bash
ngrok http 8080
```

Полученный адрес в `.env`:

```dotenv
BASE_URL=https://example.ngrok-free.app
UPSTREAM_FORWARDED_PROTO=https
```

Пересоздание сервисов, которые используют эти значения:

```bash
docker compose up -d --force-recreate server client caddy
```

## Первый запуск

Миграции выполняются автоматически сервисом `migrations`. Его состояние `Exited (0)` после запуска означает успешное завершение.

Создание администратора:

```bash
docker compose run --rm server python -m src.cli create-admin --username admin
```

Команда предложит дважды ввести пароль. После этого возможен вход в админ-панель по адресу `/admin/login`.

## Основные команды

Запуск или обновление контейнеров:

```bash
docker compose up -d --build
```

Просмотр состояния:

```bash
docker compose ps -a
```

Просмотр общих логов:

```bash
docker compose logs -f --tail=200
```

Просмотр логов конкретного сервиса:

```bash
docker compose logs -f --tail=200 server
docker compose logs -f --tail=200 client
docker compose logs -f --tail=200 caddy
```

Остановка проекта с сохранением данных:

```bash
docker compose down
```

Удаление проекта командой `docker compose down -v` также удалит том PostgreSQL с данными и том Caddy с сертификатами.

## Проверка работоспособности

Проверка API:

```bash
curl --fail --show-error http://localhost:8080/api/v1/health
```

Ожидаемый ответ:

```json
{"status":"ok"}
```

Для проверки полного Telegram-сценария:

1. Убедитесь, что бот добавлен администратором в канал.
2. Запустите сервисы с публичным HTTPS-адресом в `BASE_URL`.
3. Отправьте боту `/start`.
4. Проверьте подписку и открытие колеса.
5. Выполните вращение и проверьте сообщение с выигрышем.
6. Убедитесь, что повторное вращение для этого пользователя недоступно.

## Production-развертывание

На production-сервере Caddy самостоятельно получает и продлевает HTTPS-сертификат. Для этого домен должен указывать на сервер, а порты `80` и `443` должны быть доступны из интернета.

Полная пошаговая инструкция, включая настройку DNS, firewall, `.env`, резервное копирование, обновление и диагностику, находится в [DEPLOYMENT.md](DEPLOYMENT.md).

## Данные и постоянные тома

Docker Compose создает постоянные тома:

- `postgres_data` хранит базу данных;
- `caddy_data` хранит сертификаты и служебные данные Caddy;
- `caddy_config` хранит конфигурационное состояние Caddy.

Обычный перезапуск или пересоздание контейнеров не удаляет эти данные.

## Безопасность

- использовать уникальные случайные значения `POSTGRES_PASSWORD` и `ADMIN_SECRET_KEY`;
- хранить production `.env` только на сервере с правами доступа `600`;
- не публиковать `BOT_TOKEN` в Git, логах и сообщениях;
- не открывать порт PostgreSQL в интернет;
- выдавать боту только необходимые права в Telegram-канале;
- регулярно устанавливать обновления сервера и Docker;

## Лицензия

Проект является частным. Условия использования и передачи определяются владельцем проекта.
