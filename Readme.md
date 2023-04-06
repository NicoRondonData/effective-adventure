# API
Para ejecutar el proyecto ejecuta el comando docker-compose up -d

## Ejecuta las migraciones

docker exec -it api_4id-api-1 alembic upgrade head
## Endpoints
Al hacer lo anterior el proyecto estara corriendo en el puerto 8042


### Registar usuario

POST localhost:8042/api/auth/register

`{
  "username": "string",
  "password": "string"
}`
### Login
POST localhost:8042/api/auth/login
`{
  "username": "string",
  "id": 0,
  "password": "string"
}`

### Logut 
POST localhost:8042/api/auth/logout
`headers: token:value`