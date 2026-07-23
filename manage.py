from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = "localhost"
SERVER_PORT = 8080


class MyServer(BaseHTTPRequestHandler):
    """Класс для обработки входящих HTTP-запросов"""

    def do_GET(self):
        """Задание 2: Обработка всех GET-запросов.
        Возвращает содержимое HTML-файла с контактами.
        """
        self.send_response(200)
        # Меняем заголовки на text/html
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        # Читаем HTML-файл через конструкцию с менеджером контекста с помощью with open()
        try:
            with open("app/templates/contacts.html", "r", encoding="utf-8") as file:
                html_content = file.read()
            self.wfile.write(bytes(html_content, "utf-8"))
        except FileNotFoundError:
            self.wfile.write(bytes("<h1>Ошибка: файл contacts.html не найден</h1>", "utf-8"))

    def do_POST(self):
        """* Дополнительное задание: Обработка POST-запросов.
        Считывает переданные пользователем данные и выводит их в консоль.
        """
        # Читаем заголовок Content-Length, чтобы узнать размер полученного тела запроса
        content_length = int(self.headers.get("Content-Length", 0))

        # Считываем само тело запроса из self.rfile
        post_data = self.rfile.read(content_length).decode("utf-8")

        # Печатаем полученные данные в консоль
        print("\n--- Получены данные POST-запроса ---")
        print(post_data)
        print("-----------------------------------\n")

        # Отправляем ответ клиенту
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(bytes("<h1>Данные успешно приняты!</h1>", "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((HOST_NAME, SERVER_PORT), MyServer)
    print(f"Server started at http://{HOST_NAME}:{SERVER_PORT}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")