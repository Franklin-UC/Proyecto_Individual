# TechPortfolio - Sistema de Contacto y Administración

Este proyecto es una aplicación web backend construida con **Python** (usando la librería nativa `http.server`) conectada a una base de datos **MySQL**. 

Su función principal es permitir que los visitantes envíen mensajes a través de un formulario de contacto y proporcionar un **Panel Administrativo Protegido** donde el dueño del sitio puede leer, gestionar y revisar dichos mensajes de forma segura.

## Características Principales

* **Backend Ligero:** Funciona con Python puro, sin necesidad de frameworks pesados como Django o Flask.
* **Base de Datos MySQL:** Almacenamiento persistente de los mensajes de contacto.
* **Seguridad:**
    * Sistema de Login para administradores.
    * Protección de rutas (el panel no es accesible sin iniciar sesión).
    * Manejo de sesiones mediante Cookies.
    * Protección contra inyección HTML en el login.
* **Despliegue Automático de BD:** Incluye un script SQL para configurar la base de datos en segundos.

---

## 📋 Requisitos Previos

Para ejecutar este proyecto necesitas tener instalado:

1.  **Python 3.x**: [Descargar aquí](https://www.python.org/downloads/)
2.  **Servidor MySQL**: Puede ser MySQL Community Server o paquetes como **XAMPP**, **WAMP** o **MAMP**.[Descargar aquí](https://wampserver.aviatechno.net/)
3.  **Conector de Python**: La librería `mysql-connector-python`.

---

## 🛠️ Guía de Instalación y Configuración

Sigue estos pasos en orden para poner el proyecto en marcha.

### Paso 1: Instalar dependencias
Abre tu terminal (consola o CMD) en la carpeta del proyecto y ejecuta:

```bash
pip install mysql-connector-python
```

### Paso 1: Importar la Base de Datos
El proyecto incluye un archivo llamado **`database.sql`**. Debes importarlo para crear la base de datos y la tabla necesaria.

#### 🔹 Opción A: Usando phpMyAdmin (XAMPP/WAMP)
1.  Abre tu navegador y ve a `http://localhost/phpmyadmin`.
2.  Haz clic en la pestaña **Importar** en el menú superior.
3.  Haz clic en el botón **Seleccionar archivo** (o "Choose File").
4.  Busca y selecciona el archivo **`database.sql`** dentro de la carpeta de este proyecto.
5.  Haz clic en el botón **Continuar** (o "Go") al final de la página.
    * *Verás un mensaje verde de éxito y la base de datos `techportfolio_db` aparecerá a la izquierda.*

#### 🔹 Opción B: Usando MySQL Workbench
1.  Abre Workbench y conéctate a tu servidor local.
2.  Ve al menú **File** > **Open SQL Script**.
3.  Selecciona el archivo **`database.sql`**.
4.  Haz clic en el icono del **Rayo** ⚡ para ejecutar el script completo.
5.  En el panel izquierdo ("Schemas"), haz clic derecho y selecciona **Refresh All** para ver la nueva base de datos.

### Paso 3: Verificar conexión en Python
Abre el archivo `server.py` y busca la sección de configuración. Asegúrate de que coincida con tu sistema:

```python
# server.py
db_config = {
    'host': 'localhost',
    'user': 'root',       # Usuario por defecto
    'password': '',       # Déjalo vacío si usas XAMPP. Si definiste contraseña, ponla aquí.
    'database': 'techportfolio_db'
}
```

### Paso 3: Ejecución del Servidor
Abre la terminal en la carpeta del proyecto.
Ejecuta el siguiente comando:

```Bash
python server.py
```
Si todo está bien, verás el mensaje:
Servidor corriendo en http://localhost:8000