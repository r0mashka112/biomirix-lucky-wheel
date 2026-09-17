# Развертывание Biomirix Lucky Wheel на сервере

Эта инструкция описывает production-развертывание проекта на Linux-сервере через Docker Compose. В состав запуска входят PostgreSQL, миграции базы данных, API и админ-панель, Telegram-бот и Caddy. Caddy принимает внешний трафик, автоматически получает TLS-сертификат и перенаправляет запросы во внутренние сервисы.

## 1. Что потребуется

- Сервер с Ubuntu 22.04/24.04 или Debian 12.
- Публичный IPv4-адрес.
- Домен или поддомен, например `wheel.example.com`.
- Доступ к DNS домена.
- Git-доступ к репозиторию проекта.
- Токен Telegram-бота от `@BotFather`.
- Telegram-канал, в котором бот добавлен администратором.
- Открытые входящие TCP-порты `22`, `80` и `443`. Для HTTP/3 можно также открыть UDP-порт `443`.

Минимальная рекомендуемая конфигурация сервера: 1 CPU, 1 GB RAM и 10 GB свободного диска. Для сборки Docker-образов комфортнее использовать 2 GB RAM.

## 2. Подготовить DNS

В панели управления доменом создайте A-запись и AAAA-запись:

```text
Тип:  A
Имя:  IP
Значение: ПУБЛИЧНЫЙ_IP_СЕРВЕРА
TTL:   Auto или 300
```

```text
Тип:  AAAA
Имя:  IPv6
Значение: ПУБЛИЧНЫЙ_IPv6_СЕРВЕРА
TTL:   Auto или 300
```

Проверьте, что домен уже указывает на сервер:

```bash
getent ahostsv4 wheel.example.com
```

В результате должен присутствовать публичный IP сервера. Выпускайте сертификат только после обновления DNS.

## 3. Установить Docker

Подключитесь к серверу:

```bash
ssh root@ПУБЛИЧНЫЙ_IP_СЕРВЕРА
```

Установите Docker из официального репозитория удобным скриптом:

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
rm get-docker.sh
```

Разрешите текущему пользователю запускать Docker без `sudo`:

```bash
sudo usermod -aG docker "$USER"
```

Переподключитесь к серверу и проверьте установку:

```bash
docker --version
docker compose version
```

## 4. Настроить firewall

Если используется UFW, разрешите SSH и веб-трафик:

```bash
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 443/udp
sudo ufw enable
sudo ufw status
```

Порты PostgreSQL, API и Telegram-сервиса наружу открывать не требуется. Доступ к ним идет только внутри Docker-сети.

## 5. Скачать проект

Выберите постоянный каталог приложения:

```bash
sudo mkdir -p /opt/biomirix-lucky-wheel
sudo chown "$USER":"$USER" /opt/biomirix-lucky-wheel
git clone АДРЕС_ПРИВАТНОГО_РЕПОЗИТОРИЯ /opt/biomirix-lucky-wheel
cd /opt/biomirix-lucky-wheel
```

## 6. Создать production `.env`

Скопируйте шаблон:

```bash
cp .env.example .env
chmod 600 .env
nano .env
```

Заполните файл следующими значениями (пример):

```dotenv
APP_DOMAIN=wheel.example.com
HTTP_PORT=80
HTTPS_PORT=443
ACME_EMAIL=admin@example.com

BASE_URL=https://wheel.example.com
BACKEND_API_URL=http://server:8000/api/v1
UPSTREAM_FORWARDED_PROTO=https

BOT_TOKEN=1234567890:telegram-bot-token
TELEGRAM_CHANNEL_ID=-1001234567890
TELEGRAM_CHANNEL_URL=https://t.me/example_channel
TELEGRAM_INIT_DATA_MAX_AGE_SECONDS=86400

POSTGRES_USER=biomirix
POSTGRES_PASSWORD=replace-with-a-long-random-password
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=biomirix

ADMIN_TITLE=Biomirix Admin
ADMIN_SECRET_KEY=replace-with-a-long-random-secret
```

Назначение ключевых переменных:

| Переменная | Production-значение |
| --- | --- |
| `APP_DOMAIN` | Домен без `http://`, `https://` и завершающего `/` |
| `BASE_URL` | Полный публичный HTTPS-адрес без завершающего `/` |
| `BACKEND_API_URL` | Внутренний адрес API: `http://server:8000/api/v1` |
| `UPSTREAM_FORWARDED_PROTO` | `https`, чтобы API и админ-панель формировали HTTPS-ссылки |
| `POSTGRES_HOST` | Имя сервиса Compose: `db` |
| `ACME_EMAIL` | Email для уведомлений центра сертификации |

