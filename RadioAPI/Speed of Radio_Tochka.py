#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
import statistics

# Демонстрационные параметры
BASE_URL = "https://demoaccount.s02.radio-tochka.com:8080"
API_KEY = "p6HLVit4.trl8xfTaFCGpdv74FO3YHNeUsBSDofDx"
SERVER_ID = 1

NUM_REQUESTS = 10  # количество тестовых запросов
DELAY_BETWEEN = 1  # секунды между запросами
QUERY_PARAMS = {"limit": 10, "offset": 0, "server": SERVER_ID}


def measure_single_request():
    """
    Выполняет один GET-запрос и возвращает время отклика в секундах.
    При ошибке возвращает None.
    """
    try:
        start = time.time()
        resp = requests.get(
            f"{BASE_URL}/api/v2/history/",
            params=QUERY_PARAMS,
            headers={"SC-API-KEY": API_KEY},
            timeout=10,
            verify=False  # Отключаем проверку SSL (только для тестового демо)
        )
        elapsed = time.time() - start
        if resp.status_code == 200:
            return elapsed
        else:
            print(f"   HTTP {resp.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"   Ошибка: {e}")
        return None


def main():
    print("=== Измерение скорости ответа Radio-Tochka API ===\n")
    print(f"Параметры: {BASE_URL}/api/v2/history/ {QUERY_PARAMS}")
    print(f"Количество замеров: {NUM_REQUESTS}\n")

    times = []
    for i in range(1, NUM_REQUESTS + 1):
        print(f"Замер {i:2d}... ", end="", flush=True)
        t = measure_single_request()
        if t is not None:
            times.append(t)
            print(f"{t * 1000:.0f} мс")
        else:
            print("пропущен")

        # Пауза между запросами (кроме последнего)
        if i < NUM_REQUESTS:
            time.sleep(DELAY_BETWEEN)

    if times:
        print("\n=== РЕЗУЛЬТАТЫ ===")
        print(f"Успешных запросов: {len(times)} из {NUM_REQUESTS}")
        print(f"Медианное время ответа: {statistics.median(times) * 1000:.0f} мс")
        print(f"Среднее время ответа  : {statistics.mean(times) * 1000:.0f} мс")
        print(f"Минимальное время     : {min(times) * 1000:.0f} мс")
        print(f"Максимальное время    : {max(times) * 1000:.0f} мс")
    else:
        print("\nНе удалось выполнить ни одного успешного запроса.")


if __name__ == "__main__":
    main()