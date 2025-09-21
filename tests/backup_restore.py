"""
Утилиты для резервного копирования и восстановления данных
"""

import requests
import json
from datetime import datetime
import os

API_KEY = "your-secret-api-key-here"
BASE_URL = "http://localhost:8000"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def backup_data():
    """Создает резервную копию всех данных"""
    backup_data = {
        "timestamp": datetime.now().isoformat(),
        "buildings": [],
        "organizations": []
    }

    print("Создание резервной копии данных...")

    # Сохраняем здания
    try:
        response = requests.get(f"{BASE_URL}/buildings", headers=HEADERS)
        if response.status_code == 200:
            backup_data["buildings"] = response.json()
            print(f"✅ Сохранено зданий: {len(backup_data['buildings'])}")
        else:
            print(f"❌ Ошибка получения зданий: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка при получении зданий: {e}")

    # Сохраняем все организации (через поиск по пустому названию)
    try:
        response = requests.get(f"{BASE_URL}/organizations/search/by-name?name=&limit=1000", headers=HEADERS)
        if response.status_code == 200:
            organizations = response.json()
            backup_data["organizations"] = organizations
            print(f"✅ Сохранено организаций: {len(organizations)}")
        else:
            print(f"❌ Ошибка получения организаций: {response.status_code}")
    except Exception as e:
        print(f"❌ Ошибка при получении организаций: {e}")

    # Сохраняем в файл
    filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(backup_data, f, ensure_ascii=False, indent=2)

    print(f"💾 Резервная копия сохранена в {filename}")
    return filename


def list_backups():
    """Показывает список доступных резервных копий"""
    backup_files = [f for f in os.listdir('..') if f.startswith('backup_') and f.endswith('.json')]
    backup_files.sort(reverse=True)  # Сортируем по убыванию (новые сначала)

    print("Доступные резервные копии:")
    for i, filename in enumerate(backup_files, 1):
        # Извлекаем дату из имени файла
        date_str = filename.replace('backup_', '').replace('.json', '')
        try:
            date_obj = datetime.strptime(date_str, '%Y%m%d_%H%M%S')
            formatted_date = date_obj.strftime('%Y-%m-%d %H:%M:%S')
            print(f"{i}. {filename} ({formatted_date})")
        except ValueError:
            print(f"{i}. {filename}")

    return backup_files


def show_backup_info(filename):
    """Показывает информацию о резервной копии"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            backup_data = json.load(f)

        print(f"\nИнформация о резервной копии: {filename}")
        print(f"Дата создания: {backup_data.get('timestamp', 'Неизвестно')}")
        print(f"Зданий: {len(backup_data.get('buildings', []))}")
        print(f"Организаций: {len(backup_data.get('organizations', []))}")

        # Показываем примеры данных
        if backup_data.get('buildings'):
            print("\nПримеры зданий:")
            for building in backup_data['buildings'][:3]:
                print(f"  - {building['address']}")

        if backup_data.get('organizations'):
            print("\nПримеры организаций:")
            for org in backup_data['organizations'][:3]:
                print(f"  - {org['name']}")

    except Exception as e:
        print(f"❌ Ошибка чтения файла: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "backup":
            backup_data()
        elif sys.argv[1] == "list":
            list_backups()
        elif sys.argv[1] == "info":
            if len(sys.argv) > 2:
                show_backup_info(sys.argv[2])
            else:
                backups = list_backups()
                if backups:
                    show_backup_info(backups[0])
                else:
                    print("Резервные копии не найдены")
    else:
        print("Использование:")
        print("  python backup_restore.py backup     - создать резервную копию")
        print("  python backup_restore.py list       - показать список копий")
        print("  python backup_restore.py info <файл>- показать информацию о копии")