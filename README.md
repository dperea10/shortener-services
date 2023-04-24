# Shortened urls.


_Se servicio para acortar urls, y darle a marketing una herramienta para lograr enviarlas con la cantidad minima de carácteres_


## Trabajo realizado

_- Se Crean varios enpoint uno de permisos (token de consumo)y los otros para la funcionalidad del servicio_

_- Se trabajar con una migración basica de un user para obtener el token y lograr usar el servicio_

_- Se validan los enpoints por token_

_- Se trabaja con docker para la creacion de los ambientes necesarios para ejecutar el proyecto_

_- Se trabaja con python -FastApi, MongoDB, Redis, entre otros_

_- Los servicios estan en postman, y las  documentacion de fastapi y se dejaran los archivos en la raiz del proyecto._


## Iniciemos 🚀

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._


### Pre-requisitos 📋

_Tener instalado lo siguiente:_
_Python3.9 en mi caso_
_Pip_
_Docker_

### Instalación 🔧

_Una serie de ejemplos paso a paso que te dice lo que debes ejecutar para tener un entorno de desarrollo ejecutandose_

_1. Clonar el proyecto_
```bash
git clone https://github.com/dperea10/shortener-services.git
```

_2. ingresar a la carperta "cd "nombre del proyecto"_
```bash
cd shortener-services
```

_3. Establecer conexión con su BD local, para esto debe "_
```bash
cp .env.example .env

https://github.com/dperea10/shortener-services/.env.example
```

_4. ejecutar docker-compose_
```bash
docker-compose up --build
```


### Configuración 🔧

_Una serie de ejemplos paso a paso que te dice lo que debes ejecutar para tener un entorno de desarrollo ejecutandose_

_1. Después de realizar la instalación se explica un poco la configuración_

_En la raiz del proyecto se ecuentran dos archivos, llamados formart-file.xlsx y formart-fileErr.xlsx, con estos archivos podemos realizar las pruebas y validaciones correspondientes_

_En el postman se encuentra un enpoint para auth, pero no es necesario ejecutarlo para usar los otros, porque ya se genera de manera automatica al correr el docker una vez configurado como se explico anteriormente. Este user nos sirve para lograr consumir los otros servicios._

_En el postman se encuentra un enpoint para subir el archivo e internamente cumple con una serie de procesos y validaciones y en base de datos podemos ver que se generan dos docuemntos uno para los status y el otro para los registros._

_En el postman se encuentra un enpoint para obtener la informació con una serie de filtrados, por id, status, limit, max, skip, entre otros._

## Extras

## Variables de Entorno

En el archivo `.env`. Se encuentran estos valores predeterminados lo puedes cambiar segun tu entorno:
```bash
APP_MONGO_URI=mongodb://localhost:27017/shortened_url
APP_DATABASE_NAME=shortened_url
APP_JWT_SECRET=my_secret_key
APP_HOST_REDIS=127.0.0.1
APP_PORT_REDIS=6379
MONGODB_HOST=mongodb://localhost:27017/

APP_BASE_URL_SERVICE=http://127.0.0.1:8080/
```

## API Endpoints
routes
**Auth routes**:\
`POST /service/v1/short-url/login` - access\

**Upload files routes**:\
`POST /service/v1/short-url` - create short url\
`GET /service/v1/short-url/long-url-by/:hash_url` - getlong url\
`DELETE /service/v1/short-url/delete-by/:hash_url` - delete short url\
`GET /service/v1/short-url/record/register` - get all shorts urls\
`GET /service/v1/short-url/record/platforms/used` - get records platfomrs\
`GET /service/v1/short-url/record/clicks/used/:hash_url` - get records clicks\


## Construido con 🛠️

Python, FastApi, MongoDB, Redis, Docker y una que otras librerías que se ven instaladas en el requirements_

## Autores ✒️

* **Diego Perea** 

## Licencia 📄

_Free_

## Expresiones de Gratitud 🎁

* Comenta a otros sobre este proyecto 📢
* Da las gracias públicamente 🤓.
