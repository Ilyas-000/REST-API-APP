"""
Простой мониторинг здоровья API
"""

import requests
import time
import json
from datetime import datetime

API_KEY = "your-secret-api-key-here"
BASE_URL = "http://localhost:8000"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def check_api_health():
    """Проверяет здоровье API"""
    checks = {
        "timestamp": datetime.now().isoformat(),
        "status": "healthy",
        "checks": {}
    }

    # Проверка базового endpoint
    try:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/buildings", headers=HEADERS, timeout=5)
        response_time = time.time() - start_time

        checks["checks"]["buildings_endpoint"] = {
            "status": "ok" if response.status_code == 200 else "error",
            "response_time": round(response_time, 3),
            "status_code": response.status_code
        }
    except Exception as e:
        checks["checks"]["buildings_endpoint"] = {
            "status": "error",
            "error": str(e)
        }
        checks["status"] = "unhealthy"

    # Проверка поиска организаций
    try:
        start_time = time.time()
        response = requests.get(f"{BASE_URL}/organizations/search/by-name?name=test", headers=HEADERS, timeout=5)
        response_time = time.time() - start_time

        checks["checks"]["search_endpoint"] = {
            "status": "ok" if response.status_code == 200 else "error",
            "response_time": round(response_time, 3),
            "status_code": response.status_code
        }
    except Exception as e:
        checks["checks"]["search_endpoint"] = {
            "status": "error",
            "error": str(e)
        }
        checks["status"] = "unhealthy"

    # Проверка географического поиска
    try:
        start_time = time.time()
        params = {"latitude": 55.7558, "longitude": 37.6176, "radius": 1}
        response = requests.get(f"{BASE_URL}/organizations/in-radius", headers=HEADERS, params=params, timeout=5)
        response_time = time.time() - start_time

        checks["checks"]["geo_search_endpoint"] = {
            "status": "ok" if response.status_code == 200 else "error",
            "response_time": round(response_time, 3),
            "status_code": response.status_code
        }
    except Exception as e:
        checks["checks"]["geo_search_endpoint"] = {
            "status": "error",
            "error": str(e)
        }
        checks["status"] = "unhealthy"

    return checks


def monitor_continuously(interval=60, duration=300):
    """Непрерывный мониторинг API"""
    print(f"Начинаем мониторинг API каждые {interval} секунд в течение {duration} секунд...")
    print("-" * 80)

    start_time = time.time()

    while time.time() - start_time < duration:
        health_status = check_api_health()

        # Выводим статус
        timestamp = health_status["timestamp"]
        status = health_status["status"]

        status_icon = "✅" if status == "healthy" else "❌"
        print(f"{status_icon} {timestamp} - API Status: {status.upper()}")

        # Детали по каждому check
        for check_name, check_result in health_status["checks"].items():
            check_status = check_result["status"]
            check_icon = "✅" if check_status == "ok" else "❌"

            if "response_time" in check_result:
                response_time = check_result["response_time"]
                print(f"   {check_icon} {check_name}: {response_time}s")
            elif "error" in check_result:
                error = check_result["error"]
                print(f"   {check_icon} {check_name}: {error}")

        print("-" * 80)
        time.sleep(interval)


def save_health_report():
    """Сохраняет отчет о здоровье API в файл"""
    health_status = check_api_health()

    filename = f"health_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(health_status, f, ensure_ascii=False, indent=2)

    print(f"Отчет сохранен в {filename}")
    return health_status


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "monitor":
            # Непрерывный мониторинг
            interval = int(sys.argv[2]) if len(sys.argv) > 2 else 60
            duration = int(sys.argv[3]) if len(sys.argv) > 3 else 300
            monitor_continuously(interval, duration)
        elif sys.argv[1] == "report":
            # Одноразовый отчет
            health_status = save_health_report()
            print("\nТекущий статус:")
            print(json.dumps(health_status, ensure_ascii=False, indent=2))
    else:
        # Простая проверка
        health_status = check_api_health()
        print(json.dumps(health_status, ensure_ascii=False, indent=2))