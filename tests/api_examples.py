"""
Примеры использования API
Убедитесь, что приложение запущено и заполнено тестовыми данными
"""

import requests
import json

API_KEY = "your-secret-api-key-here"
BASE_URL = "http://localhost:8000"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def test_all_endpoints():
    print("=== Тестирование API endpoints ===\n")

    # 1. Получить все здания
    print("1. Получение списка всех зданий:")
    response = requests.get(f"{BASE_URL}/buildings", headers=HEADERS)
    if response.status_code == 200:
        buildings = response.json()
        print(f"   Найдено зданий: {len(buildings)}")
        for building in buildings[:2]:  # Показываем первые 2
            print(f"   - {building['address']} (ID: {building['id']})")
    else:
        print(f"   Ошибка: {response.status_code}")
    print()

    # 2. Поиск организаций по зданию
    print("2. Поиск организаций в здании ID=1:")
    response = requests.get(f"{BASE_URL}/organizations/by-building/1", headers=HEADERS)
    if response.status_code == 200:
        organizations = response.json()
        print(f"   Найдено организаций: {len(organizations)}")
        for org in organizations:
            print(f"   - {org['name']} (тел: {', '.join(org['phone_numbers'])})")
    else:
        print(f"   Ошибка: {response.status_code}")
    print()

    # 3. Поиск по виду деятельности (иерархический)
    print("3. Поиск организаций по виду деятельности 'Еда' (ID=1, включая дочерние):")
    response = requests.get(f"{BASE_URL}/organizations/by-activity/1", headers=HEADERS)
    if response.status_code == 200:
        organizations = response.json()
        print(f"   Найдено организаций: {len(organizations)}")
        for org in organizations:
            activities = [act['name'] for act in org['activities']]
            print(f"   - {org['name']} (деятельность: {', '.join(activities)})")
    else:
        print(f"   Ошибка: {response.status_code}")
    print()

    # 4. Поиск в радиусе (центр Москвы)
    print("4. Поиск организаций в радиусе 50 км от центра Москвы:")
    params = {
        "latitude": 55.7558,
        "longitude": 37.6176,
        "radius": 50
    }
    response = requests.get(f"{BASE_URL}/organizations/in-radius", headers=HEADERS, params=params)
    if response.status_code == 200:
        organizations = response.json()
        print(f"   Найдено организаций: {len(organizations)}")
        for org in organizations:
            building = org['building']
            print(f"   - {org['name']} ({building['address']})")
    else:
        print(f"   Ошибка: {response.status_code}")
    print()

    # 5. Поиск в прямоугольной области
    print("5. Поиск организаций в прямоугольной области (Москва-СПб):")
    params = {
        "min_lat": 55.0,
        "max_lat": 60.0,
        "min_lon": 30.0,
        "max_lon": 38.0
    }
    response = requests.get(f"{BASE_URL}/organizations/in-rectangle", headers=HEADERS, params=params)
    if response.status_code == 200:
        organizations = response.json()
        print(f"   Найдено организаций: {len(organizations)}")
        for org in organizations:
            building = org['building']
            print(f"   - {org['name']} ({building['address']})")
    else:
        print(f"   Ошибка: {response.status_code}")
    print()

    # 6. Поиск по названию
    print("6. Поиск организаций по названию 'Рога':")
    params = {"name": "Рога"}
    response = requests.get(f"{BASE_URL}/organizations/search/by-name", headers=HEADERS, params=params)
    if response.status_code == 200:
        organizations = response.json()
        print(f"   Найдено организаций: {len(organizations)}")
        for org in organizations:
            print(f"   - {org['name']}")
    else:
        print(f"   Ошибка: {response.status_code}")
    print()

    # 7. Получение информации об организации по ID
    print("7. Получение информации об организации ID=1:")
    response = requests.get(f"{BASE_URL}/organizations/1", headers=HEADERS)
    if response.status_code == 200:
        org = response.json()
        print(f"   Название: {org['name']}")
        print(f"   Телефоны: {', '.join(org['phone_numbers'])}")
        print(f"   Адрес: {org['building']['address']}")
        activities = [act['name'] for act in org['activities']]
        print(f"   Деятельность: {', '.join(activities)}")
    else:
        print(f"   Ошибка: {response.status_code}")
    print()

    # 8. Создание нового здания
    print("8. Создание нового здания:")
    new_building = {
        "address": "г. Екатеринбург, ул. Ленина, 50",
        "latitude": 56.8431,
        "longitude": 60.6454
    }
    response = requests.post(f"{BASE_URL}/buildings", headers=HEADERS, json=new_building)
    if response.status_code == 200:
        building = response.json()
        print(f"   Создано здание ID={building['id']}: {building['address']}")
        new_building_id = building['id']
    else:
        print(f"   Ошибка: {response.status_code} - {response.text}")
        new_building_id = None
    print()

    # 9. Создание нового вида деятельности
    print("9. Создание нового вида деятельности:")
    new_activity = {
        "name": "Услуги",
        "parent_id": None,
        "level": 1
    }
    response = requests.post(f"{BASE_URL}/activities", headers=HEADERS, json=new_activity)
    if response.status_code == 200:
        activity = response.json()
        print(f"   Создана деятельность ID={activity['id']}: {activity['name']}")
        new_activity_id = activity['id']
    else:
        print(f"   Ошибка: {response.status_code} - {response.text}")
        new_activity_id = None
    print()

    # 10. Создание новой организации
    if new_building_id and new_activity_id:
        print("10. Создание новой организации:")
        new_organization = {
            "name": "ООО \"Новая компания\"",
            "phone_numbers": ["8-800-100-20-30", "343-123-45-67"],
            "building_id": new_building_id,
            "activity_ids": [new_activity_id]
        }
        response = requests.post(f"{BASE_URL}/organizations", headers=HEADERS, json=new_organization)
        if response.status_code == 200:
            org = response.json()
            print(f"   Создана организация ID={org['id']}: {org['name']}")
        else:
            print(f"   Ошибка: {response.status_code} - {response.text}")
        print()


