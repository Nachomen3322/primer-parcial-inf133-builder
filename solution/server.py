from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs


# class Personaje:
#     def __init__(self):
#         self.builder = builder


personajes = [
    {
        "id": 1,
        "name": "Leon",
        "level": 5,
        "role": "Wizard",
        "charisma": 10,
        "strength": 20,
        "dexterity": 5,
    },
    {
        "id": 2,
        "name": "Hazard",
        "level": 20,
        "role": "Archer",
        "charisma": 20,
        "strength": 5,
        "dexterity": 30,
    },
]


def PersonajeService():
    @staticmethod
    def actualizar_personaje(id, data):
        personaje = PersonajeService.buscar_por_id(id, data)
        if personaje:
            personaje.update(data)
            return personajes
        else:
            print("Personaje no encontrado, 404")
            return None

    @staticmethod
    def add_personaje(data):
        personajes.append(data)
        return personajes

    @staticmethod
    def add_correlativo(data):
        data["id"] = len(personajes) + 1
        personajes.append(data)
        return personajes

    @staticmethod
    def listar_personajes():
        return personajes

    @staticmethod
    def buscar_por_id(id, data):
        return [personaje for personaje in personajes if personaje["id"] == id]

    def listar_por_rol(role, level, charisma):
        return [
            personaje
            for personaje in personajes
            if personaje["role"] == role
            and personaje["level"] == level
            and personaje["charisma"] == charisma
        ]

    def eliminar_por_id(id):
        personaje = PersonajeService.buscar_por_id(id)
        if personaje:
            personajes.pop(personaje)
            return (200, personajes)
        else:
            print("Personaje no encontrado")
            return (400, [])


class HTTPResponseHandler:

    # handle response
    @staticmethod
    def handle_respone(handler, status, data):
        handler.send_response(status)
        handler.send_header("Content-type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps(data).encode("utf-8"))

    # handle reader
    @staticmethod
    def handle_reader(handler):
        content_length = int(handler.headers["Content-Length"])
        post_data = handler.rfile.read(content_length)
        return json.loads(post_data.decode("utf-8"))


# post 201, se crea 200, obtener 204


def PersonajeHandler():

    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        if parsed_path == "/personajes/":
            if (
                "role" in query_params
                and "level" in query_params
                and "charisma" in query_params
            ):
                role = query_params["role"][0]
                level = query_params["level"][0]
                charisma = query_params["charisma"][0]
                personajes_filtrados = PersonajeService.listar_por_rol(
                    role, level, charisma
                )
                if personajes_filtrados != []:
                    HTTPResponseHandler.handle_respone(self, 200, personajes_filtrados)
                else:
                    HTTPResponseHandler.handle_respone(self, 204, [])
            else:
                HTTPResponseHandler.handle_respone(self, 200, personajes)

        elif parsed_path == "/personajes":
            personajes_filtrados = PersonajeService.listar_personajes()
            if personajes_filtrados != []:
                HTTPResponseHandler.handle_respone(self, 200, personajes_filtrados)
            else:
                HTTPResponseHandler.handle_respone(self, 204, [])

        elif self.path.startswith("/personajes"):
            id = int(self.path.split("/")[-1])
            personaje = PersonajeService.buscar_por_id(id)
            if personaje:
                HTTPResponseHandler.handle_response(self, 200, [personaje])
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_POST(self):
        if self.path.startswith("/personajes"):
            data = HTTPResponseHandler.handle_reader(self)
            personajes = PersonajeService.personaje(data)
            HTTPResponseHandler.handle_response(self, 201, personajes)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/personajes/"):
            id = int(self.path.split("/")[-1])
            data = HTTPResponseHandler.handle_reader(self)
            personaje = PersonajeService.buscar_por_id(id, data)
            if personaje:
                HTTPResponseHandler.handle_response(self, 200, personajes)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Peronsaje no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_DELETE(self):
        if self.path.startswith("/personajes/"):
            id = int(self.path.split("/")[-1])
            personajes = PersonajeService.eliminar_por_id(id)

            if personajes:
                HTTPResponseHandler.handle_response(self, 200, personajes)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "Personaje no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )


# Run server
def run(server_class=HTTPServer, handler_class=PersonajeHandler, port=8000):
    server_address = ("", port)
    httpd = server_class(server_address, handler_class)
    print(f"Iniciando servidor HTTP en puerto {port}...")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
