import http.server
import socketserver
import urllib.parse
import mysql.connector
from http import cookies

# --- CONFIGURACIÓN ---
PORT = 8000
PASSWORD_ADMIN = "admin2025"  
SESSION_TOKEN = "token_secreto_acceso_autorizado"

# Configuración de BD 
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '', 
    'database': 'techportfolio_db'
}

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def get_login_page(self, error_msg=""):
        """Ayuda a cargar el HTML del login e inyectar errores si los hay"""
        try:
            with open('login.html', 'r', encoding='utf-8') as f:
                content = f.read()
                if error_msg:
                    mensaje_html = f'<div class="error-msg">⚠ {error_msg}</div>'
                else:
                    mensaje_html = ''
                return content.replace('{{MENSAJE_ERROR}}', mensaje_html)
        except FileNotFoundError:
            return "<h1>Error: Falta el archivo login.html</h1>"
        
    def do_POST(self):
        # --- LOGIN ---
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = urllib.parse.parse_qs(post_data)
            
            password_ingresada = data.get('password', [''])[0]

            if password_ingresada == PASSWORD_ADMIN:
                # ÉXITO: Redirigir
                self.send_response(303)
                c = cookies.SimpleCookie()
                c["auth_session"] = SESSION_TOKEN
                self.send_header('Set-Cookie', c.output(header='').strip())
                self.send_header('Location', '/mensajes.html')
                self.end_headers()
            else:
                self.send_response(200) 
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                
                html_con_error = self.get_login_page("Contraseña incorrecta. Intenta de nuevo.")
                self.wfile.write(html_con_error.encode('utf-8'))
            return

        # --- ENVIAR CONTACTO ---
        if self.path == '/enviar-contacto':
            length = int(self.headers['Content-Length'])
            data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
            
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO mensajes (nombre, email, mensaje) VALUES (%s, %s, %s)",
                             (data['nombre_contacto'][0], data['email_contacto'][0], data['mensaje_contacto'][0]))
                conn.commit()

                self.send_response(303)
                self.send_header('Location', '/contacto.html?exito=1')
                self.end_headers()
            except Exception as e:
                self.send_error(500, f"Error BD: {e}")
            finally:
                if 'conn' in locals() and conn.is_connected(): conn.close()
            return

        super().do_POST()

    def do_GET(self):
        # --- CERRAR SESIÓN  ---
        if self.path == '/logout':
            self.send_response(303) 
            c = cookies.SimpleCookie()
            c["auth_session"] = ""
            c["auth_session"]["expires"] = "Thu, 01 Jan 1970 00:00:00 GMT"
            self.send_header('Set-Cookie', c.output(header='').strip())
            self.send_header('Location', '/mensajes.html') 
            self.end_headers()
            return
        
        # --- RUTA PROTEGIDA ---
        if self.path == '/mensajes.html':
            # 1. Verificar Cookie
            cookie_header = self.headers.get('Cookie')
            autorizado = False
            if cookie_header:
                c = cookies.SimpleCookie(cookie_header)
                if "auth_session" in c and c["auth_session"].value == SESSION_TOKEN:
                    autorizado = True

            # 2. Si NO está autorizado, servir login.html
            if not autorizado:
                html_login = self.get_login_page("") 
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(html_login.encode('utf-8'))
                return

            # 3. Si SÍ está autorizado, mostrar datos
            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                cursor.execute("SELECT fecha, nombre, email, mensaje FROM mensajes ORDER BY fecha DESC")
                filas = cursor.fetchall()
                
                filas_html = "".join([f"<tr><td>{f[0]}</td><td>{f[1]}</td><td>{f[2]}</td><td>{f[3]}</td></tr>" for f in filas])
                
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

        return super().do_GET()

with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Servidor corriendo en http://localhost:{PORT}")
    httpd.serve_forever()