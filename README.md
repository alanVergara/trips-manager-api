# trips-manager-api

- Es necesario contar con los siguientes repositorios para la prueba integral del sistema

- Backend: https://github.com/alanVergara/trips-manager-api
- Frontend: https://github.com/alanVergara/trips-manager-front

## Instalación API (Backend)

- Instalar pip https://pip.pypa.io/en/stable/installing/

- Instalar Python (version 3.9.1) https://www.python.org/downloads/

- Ingresar a directorio del proyecto descargado
    - cd <local-path>/trips-manager-api/

- Instalar las dependencias presentes dentro del archivo requirements.txt con pip
    - pip install -r requirements.txt

- Ingresar a la carpeta "app" dentro del proyecto
    - cd <local-path>/trips-manager-api/app

- Dentro de la carpeta "app" correr los siguientes comandos para generacion de tablas
    - python manage.py makemigrations main
    - python manage.py migrate

- Ejecutar test
    - python manage.py test

- Ejecutar test junto con flake8 para verificar tests y buenas practicas dentro del codigo
    - python manage.py test && flake8

- Iniciar servidor (por defecto es iniciado en http://127.0.0.1:8000/)
    - python manage.py runserver

- Iniciar servidor en un puerto en particular
    - python manage.py runserver <port_number>

- Abrir navegador para visualizar administrador de usuarios creados en API (En caso de ser necesario)
    - http://127.0.0.1:<port_number>/admin

## Instalación Aplicación Vue (FrontEnd)

- Instalar Node (version v14.13.1) y npm (version 6.14.8)
    https://nodejs.org/en/

- Instalar Cliente de Vue
    https://cli.vuejs.org/guide/installation.html

- Instalar Vue prototyping
    https://cli.vuejs.org/guide/prototyping.html

- Ingresar dentro de la carpeta contenedora del proyecto front
    - cd <local-path>/trips-manager-front

- Instalar las dependencias del proyecto
    - npm install

- Iniciar aplicación
    - npm run serve

## Funcionalidades y alcances

- Se debe iniciar ambos proyectos para realizar una prueba integral

- En caso de iniciar la API en un puerto diferente al 8000, se debe modificar el siguiente archivo
    (reemplazar valor del puerto en linea 6 dentro de "axios.defaults.baseURL")
    - <local-path>/trips-manager-front/src/axios.js

- Se generan 3 tipos de usuario: pasajeros, conductores y administradores

- La base de datos contiene información de ejemplo

- Se provee un super admin para efectos de pruebas, ingresar al panel de administración de usuarios dentro de la API
    - En navegador: http://127.0.0.1:<port_number>/admin
    - username: superadmin
    - password: PS9sup8adm7PS

- Se provee un usuario administrador para la plataforma web
    - username: adminplataform
    - password: TS9p1a9s2s8TS

- En caso de querer generar un nuevo usuario administrador, la unica manera es directamente a traves del modulo de administracion de la API y asignarle el rol de administrador

- Permisos por tipo de usuario 

    Funcionalidades usuarios sin iniciar sesión:
        - Visualización de listado de viajes
        - Iniciar sesión
        - Registro de pasajeros 

    Funcionalidades al iniciar sesión con cuenta Pasajero: 
        - Visualización de listado de viajes
        - Opción de reserva de tickets dentro de listado de viajes
        - Visualizacion de pantalla de tickets con filtro por viaje
        - Visualización de tickets disponibles por viaje
        - Reservar ticket 
        - Cerrar sesión
        - Editar datos de cuenta
        - Borrar su cuenta
    
    Funcionalidades al iniciar sesión con cuenta Conductor:
        - Visualizar listado de viajes
        - Editar datos de cuenta
        - Cerrar sesión
    
    Funcionalidades al iniciar sesion con cuenta Administrador:
        - CRUD Rutas
        - CRUD Buses
        - CRUD Viajes
        - Crear y borrar Conductores
        - Visualizar promedio de pasajeros por trayecto dentro de listado de rutas
        - Visualización de buses con más de un cierto porcentaje de su capacidad utilizada por ruta
        - Cerrar sesión
