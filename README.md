# SpotiGraph - Visualización de colaboraciones de artistas en Spotify
SpotiGraph es una aplicación web que utiliza la API de Spotify para generar una visualización en 3D de las colaboraciones de un artista en particular. La aplicación utiliza Flask y SQLAlchemy para el backend y React y D3 para el frontend.

## Funcionalidades
- Búsqueda de artistas en la API de Spotify.
- Generación de un force directed graph en 3D del artista y sus colaboradores.
- Conexión entre los nodos que representan a los artistas que han colaborado en una canción juntos.
- Recursividad de la generación del force directed graph hasta llegar a un tope de nodos dado por el usuario.

## Tecnologías utilizadas
Backend:

- Flask
- SQLAlchemy
- Spotify API

## Frontend:

- React
- D3
- Bootstrap (Por ahora, la idea es agregarle CSS al finalizar todo lo demas)

## Instalación
1. Clonar el repositorio en tu máquina local.
2. Instalar las dependencias de backend con pip install -r requirements.txt.
3. Crear una cuenta y obtener las credenciales de la API de Spotify.
4. Configurar las credenciales en el archivo .env.
5. Instalar las dependencias de frontend con npm install.

## Uso
1. Ejecutar el backend con python main.py.
2. Ejecutar el frontend con npm start.
3. En el navegador, acceder a http://localhost:3000/.
4. Buscar un artista y explorar el force directed graph generado.


## [DEMO](https://www.youtube.com/watch?v=ACRrcaVPWw8)



