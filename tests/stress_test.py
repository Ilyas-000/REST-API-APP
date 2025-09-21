"""
Простой stress test для API
"""

import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import statistics

API_KEY = "your-secret-api-key-here"
BASE_URL = "http://localhost:8000"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def make_request(endpoint):
    """Выполняет один запрос и возвращает время выполнения"""
    start_time = time.time()
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", headers=HEADERS, timeout=10)
        end_time = time.time()
        return {
            'success': response.status_code == 200,
            'time': end_time - start_time,
            'status_code': response.status_code
        }
    except Exception as e:
        end_time = time.time()
        return {
            'success': False,
            'time': end_time - start_time,
            'error': str(e)
        }


def stress_test(endpoint, num_requests=100, num_threads=10):
    """Выполняет stress test для конкретного endpoint"""
    print(f"Тестирование {endpoint} - {num_requests} запросов в {num_threads} потоков")

    start_time = time.time()
    results = []

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [executor.submit(make_request, endpoint) for _ in range(num_requests)]
        results = [future.result() for future in futures]

    end_time = time.time()
    total_time = end_time - start_time

    # Анализ результатов
    successful_requests = [r for r in results if r['success']]
    failed_requests = [r for r in results if not r['success']]

    if successful_requests:
        response_times = [r['time'] for r in successful_requests]
        avg_response_time = statistics.mean(response_times)
        min_response_time = min(response_times)
        max_response_time = max(response_times)
        median_response_time = statistics.median(response_times)

        print(f"  ✅ Успешных запросов: {len(successful_requests)}/{num_requests}")
        print(f"  ⏱️ Общее время: {total_time:.2f} сек")
        print(f"  📊 RPS (запросов/сек): {num_requests / total_time:.2f}")
        print(f"  📈 Среднее время ответа: {avg_response_time:.3f} сек")
        print(f"  📈 Медианное время ответа: {median_response_time:.3f} сек")
        print(f"  📈 Мин/Макс время ответа: {min_response_time:.3f}/{max_response_time:.3f} сек")

    if failed_requests:
        print(f"  ❌ Неудачных запросов: {len(failed_requests)}")
        error_types = {}
        for req in failed_requests:
            error = req.get('error', f"HTTP {req.get('status_code', 'Unknown')}")
            error_types[error] = error_types.get(error, 0) + 1

        for error, count in error_types.items():
            print(f"     {error}: {count}")

    print()


def main():
    print("=== Stress Test для Organizations API ===\n")

    # Проверяем доступность API
    try:
        response = requests.get(f"{BASE_URL}/buildings", headers=HEADERS, timeout=5)
        if response.status_code != 200:
            print(f"❌ API недоступен. Статус: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Не удается подключиться к API: {e}")
        return

    print("✅ API доступен, начинаем тестирование...\n")

    # Тестируем разные endpoints
    endpoints_to_test = [
        "/buildings",
        "/organizations/by-building/1",
        "/organizations/by-activity/1",
        "/organizations/search/by-name?name=компания",
        "/organizations/in-radius?latitude=55.7558&longitude=37.6176&radius=10"
    ]

    for endpoint in endpoints_to_test:
        stress_test(endpoint, num_requests=50, num_threads=5)

    print("🏁 Stress test завершен!")


if __name__ == "__main__":
    main()