"""
Скрипт для заполнения базы данных тестовыми данными
Запускать после запуска приложения: python test_data.py
"""

import requests
import json

API_KEY = "your-secret-api-key-here"
BASE_URL = "http://localhost:8000"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def create_test_data():
    # Создаем здания
    buildings = [
        {"address": "г. Москва, ул. Ленина 1, офис 3", "latitude": 55.7558, "longitude": 37.6176},
        {"address": "г. Москва, ул. Блюхера, 32/1", "latitude": 55.7558, "longitude": 37.6176},
        {"address": "г. Санкт-Петербург, Невский пр., 100", "latitude": 59.9311, "longitude": 30.3609},
        {"address": "г. Новосибирск, ул. Красный проспект, 50", "latitude": 55.0084, "longitude": 82.9357}
    ]

    building_ids = []
    for building in buildings:
        response = requests.post(f"{BASE_URL}/buildings", headers=HEADERS, json=building)
        if response.status_code == 200:
            building_ids.append(response.json()["id"])
            print(f"Created building: {building['address']}")

    # Создаем виды деятельности
    activities_data = [
        # Уровень 1
        {"name": "Еда", "parent_id": None, "level": 1},
        {"name": "Автомобили", "parent_id": None, "level": 1},
        {"name": "IT", "parent_id": None, "level": 1},
    ]

    activity_ids = {}
    for activity in activities_data:
        response = requests.post(f"{BASE_URL}/activities", headers=HEADERS, json=activity)
        if response.status_code == 200:
            activity_id = response.json()["id"]
            activity_ids[activity["name"]] = activity_id
            print(f"Created activity: {activity['name']}")

    # Уровень 2
    level_2_activities = [
        {"name": "Мясная продукция", "parent_id": activity_ids["Еда"], "level": 2},
        {"name": "Молочная продукция", "parent_id": activity_ids["Еда"], "level": 2},
        {"name": "Грузовые", "parent_id": activity_ids["Автомобили"], "level": 2},
        {"name": "Легковые", "parent_id": activity_ids["Автомобили"], "level": 2},
        {"name": "Веб-разработка", "parent_id": activity_ids["IT"], "level": 2},
    ]

    for activity in level_2_activities:
        response = requests.post(f"{BASE_URL}/activities", headers=HEADERS, json=activity)
        if response.status_code == 200:
            activity_id = response.json()["id"]
            activity_ids[activity["name"]] = activity_id
            print(f"Created activity: {activity['name']}")

    # Уровень 3
    level_3_activities = [
        {"name": "Запчасти", "parent_id": activity_ids["Грузовые"], "level": 3},
        {"name": "Аксессуары", "parent_id": activity_ids["Легковые"], "level": 3},
        {"name": "Frontend", "parent_id": activity_ids["Веб-разработка"], "level": 3},
        {"name": "Backend", "parent_id": activity_ids["Веб-разработка"], "level": 3},
    ]

    for activity in level_3_activities:
        response = requests.post(f"{BASE_URL}/activities", headers=HEADERS, json=activity)
        if response.status_code == 200:
            activity_id = response.json()["id"]
            activity_ids[activity["name"]] = activity_id
            print(f"Created activity: {activity['name']}")

    # Создаем организации
    organizations = [
        {
            "name": 'ООО "Рога и Копыта"',
            "phone_numbers": ["2-222-222", "3-333-333", "8-923-666-13-13"],
            "building_id": building_ids[0],
            "activity_ids": [activity_ids["Мясная продукция"], activity_ids["Молочная продукция"]]
        },
        {
            "name": 'ЗАО "Быстрые колеса"',
            "phone_numbers": ["8-800-555-35-35"],
            "building_id": building_ids[1],
            "activity_ids": [activity_ids["Легковые"], activity_ids["Аксессуары"]]
        },
        {
            "name": 'ИП "Грузоперевозки МСК"',
            "phone_numbers": ["495-123-45-67", "926-789-01-23"],
            "building_id": building_ids[0],
            "activity_ids": [activity_ids["Грузовые"], activity_ids["Запчасти"]]
        },
        {
            "name": 'ООО "ТехноСофт"',
            "phone_numbers": ["812-987-65-43"],
            "building_id": building_ids[2],
            "activity_ids": [activity_ids["IT"], activity_ids["Frontend"], activity_ids["Backend"]]
        },
        {
            "name": 'ИП "Продукты у дома"',
            "phone_numbers": ["383-456-78-90"],
            "building_id": building_ids[3],
            "activity_ids": [activity_ids["Еда"]]
        }
    ]

    for org in organizations:
        response = requests.post(f"{BASE_URL}/organizations", headers=HEADERS, json=org)
        if response.status_code == 200:
            print(f"Created organization: {org['name']}")
        else:
            print(f"Failed to create organization: {org['name']}, {response.text}")


if __name__ == "__main__":
    create_test_data()
    print("Test data creation completed!")