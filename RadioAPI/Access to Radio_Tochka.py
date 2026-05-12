#!/usr/bin/env python3
# -- coding: utf-8 --

import requests
import sys

# Демонстрационные параметры из официальной документации Radio‑Tochka
BASE_URL = "https://demoaccount.s02.radio-tochka.com:8080"
API_KEY  = "p6HLVit4.trl8xfTaFCGpdv74FO3YHNeUsBSDofDx"   # тестовый ключ
SERVER_ID = 1                                              # ID сервера на демо‑аккаунте

def get_now_playing():
    """
    Запрашивает последний трек из истории эфира (Now Playing).
    Возвращает словарь с данными трека или None при ошибке.
    """
    try:
        resp = requests.get(
            f"{BASE_URL}/api/v2/history/",
            params={"limit": 1, "offset": 0, "server": SERVER_ID},
            headers={"SC-API-KEY": API_KEY},
            timeout=15
        )
        if resp.status_code == 200:
            data = resp.json()
            if data.get("results"):
                return data["results"][0]
            else:
                print("История пуста — радио, возможно, не вещает.")
                return None
        else:
            print(f"Ошибка HTTP {resp.status_code}: {resp.text[:200]}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Сетевая ошибка: {e}")
        return None

def main():
    print("=== Проверка доступности API Radio‑Tochka ===\n")
    track = get_now_playing()
    if track:
        print(f"API доступен. Сейчас играет:\n"
              f"   Исполнитель : {track['author']}\n"
              f"   Название    : {track['title']}\n"
              f"   Альбом      : {track['album']}\n"
              f"   Длительность: {track['length'] // 1000} сек\n"
              f"   Слушателей  : {track['n_listeners']}\n"
              f"   Метаданные  : {track['metadata']}\n"
              f"   Обложка     : {track['img_url']}")
    else:
        print("Не удалось получить данные о треке.")

if __name__ == "__main__":
    main()
