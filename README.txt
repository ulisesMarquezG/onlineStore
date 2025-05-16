# Tienda Virtual Django (Python 2.7)

Este proyecto implementa una tienda virtual básica usando Django 1.11 y Python 2.7. Permite a los usuarios registrarse, iniciar sesión, agregar productos al carrito, calcular impuestos y confirmar órdenes.

---

## Requisitos

- Python 2.7.x
- Django 1.11.x  
- No se requieren librerías externas adicionales.
- (Opcional) SQLite3 para desarrollo rápido (configuración por defecto de Django).

---

## Estructura de Archivos

- **main/**: Aplicación principal (home, landing, etc.).
- **orders/**: Lógica del carrito, órdenes y productos.
- **media/**: Carpeta donde se almacenan las imágenes de productos (se ignora en Git).
- **requirements.txt**: Dependencias del proyecto.
- **seed_products.py**: Comando para cargar productos de ejemplo.
- **README.md**: Este archivo.
- **manage.py**: Comando de utilidad Django.

---

## Instalación y Ejecución

1. Crear entorno virtual (recomendado):  
   virtualenv venv -p python2.7  
   source venv/bin/activate

2. Instalar dependencias:  
   pip install -r requirements.txt

3. Aplicar migraciones:  
   python manage.py makemigrations  
   python manage.py migrate

4. Poblar la base de datos con productos de ejemplo:  
   python manage.py seed_products

5. Crear un superusuario (opcional, para el admin de Django):  
   python manage.py createsuperuser

6. Levantar el servidor de desarrollo:  
   python manage.py runserver

7. Abrir la tienda en el navegador:  
   http://localhost:8000/

---

## Características Principales

- Registro e inicio de sesión de usuarios.
- Listado de productos con imágenes y control de stock.
- Solo usuarios autenticados pueden agregar productos al carrito y confirmar órdenes.
- Mensajes amigables de éxito y error (por ejemplo, “sin stock”, “debes iniciar sesión”).
- Cálculo de impuestos automático según tipo de producto (libros, electrónicos, ropa).
- Panel de administración de Django (`/admin`).
- Poblado de productos demo usando el comando custom seed_products.

---

## Notas Importantes

- No subas la carpeta `media/` ni archivos de base de datos (`db.sqlite3`) al repositorio.  
  Usa `.gitignore` para asegurarte de esto.
- El entorno virtual debe crearse fuera de la carpeta del proyecto si vas a compartirlo.
- Compatible solo con Python 2.7 y Django 1.11.
- Si necesitas reiniciar la base de