def test_error_cases():
    print("=== Тестирование обработки ошибок ===\n")

    # Неверный API ключ
    print("1. Тест с неверным API ключом:")
    wrong_headers = {"Authorization": "Bearer wrong-key"}
    response = requests.get(f"{BASE_URL}/buildings", headers=wrong_headers)
    print(f"   Статус: {response.status_code} (ожидается 401)")
    print()

    # Несуществующая организация
    print("2. Поиск несуществующей организации:")
    response = requests.get(f"{BASE_URL}/organizations/99999", headers=HEADERS)
    print(f"   Статус: {response.status_code} (ожидается 404)")
    print()

    # Попытка создать деятельность 4-го уровня
    print("3. Попытка создать деятельность 4-го уровня:")
    # Сначала создаем 3 уровня
    level1 = {"name": "Тест уровень 1", "parent_id": None, "level": 1}
    response1 = requests.post(f"{BASE_URL}/activities", headers=HEADERS, json=level1)
    if response1.status_code == 200:
        id1 = response1.json()['id']

        level2 = {"name": "Тест уровень 2", "parent_id": id1, "level": 2}
        response2 = requests.post(f"{BASE_URL}/activities", headers=HEADERS, json=level2)
        if response2.status_code == 200:
            id2 = response2.json()['id']

            level3 = {"name": "Тест уровень 3", "parent_id": id2, "level": 3}
            response3 = requests.post(f"{BASE_URL}/activities", headers=HEADERS, json=level3)
            if response3.status_code == 200:
                id3 = response3.json()['id']

                # Пытаемся создать 4-й уровень
                level4 = {"name": "Тест уровень 4", "parent_id": id3, "level": 4}
                response4 = requests.post(f"{BASE_URL}/activities", headers=HEADERS, json=level4)
                print(f"   Статус: {response4.status_code} (ожидается 400)")
                if response4.status_code == 400:
                    print(f"   Сообщение: {response4.json().get('detail', 'Нет детали')}")
    print()


def performance_test():
    print("=== Простой тест производительности ===\n")

    import time

    # Тест поиска по названию
    start_time = time.time()
    for i in range(10):
        response = requests.get(f"{BASE_URL}/organizations/search/by-name?name=компания", headers=HEADERS)
    end_time = time.time()
    avg_time = (end_time - start_time) / 10
    print(f"Среднее время поиска по названию: {avg_time:.3f} секунд")

    # Тест географического поиска
    start_time = time.time()
    for i in range(10):
        params = {"latitude": 55.7558, "longitude": 37.6176, "radius": 10}
        response = requests.get(f"{BASE_URL}/organizations/in-radius", headers=HEADERS, params=params)
    end_time = time.time()
    avg_time = (end_time - start_time) / 10
    print(f"Среднее время географического поиска: {avg_time:.3f} секунд")
    print()


if __name__ == "__main__":
    try:
        test_all_endpoints()
        test_error_cases()
        performance_test()
        print("✅ Все тесты завершены!")
    except requests.exceptions.ConnectionError:
        print("❌ Ошибка соединения. Убедитесь, что приложение запущено на http://localhost:8000")
    except Exception as e:
        print(f"❌ Ошибка: {e}")