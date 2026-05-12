#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
import statistics

STREAM_ID = "57c48171-4b6f-4609-9ceb-29238c52815f"
BASE_URL = f"https://openapi.streamafrica.cloud/metadata/{STREAM_ID}"
QUERY_PARAMS = {"history": "true"}
NUM_REQUESTS = 10
DELAY_BETWEEN = 1  # секунды между запросами

def measure_single_request():
    try:
        start = time.time()
        resp = requests.get(
            BASE_URL,
            params=QUERY_PARAMS,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
            timeout=10,
            verify=False   # отключаем проверку SSL для тестов (если нужно)
        )
        elapsed = time.time() - start

        if resp.status_code == 200:
            return elapsed
        else:
            print(f"   HTTP {resp.status_code} — {resp.text[:50]}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"   Ошибка: {e}")
        return None

def main():
    print("Измерение скорости ответа RadioAPI\n")
    print(f"Эндпоинт: {BASE_URL}")
    print(f"Параметры: {QUERY_PARAMS}")
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

        if i < NUM_REQUESTS:
            time.sleep(DELAY_BETWEEN)

    if times:
        print("\nРЕЗУЛЬТАТЫ")
        print(f"Успешных запросов: {len(times)} из {NUM_REQUESTS}")
        print(f"Медианное время ответа: {statistics.median(times) * 1000:.0f} мс")
        print(f"Среднее время ответа  : {statistics.mean(times) * 1000:.0f} мс")
        print(f"Минимальное время     : {min(times) * 1000:.0f} мс")
        print(f"Максимальное время    : {max(times) * 1000:.0f} мс")
    else:
        print("\nНе удалось выполнить ни одного успешного запроса.")
        print("Проверьте STREAM_ID и доступность API (возможно, требуется VPN).")

if __name__ == "__main__":
    main()