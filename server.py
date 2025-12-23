import http.server
import socketserver
import urllib.parse
import mysql.connector
from http import cookies

# --- CONFIGURACIÓN DEL SERVIDOR ---
PORT = 8000
PASSWORD_ADMIN = "admin2025"  
# Token simple para simular una sesión segura
SESSION_TOKEN = "token_secreto_acceso_autorizado"

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
# Asegúrate de que estos datos coincidan con tu instalación local de MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '', 
    'database': 'techportfolio_db'
}

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def get_login_page(self, error_msg=""):
        # Helper: Lee el archivo login.html e inyecta un mensaje de error si es necesario.
        try:
            with open('login.html', 'r', encoding='utf-8') as f:
                content = f.read()
                # Sistema de plantillas simple: reemplaza el marcador {{MENSAJE_ERROR}}
                if error_msg:
                    mensaje_html = f'<div class="error-msg">⚠ {error_msg}</div>'
                else:
                    mensaje_html = ''
                return content.replace('{{MENSAJE_ERROR}}', mensaje_html)
        except FileNotFoundError:
            return "<h1>Error: Falta el archivo login.html</h1>"
        
    def do_POST(self):
        """Maneja los envíos de formularios (Login y Contacto)"""
        
        # --- INTENTO DE LOGIN ---
        if self.path == '/login':
            # Leer los datos enviados en el cuerpo de la petición
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = urllib.parse.parse_qs(post_data)
            
            password_ingresada = data.get('password', [''])[0]

            # Verificar contraseña
            if password_ingresada == PASSWORD_ADMIN:
                # ÉXITO: Crear cookie de sesión y redirigir al panel
                self.send_response(303) # 303 See Other (Redirección)
                c = cookies.SimpleCookie()
                c["auth_session"] = SESSION_TOKEN
                self.send_header('Set-Cookie', c.output(header='').strip())
                self.send_header('Location', '/mensajes.html')
                self.end_headers()
            else:
                # FALLO: Mostrar el login nuevamente con mensaje de error
                self.send_response(200) 
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                
                html_con_error = self.get_login_page("Contraseña incorrecta. Intenta de nuevo.")
                self.wfile.write(html_con_error.encode('utf-8'))
            return

        # --- ENVÍO DE FORMULARIO DE CONTACTO ---
        if self.path == '/enviar-contacto':
            length = int(self.headers['Content-Length'])
            data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
            
            try:
                # Conexión a BD e inserción de datos
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                # Uso de parámetros (%s) para prevenir Inyección SQL
                cursor.execute("INSERT INTO mensajes (nombre, email, mensaje) VALUES (%s, %s, %s)",
                             (data['nombre_contacto'][0], data['email_contacto'][0], data['mensaje_contacto'][0]))
                conn.commit()

                # Redirigir al usuario con un parámetro de éxito para mostrar notificación
                self.send_response(303)
                self.send_header('Location', '/contacto.html?exito=1')
                self.end_headers()
            except Exception as e:
                self.send_error(500, f"Error BD: {e}")
            finally:
                # Cerrar conexión siempre, ocurra error o no
                if 'conn' in locals() and conn.is_connected(): conn.close()
            return
        super().do_POST()

    def do_GET(self):
        """Maneja las peticiones de lectura de páginas"""

        # --- CERRAR SESIÓN (LOGOUT) ---
        if self.path == '/logout':
            self.send_response(303) 
            c = cookies.SimpleCookie()
            # Borrar la cookie expirándola en el pasado
            c["auth_session"] = ""
            c["auth_session"]["expires"] = "Thu, 01 Jan 1970 00:00:00 GMT"
            self.send_header('Set-Cookie', c.output(header='').strip())
            self.send_header('Location', '/mensajes.html') 
            self.end_headers()
            return
        
        # --- ACCESO AL PANEL PRIVADO (PROTEGIDO) ---
        if self.path == '/mensajes.html':
            # 1. Verificar si existe la Cookie de autorización
            cookie_header = self.headers.get('Cookie')
            autorizado = False
            if cookie_header:
                c = cookies.SimpleCookie(cookie_header)
                if "auth_session" in c and c["auth_session"].value == SESSION_TOKEN:
                    autorizado = True

            # 2. Si NO está autorizado, mostrar formulario de login en lugar del panel
            if not autorizado:
                html_login = self.get_login_page("") 
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(html_login.encode('utf-8'))
                return

            # 3. Si está autorizado, obtener mensajes de la BD
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                cursor.execute("SELECT fecha, nombre, email, mensaje FROM mensajes ORDER BY fecha DESC")
                filas = cursor.fetchall()
                
                # Construir filas de la tabla HTML dinámicamente
                filas_html = "".join([f"<tr><td>{f[0]}</td><td>{f[1]}</td><td>{f[2]}</td><td>{f[3]}</td></tr>" for f in filas])
                
                # Inyectar las filas en la plantilla mensajes.html
                with open('mensajes.html', 'r', encoding='utf-8') as f:
                    final_content = f.read().replace("{{TABLA_CONTENIDO}}", filas_html)
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(final_content.encode('utf-8'))
                cursor.close()
                conn.close()
                return
            except Exception as e:
                self.send_error(500, f"Error leyendo BD: {e}")

        # Comportamiento por defecto para archivos estáticos (css, js, imágenes)
        return super().do_GET()

# --- ARRANQUE DEL SERVIDOR ---
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Servidor corriendo en http://localhost:{PORT}")
    httpd.serve_forever()