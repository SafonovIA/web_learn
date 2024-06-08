import requests
from flask import current_app # Текущее фласк приложение

def wether_by_city(city_name):
    url = current_app.config["WETHER_URL"]
    params = {
        "key": current_app.config["KEY"],
        "q": city_name,
        "format": "json",
        "num_of_days": 1
    }

    try:
        wt = requests.get(url, params=params) # Передача в реквестс ссылки и пареметров
        wt.raise_for_status() # Сгенерирует ошибку если сервер ответил кодом 4** или 5**
        wt = wt.json() # Перевод в json
        if "data" in wt: # Поиск словоря с температурой
            if "current_condition" in wt["data"]:
                try:
                    return wt["data"]["current_condition"][0]
                except(IndexError, TypeError):
                    return False
        return False
    except(requests.RequestException, ValueError): # Сетевые ошибки и ошибки значений
        return False

if __name__ == "__main__":
    pass
