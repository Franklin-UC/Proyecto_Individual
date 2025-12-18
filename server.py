import http.server
import socketserver
import urllib.parse
import mysql.connector

# Configuración de BD 
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '', # Contraseña de MySQL
    'database': 'techportfolio_db'
}

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
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
                self.send_error(500, f"Error: {e}")
            finally:
                if conn.is_connected(): conn.close()

    def do_GET(self):
        if self.path == '/mensajes.html':
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
                self.send_error(500, f"Error: {e}")
        return super().do_GET()

PORT = 8000
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Servidor profesional en http://localhost:{PORT}")
    httpd.serve_forever()