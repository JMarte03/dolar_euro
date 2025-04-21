# Imagen base con Python y Debian
FROM python:3.12-slim

# Evita prompts al instalar paquetes
ENV DEBIAN_FRONTEND=noninteractive

# Instala dependencias del sistema necesarias para Playwright
RUN apt-get update && apt-get install -y \
    wget gnupg curl unzip fontconfig locales \
    libnss3 libatk-bridge2.0-0 libgtk-3-0 libxss1 libasound2 libxshmfence1 libgbm1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos del proyecto
COPY . .

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instala Playwright + navegadores
RUN pip install playwright && playwright install --with-deps

# Expone el puerto (Render escucha en 10000 por defecto, pero tú puedes usar 8080)
EXPOSE 8080

# Comando para correr la app
CMD ["python", "app.py"]
