import urllib.request
import json
import socket

def check_servers():
    servers = []
    available_servers = []
    try:
        # Получаем список всех серверов
        all_ips = socket.gethostbyname_ex('all.api.radio-browser.info')[2]
        for ip in all_ips:
            try:
                # Пытаемся получить обратное DNS имя для красивого вывода
                name = socket.gethostbyaddr(ip)[0]
                servers.append(name)
            except:
                servers.append(ip)
    except Exception as e:
        return {"error": f"Не удалось получить список серверов: {e}"}

    # Проверяем доступность каждого сервера через путь /json/stats для получения данных
    for server in servers:
        try:
            server_url = f"http://{server}/json/stats"
            # Добавляем понятный User-Agent, как рекомендуется в документации
            req = urllib.request.Request(server_url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                if data.get('status') == 'OK':
                    available_servers.append(server)
        except Exception as e:
            # Игнорируем недоступные серверы
            pass
    return available_servers


# Запуск проверки
working_servers = check_servers()
print(f"Доступные серверы: {working_servers}")