#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Программа для измерения скорости ответа API radio-browser.info.
Выполняет DNS-запрос для получения списка всех серверов,
затем измеряет время отклика каждого из них.
"""

import urllib.request
import json
import socket
import time
import statistics


def get_all_api_servers():
    """
    Получает список всех серверов API через DNS-запрос к all.api.radio-browser.info.
    Возвращает список имён серверов (например, ['de1.api.radio-browser.info', ...]).
    """
    servers = []
    try:
        # Запрашиваем все IP-адреса, связанные с именем all.api.radio-browser.info
        all_ips = socket.gethostbyname_ex('all.api.radio-browser.info')[2]
        for ip in all_ips:
            try:
                # Пытаемся получить обратное DNS-имя для красивого вывода
                name = socket.gethostbyaddr(ip)[0]
                servers.append(name)
            except socket.herror:
                # Если обратного разрешения нет, используем IP
                servers.append(ip)
    except socket.gaierror as e:
        print(f"Ошибка DNS-запроса: {e}")
        return []
    return servers


def measure_response_time(server, timeout=5):
    """
    Измеряет время полного ответа от заданного сервера.
    Путь: /json/stats
    Возвращает время в секундах или None в случае ошибки.
    """
    url = f"http://{server}/json/stats"
    req = urllib.request.Request(
        url,
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    )
    try:
        start = time.time()
        with urllib.request.urlopen(req, timeout=timeout) as response:
            # Читаем всё содержимое, чтобы быть уверенными, что ответ полностью получен
            response.read()
        elapsed = time.time() - start
        return elapsed
    except Exception as e:
        # Любая ошибка (таймаут, соединение, HTTP ошибка) обрабатывается как недоступность
        return None


def main():
    print("=== Измерение скорости ответа API radio-browser.info ===\n")

    # 1. Получаем список серверов
    servers = get_all_api_servers()
    if not servers:
        print("Не удалось получить список серверов. Проверьте подключение к интернету.")
        return

    print(f"Найдено серверов: {len(servers)}")
    print("Имена серверов:", ", ".join(servers), "\n")

    # 2. Измеряем время отклика каждого
    results = {}  # server -> время (float) или None
    for server in servers:
        print(f"Тестирую {server}... ", end='', flush=True)
        elapsed = measure_response_time(server)
        if elapsed is not None:
            results[server] = elapsed
            print(f"{elapsed:.3f} сек")
        else:
            results[server] = None
            print("ошибка/таймаут")

    # 3. Статистика по успешным замерам
    successful_times = [t for t in results.values() if t is not None]
    if successful_times:
        median_time = statistics.median(successful_times)
        mean_time = statistics.mean(successful_times)
        print("\n=== ИТОГОВАЯ СТАТИСТИКА ===")
        print(f"Успешных ответов: {len(successful_times)} из {len(servers)}")
        print(f"Медианное время ответа: {median_time:.3f} сек")
        print(f"Среднее время ответа:   {mean_time:.3f} сек")
        print(f"Минимальное время:      {min(successful_times):.3f} сек")
        print(f"Максимальное время:     {max(successful_times):.3f} сек")
    else:
        print("\nНе удалось получить ответ ни от одного сервера. Проверьте соединение с интернетом.")


if __name__ == "__main__":
    main()