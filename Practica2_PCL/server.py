# Universidad Politécnica de Madrid - Curso 2025-26
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import datetime
import socket

hostName = "localhost"
serverPort = 8080

asignatura = "Programaci&oacute;n clientes (Web) Ligeros 2025-26"
piePagina = f"{asignatura}. UPM ({datetime.datetime.now().strftime('%c')} en {socket.gethostname()})"

class MyServer(BaseHTTPRequestHandler):

    def obtener_mimetype(self, fichero):
        if fichero.endswith(".css"): return "text/css"
        if fichero.endswith(".gif"): return "image/gif"
        if fichero.endswith(".png"): return "image/png"
        if fichero.endswith(".jpg") or fichero.endswith(".jpeg"): return "image/jpeg"
        if fichero.endswith(".js"): return "application/javascript"
        if fichero.endswith(".ico"): return "image/x-ico"
        return "text/html"

    def procesar_y_responder(self, metodo):
        print(f"PETICIÓN RECIBIDA ({metodo}): {self.requestline}")


        # Si es POST, leemos y mostramos el cuerpo
        #if metodo == "POST":
            #content_length = int(self.headers.get('Content-Length', 0))
            #post_data = self.rfile.read(content_length)
            #print(f"CUERPO (PAYLOAD) RECIBIDO:\n{post_data.decode('utf-8', errors='ignore')}\n")

        # 2. DETERMINAR EL ARCHIVO Y MIME TYPE
        parsed_path = urlparse(self.path)
        fichero = "index.html" if self.path == "/" else parsed_path.path[1:]
        mimetype = self.obtener_mimetype(fichero)

        try:
            with open(fichero, 'rb') as f:
                contenido = f.read()
                codigo_resp = 200
            print(f"FICHERO ENCONTRADO: {fichero}")
        except (FileNotFoundError, IOError):
            contenido = bytes(self.pagina_default(), "utf-8")
            codigo_resp = 404
            mimetype = "text/html"


        # 3. PREPARAR Y MOSTRAR CABECERAS EMITIDAS
        print(f"RESPUESTA HTTP ENVIADA ({codigo_resp}):")

        self.send_response(codigo_resp)
        self.send_header("Content-type", mimetype)
        self.send_header("Content-Length", str(len(contenido)))
        self.send_header("Server-Software", "Python/UPM-Didactic")
        self.end_headers()


        # 4. ENVIAR EL CUERPO
        self.wfile.write(contenido)

    def do_GET(self):
        self.procesar_y_responder("GET")

    def do_POST(self):
        self.procesar_y_responder("POST")

    def pagina_default(self):
        return f"<html><body><h1>Error 404</h1><p>{piePagina}</p></body></html>"

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Servidor UPM activo en http://{hostName}:{serverPort}")
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        webServer.server_close()
        print("\nServidor apagado.")
