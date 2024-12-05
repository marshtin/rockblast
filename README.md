-Paso 1: Clonar el repositorio
-Paso 2: Cargar tifs con los siguientes nombres: RES.tif, REE.tif en App>data
-Paso 3: Reiniciar el editor de código que ud. utiliza para que se actualice el directorio data.
-Paso 4: Iniciar editor de código.
-Paso 5: Ejecutar App/app.py

Estructura:
-assets: estilos, imágenes
-callbacks: funciones para eventos dentro del front-end
-components: vistas html layouts
-data: tiffs y geojson
-databse: conexion a base de datos, credenciales y queries
-utils: funcion para transformar el tiff y cargarlo
app.py: ejecuta la aplicacion


Ejecutar a traves de docker, para omitir descarga individual de dependencias/librerias.
-Paso 1 Instalar Docker.
-Paso 2 Descargar el proyecto desde GitHub.
-Paso 3 Cargar tifs según instrucciones anteriores.
-Paso 3 Construir la imagen con docker build.
-Paso 3.1 "docker build -t rockblast-app ."
-Paso 4 Ejecutar el contenedor con docker run.
-Paso 4.1 "docker run -d -p 8080:8080 rockblast-app"
-Paso 5 Acceder a la aplicación en el navegador o desde la app docker.
