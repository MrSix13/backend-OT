# Establecer la imagen base para tu aplicación Django
FROM python:3.9-alpine

# Establecer el directorio de trabajo
WORKDIR /code

# Instalar las dependencias del sistema necesarias para PostgreSQL
RUN apt-get update && apt-get install -y postgresql-client

# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instalar las dependencias de tu aplicación Django
RUN pip install -r requirements.txt

# Copiar el resto de los archivos de tu aplicación al contenedor
COPY . .

# Definir las variables de entorno para la base de datos PostgreSQL
ENV DB_NAME=databasetest2
ENV DB_USER=postgres
ENV DB_PASSWORD=password
ENV DB_HOST=db
ENV DB_PORT=5432

# Ejecutar las migraciones de Django y crear el superusuario (opcional)
RUN python manage.py migrate
# RUN echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

# Exponer el puerto 8000 para acceder a la aplicación
EXPOSE 8000

# Iniciar el servidor de desarrollo de Django
CMD python manage.py runserver 0.0.0.0:8000
