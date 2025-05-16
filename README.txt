Tienda Virtual - Django 1.11 / Python 2.7

=========================================
DESCRIPCIÓN GENERAL
=========================================
Este proyecto implementa una tienda virtual simple con las siguientes funcionalidades principales:

- Registro e inicio de sesión de usuarios (solo usuarios autenticados pueden comprar).
- Listado de productos (con imágenes y control de stock).
- Carrito de compras: cada usuario puede agregar productos y cantidades a su propio carrito.
- Gestión de órdenes: al confirmar la orden, el carrito se cierra y no puede ser modificado.
- Cálculo de impuestos según el tipo de producto.
- Mensajes informativos y de error al usuario (sin stock, éxito de compra, etc).

Todo el sistema es compatible con Python 2.7 y Django 1.11, **sin uso de librerías externas** (solo las de Python y Django).

=========================================
REQUISITOS
=========================================
- Python 2.7.x
- Django 1.11.x (se instala automáticamente con requirements.txt)
- SQLite (por defecto, o tu gestor compatible con Django)

=========================================
INSTALACIÓN Y USO
=========================================

1. **(Recomendado) Crear el entorno virtual FUERA del proyecto:**

    $ cd /ruta/donde/guardar/entorno
    $ virtualenv venv -p python2.7
    $ source venv/bin/activate

2. **Entrar a la carpeta del proyecto:**

    $ cd /ruta/del/proyecto/onlineStore

3. **Instalar las dependencias:**

    $ pip install -r requirements.txt

4. **Aplicar migraciones:**

    $ python manage.py makemigrations
    $ python manage.py migrate

5. **Poblar productos de ejemplo (ejecutar el comando seed):**

    $ python manage.py seed_products

6. **(Opcional) Crear un superusuario para administrar:**

    $ python manage.py createsuperuser

7. **Levantar el servidor:**

    $ python manage.py runserver

8. **Acceder en el navegador:**

    http://localhost:8000/

=========================================
NOTAS Y SUGERENCIAS
=========================================
- El archivo `requirements.txt` se encuentra en la raíz del proyecto y debe ser usado para instalar las dependencias.
- El entorno virtual debe estar siempre **fuera** de la carpeta del proyecto para evitar mezclar archivos y accidentalmente subirlos a repositorios.
- Puedes crear productos de prueba desde el panel de administración (`/admin`) o ejecutando el comando `python manage.py seed_products`.
- Solo los usuarios autenticados pueden agregar productos al carrito y cerrar órdenes.
- El stock se controla automáticamente; si no hay suficientes existencias, se mostrará un mensaje y no se permitirá la compra.
- El sistema muestra los impuestos calculados para cada producto según su tipo (libro, electrónico, ropa).
- Las rutas principales están en las apps `main` y `orders`. El registro y login usan los views y templates integrados de Django.

=========================================
AUTORES / CONTACTO
=========================================
Proyecto desarrollado como práctica para gestión básica de e-commerce en Django.
Puedes contactarme en: [tu-email@ejemplo.com]

