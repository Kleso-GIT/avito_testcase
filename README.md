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

Если не задать свои ключ и url, будут использоваться параметры по умолчанию