# Desarrollado por la asignatura Programación de clientes ligeros
# Universidad Politécnica de Madrid
# Curso 2024-25

import conf

from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib

import logging as lg
import datetime
import socket

piePagina = conf.ASIGNATURA + "Universidad Polit&eacute;cnica de Madrid ("+datetime.datetime.now().strftime("%c")+" en "+socket.gethostname()+")"

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):

        lg.debug("New request: "+self.path+" from: "+self.client_address[0])
        try:
            parsed_path = urllib.parse.urlparse(self.path)

            sendReply = True
            petición = self.path[1:]
            if (petición == ""):

                petición="index.html"

            elif (petición == "favicon.ico"):
                pass


            elif ("reservar_puesto" in petición):
                query_params = urllib.parse.parse_qs(parsed_path.query)
                self.send_headers(200, "text/plain")

                self.wfile.write(bytes(self.datos_formulario(query_params), "utf-8"))

                sendReply = False


            if petición.endswith(".html"):
                mimetype='text/html'
            elif petición.endswith(".jpg"):
                mimetype='image/jpg'
            elif petición.endswith(".gif"):
                mimetype='image/gif'
            elif petición.endswith(".js"):
                mimetype='application/javascript'
            elif petición.endswith(".css"):
                mimetype='text/css'
            elif petición.endswith(".ico"):
                mimetype='image/x-ico'
            elif petición.endswith(".png"):
                mimetype='image/png'
            elif petición.endswith(".bmp"):
                mimetype='image/bmp'

            else:

                petición = parsed_path.path[1:]




            if sendReply:


                self.send_headers(200, mimetype)
                templateFile=open(petición,'rb')
                string=templateFile.read()
                self.wfile.write(string)

        except ( FileNotFoundError):
            lg.warning(f"Se solicita una página o fichero '{self.path}' inexistente.")
            self.wfile.write(bytes(self.pagina_default(), "utf-8"))
        except (IOError):
            lg.warning(f"Se ha producido un error indefinido")
            self.wfile.write(bytes(self.pagina_default(), "utf-8"))

    def send_headers(self, status, content_type):
        #    """Send out the group of headers for a successful request"""
        # Send HTTP headers

        self.send_response(status, "OK")
        self.send_header('Content-type', content_type)
        self.send_header('Transfer-Encoding', 'chunked')
        self.send_header('Connection', 'close')
        self.end_headers()

    def pagina_default(self):
        pagina = "<html><head>"
        pagina += "<title>"+conf.ASIGNATURA + " WEB Server script</title>"
        pagina += "<meta charset=\"utf-8\" />"
        pagina += "<meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\">"
        pagina += "</head>"


        pagina += "<body>"
        pagina += "<h1>"+conf.ASIGNATURA+"</h1>"
        pagina +="<p><b>ERROR</b> No se ha encontrado la página.</p>"
        pagina += "<p id=\"fecha\">"+piePagina + "</p>"
        pagina += "<p align=\"center\"><a href=\"index.html\">Volver al ménu</a>"
        pagina += "</body></html>"
        return pagina


    def datos_formulario(self, query_params):
        # Extraemos los datos usando los 'name' del formulario HTML
        empleado = query_params.get("empleado", [""])[0]
        departamento = query_params.get("departamento", ["No especificado"])[0]
        tipo_puesto = query_params.get("tipo", ["No especificado"])[0]
        planta = query_params.get("planta", ["No especificada"])[0]
        
        # 'extra' es un checkbox, puede devolver una lista de valores
        extras_lista = query_params.get("extra", ["Ninguno"])
        extras = ", ".join(extras_lista)
        
        notas = query_params.get("notas", ["Sin observaciones"])[0]

        # Construimos la respuesta visual
        aux = f"""
            <div style="text-align: left; padding: 10px; border-left: 4px solid #004080;">
                <p><strong>Confirmación de Solicitud:</strong></p>
                <p><b>Empleado:</b> {empleado}</p>
                <p><b>Departamento:</b> {departamento}</p>
                <p><b>Ubicación:</b> Planta {planta} ({tipo_puesto.capitalize()})</p>
                <p><b>Equipamiento adicional:</b> {extras}</p>
                <p><b>Notas de mantenimiento:</b> {notas}</p>
            </div>
        """
        return aux






if __name__ == "__main__":

    lg.info("Starting web server...")

    webServer = HTTPServer((conf.HOSTNAME, conf.SERVER_PORT), MyServer)

    lg.info("Server started http://%s:%s" % (conf.HOSTNAME, conf.SERVER_PORT))
    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        lg.error("Keyboard interruption. Stopping web server...")

    webServer.server_close()
    lg.info ("Server stopped.")
