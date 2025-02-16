# Запуск приложения

### Сборка и запуск контейнера

```bash
docker-compose up --build
```

### После запуска контейнера API досупно по адресу

http://localhost:8080

### Swagger документация

http://localhost:8080/docs

# Конфигурация

В [.env](.env) можно задать свои

- SECRET_KEY="your_secret_key"
- DATABASE_URL="postgresql+asyncpg://user:password@host:port/db_name"

Либо можно прописать их в *environment* в [docker-compose.yml](docker-compose.yml)

Если не задать свои ключ и url, будут использоваться параметры по умолчанию

# Комментарии к заданию

Не успел реализовать весь функционал и покрыть проект тестами. Удалю этот комментарий, когда напишу
тесты.
Производительность также может быть значительно улучшена, также удалю этот комментарий, когда исправлю ограничения,
на данный момент самый ресурсозатратный процесс - регистрация нового пользователя.
