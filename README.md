# Process Files Excels.

_CHALLENGE BACKEND_

_Se desea crear un servicio de carga de excels con validación de formato y notificación de procesamiento._

_El servicio debe presentar una api con un endpoint que permita hacer un upload de un archivo excel conjunto a un formato de mapeo que deberá respetar y una callback para informar cuando el archivo pasa de estado._

_Al subir el excel, se deberá retornar un id haciendo referencia a la tarea de carga._

_Se deberá permitir recuperar el estado de dicha tarea la cual permitirá saber si el excel está en estado “pending” si todavía no se está procesando el archivo, “processing” o “done” e informar en “errors” la cantidad de errores encontrados en el archivo. Se deberá permitir recuperar los errores del archivo de forma paginada, indicando la fila y columna que ocasionó el error_


## Trabajo realizado

_- Se Crean tres enpoint uno de permisos (token de consumo), un post y un get_

_- Se carga un file con un formato establecido y se procesa en dos parte a nivel de base de datos_

_- Se validan los enpoints_

_- Se trabaja con docker para la creacion de los ambientes necesarios para ejecutar el proyecto_

_- Se trabaja con NodeJs, Mongo, ExpressJs y TypeScrips_

_- Los servicios estan en postman, y los archivos en la raiz del proyecto._


## Iniciemos 🚀

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._


### Pre-requisitos 📋

_Tener instalado lo siguiente:_
_Node_
_Npm (en mi caso trabajé coon la Versión 14)_
_Docker_

### Instalación 🔧

_Una serie de ejemplos paso a paso que te dice lo que debes ejecutar para tener un entorno de desarrollo ejecutandose_

_1. Clonar el proyecto_
```bash
git clone https://github.com/dperea10/process-files-challenge.git
```

_2. ingresar a la carperta "cd "nombre del proyecto"_
```bash
cd process-files-challenge
```

_3. ejecutar npm install_
```bash
npm i or npm install
```

_4. Establecer conexión con su BD local, para esto debe "_
```bash
cp .env.example .env

https://github.com/dperea10/process-files-challenge/blob/main/.env.example
```

_5. ejecutar docker-compose_
```bash
npm run docker:dev
```
_6. crear una conexion local a mongo (cuando se ejecute docker, la base de datos y un user admin sera creados automaticamente)._

_7. Exportar la collection de postman para usar los enpoints en la raiz del proyecto._
```bash
https://github.com/dperea10/process-files-challenge/blob/main/Process%20File%20-%20KBX.postman_collection.json
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
DATABASE_USERNAME=root
DATABASE_PASSWORD=root
DATABASE_HOST=127.0.0.1
DATABASE_PORT=27017
DATABASE_DBNAME=process-files
JWT_SECRET=token.secret
```

## API Endpoints
routes
**Auth routes**:\
`POST /api/auth` - access\

**Upload files routes**:\
`POST /api/upload-file` - upload files\
`GET /api/upload-file` - get upload files\


## Construido con 🛠️

_NodeJs, Express, MongoDB, TypeScripts, Docker y una que otras librerías que se ven instaladas en el package.json_

## Autores ✒️

* **Diego Perea** 

## Licencia 📄

_Free_

## Expresiones de Gratitud 🎁

* Comenta a otros sobre este proyecto 📢
* Da las gracias públicamente 🤓.