Сгенерировать надежные значения для `POSTGRES_PASSWORD` и `ADMIN_SECRET_KEY` можно командами:

```bash
openssl rand -base64 36
openssl rand -hex 32
```

## 7. Запустить проект

Проверьте итоговую конфигурацию Compose:

```bash
docker compose config --quiet
```

Соберите образы и запустите сервисы:

```bash
docker compose up -d --build
```

Миграции выполняются автоматически отдельным сервисом `migrations`. После успешного запуска он завершится с кодом `0`; это штатное поведение.

Посмотрите состояние контейнеров:

```bash
docker compose ps -a
```

Ожидаемое состояние:

- `db`, `server`, `client` и `caddy` работают;
- `db`, `server` и `client` имеют статус `healthy`;
- `migrations` имеет статус `Exited (0)`.

При первом запуске Caddy автоматически запросит сертификат. Обычно это занимает несколько секунд.

## 8. Создать администратора

После запуска создайте учетную запись админ-панели:

```bash
docker compose run --rm server python -m src.cli create-admin --username admin
```

Команда дважды запросит пароль. Ввод пароля в терминале не отображается.

Админ-панель будет доступна по адресу:

```text
https://wheel.example.com/admin/login
```

## 9. Проверить развертывание

Проверьте API:

```bash
curl --fail --show-error https://wheel.example.com/api/v1/health
```

Ожидаемый ответ:

```json
{"status":"ok"}
```

Проверьте главную страницу и HTTPS-заголовки:

```bash
curl --head https://wheel.example.com/
```

Проверьте зарегистрированный Telegram webhook:

```bash
curl "https://api.telegram.org/bot<BOT_TOKEN>/getWebhookInfo"
```

В поле `url` должен быть адрес `https://wheel.example.com/webhook`, а `last_error_message` должен отсутствовать.

После этого откройте бота в Telegram, отправьте `/start` и проверьте запуск Web App.

## 10. Посмотреть логи

Логи всех активных сервисов:

```bash
docker compose logs -f --tail=200
```

Логи отдельных сервисов:

```bash
docker compose logs -f --tail=200 caddy
docker compose logs -f --tail=200 server
docker compose logs -f --tail=200 client
docker compose logs --tail=200 migrations
docker compose logs -f --tail=200 db
```

Выход из режима просмотра логов: `Ctrl+C`. Контейнеры продолжат работать.


Compose пересоберет изменившиеся образы, выполнит новые миграции и перезапустит нужные сервисы. Данные PostgreSQL и сертификаты Caddy находятся в Docker volumes и сохраняются при обычном пересоздании контейнеров.

## 11. Перезапуск и остановка

Перезапустить все сервисы:

```bash
docker compose restart
```

Перезапустить один сервис:

```bash
docker compose restart server
```

Остановить проект с сохранением данных:

```bash
docker compose down
```

Запустить его снова:

```bash
docker compose up -d
```

Не используйте `docker compose down -v` на production-сервере: флаг `-v` удаляет том PostgreSQL с данными и том Caddy с сертификатами.

## 12. Частые проблемы

### Caddy не получает сертификат

Проверьте:

- `APP_DOMAIN` содержит реальный домен без протокола;
- A-запись домена указывает на IP сервера;
- TCP-порты `80` и `443` доступны из интернета;
- другой процесс на сервере не занимает эти порты;
- в `ACME_EMAIL` указан корректный email.

Диагностика:

```bash
docker compose logs --tail=200 caddy
sudo ss -lntup | grep -E ':80|:443'
```

### Контейнер `client` нездоров

Посмотрите логи:

```bash
docker compose logs --tail=200 client
```

Чаще всего причина связана с неверным `BOT_TOKEN`, недоступностью Telegram API или некорректным `BASE_URL`. Для production `BASE_URL` должен начинаться с `https://`.

### Админ-панель загружается без стилей

Проверьте production-настройки:

```dotenv
BASE_URL=https://wheel.example.com
UPSTREAM_FORWARDED_PROTO=https
```

Затем пересоздайте сервисы:

```bash
docker compose up -d --force-recreate server client caddy
```

### Миграции завершились с ошибкой

```bash
docker compose logs --tail=200 migrations
docker compose logs --tail=200 db
```

После исправления `.env` или доступности базы повторите запуск:

```bash
docker compose up -d
```

### Порт 80 или 443 уже занят

Найдите процесс:

```bash
sudo ss -lntup | grep -E ':80|:443'
```