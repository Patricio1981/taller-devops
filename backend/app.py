import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit


PRODUCTOS = [
    {"id": 1, "nombre": "Taza de cerámica", "precio": 8500, "stock": 12},
    {"id": 2, "nombre": "Plato de cerámica", "precio": 12000, "stock": 8},
    {"id": 3, "nombre": "Florero de cerámica", "precio": 18000, "stock": 5},
]


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        ruta = urlsplit(self.path).path

        if ruta == "/productos":
            self.enviar_json(200, PRODUCTOS)
        elif ruta == "/health":
            self.enviar_json(200, {"status": "ok"})
        else:
            self.enviar_json(404, {"error": "No encontrado"})

    def enviar_json(self, estado, datos):
        contenido = json.dumps(datos, ensure_ascii=False).encode("utf-8")
        self.send_response(estado)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(contenido)))
        self.end_headers()
        self.wfile.write(contenido)


if __name__ == "__main__":
    puerto = int(os.environ.get("PORT", "8000"))
    with HTTPServer(("0.0.0.0", puerto), Handler) as servidor:
        print(f"Servidor escuchando en el puerto {puerto}", flush=True)
        servidor.serve_forever()
